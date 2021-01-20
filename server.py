import os

from discord.ext import ipc
from quart import Quart, render_template, redirect, url_for, request, session, flash, abort, send_from_directory, \
    jsonify

import davobot

app = Quart(__name__)
ipc_client = ipc.Client(secret_key=davobot.ipc_secret)

app.config.update({
    'DEBUG': True,
    'SECRET_KEY': '4Zh85UDeI2KwfTMxD4px2hGHjUqy2t1w',
    'USERNAME': 'admin',
    'PASSWORD': 'default',
})


@app.before_first_request
async def before():
    app.ipc_node = await ipc_client.discover()  # discover IPC Servers on your network


@app.route('/favicon.ico', methods=['GET'])
async def favicon():
    return await send_from_directory(os.path.join(app.root_path, 'static/media'),
                                     'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login/', methods=['GET', 'POST'])
async def login():
    error = None
    if request.method == 'POST':
        form = await request.form
        if form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            await flash('You were logged in')
            return redirect(url_for('dashboard'))
    return await render_template('login.html', error=error)


@app.route('/logout/')
async def logout():
    session.pop('logged_in', None)
    await flash('You were logged out')
    return redirect(url_for('dashboard'))


@app.route('/dashboard/', methods=['GET', 'POST'])
async def dashboard():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        else:
            formdata = await request.form
            server = formdata['postserver']
            channel = formdata['postchannel']
            message = formdata['postmessage']
            # form['postserver']
            # form['postchannel']
            # form['postmessage']
            await app.ipc_node.request("runPost", server=server, channel=channel, msg=message)
            return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        if session.get('logged_in'):
            bot_latency = await app.ipc_node.request("get_bot_latency", data="")
            guilds = await app.ipc_node.request("get_guilds", data="")
            timer = str(await app.ipc_node.request("get_runtime", data=""))

            def guildloop(listt):
                final_members = []
                for members in listt['members']:
                    final_members.append(members)
                return final_members

            def guildnamesloop(listt):
                final_names = []
                for names in listt['guild']:
                    final_names.append(names)
                return final_names

            def guildidloop(listt):
                final_ids = []
                for ids in listt['id']:
                    final_ids.append(ids)
                return final_ids

            return await render_template('dashboard.html', latency=bot_latency, guilds=guilds,
                                         members=guildloop(guilds), ids=guildidloop(guilds),
                                         names=guildnamesloop(guilds), runtime=timer)
        else:
            return redirect(url_for('login'))


@app.route('/_get_data/', methods=['POST'])
async def _get_data():
    def sliceString(string):
        head1, sep1, tail1 = str(string).partition('&')
        head, sep, tail = head1.partition('=')
        return tail

    guildid = (await request.get_data())
    guildint = int(sliceString(guildid))

    finalguildid = guildint

    guildlist = await app.ipc_node.request("get_guildchannels", id=finalguildid)
    glstr = str(guildlist).replace('\'', '#')
    finallist = glstr.strip('][').split(', ')
    for x in range(len(finallist)):
        finallist[x] = finallist[x].rstrip('#')

    return jsonify(
        {'data': str(await render_template('response.html', myList=finallist))})


@app.route("/api/")
async def test():
    timer = str(await app.ipc_node.request("get_runtime", data=""))
    return timer


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
