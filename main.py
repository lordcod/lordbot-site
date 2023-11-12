import flask
from flask import (Flask,redirect,session,render_template)
import nextcord
import logging
import time
from .resources import (info,discord,roblox)

from functools import wraps


app = Flask(__name__)
app.secret_key = 'None'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

login = True

def check_roblox_auth(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        rotokens = session.get('ro_tokens',None)
        if not rotokens:
            return redirect("/")
        
        if 'error' in rotokens:
            del session['ro_tokens']
            return render_template("/")
        
        intos = await roblox.introspect(rotokens)
        if not intos["active"]:
            rotokens = await roblox.updateRefreshToken(rotokens)
            if 'error' in rotokens:
                del session['ro_tokens']
                return render_template("home.html",rotok=True)
            session['ro_tokens'] = rotokens
        
        ret = await func(*args,**kwargs)
        return ret
    return wrapper

def check_discord_auth(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        tokens = session.get('tokens',None)
        if not tokens:
            return redirect('/')
        
        if time.time() >= tokens['expires_in']:
            tokens = await discord.updateTokens(tokens)
            tokens['expires_in'] += time.time()
            session['tokens'] = tokens
        
        user = await discord.getUserDate(tokens)
        if 'code' in user:
            del session['tokens']
            return redirect('/')
        
        ret = await func(*args,**kwargs)
        return ret
    return wrapper



# TODO registers
@app.route("/link-role")
async def role():
    return redirect(info.dis_url_auth)

@app.route("/link-role-callback")
async def role_callback():
    code = flask.request.args.get('code')
    if code:
        tokens = await discord.getOAuthTokens(code)
        if 'error' in tokens:
            return tokens['error']
        tokens['expires_in'] += time.time()
        session['tokens'] = tokens
        return redirect("/invite")
    else:
        return "Error no attribyte code"

@app.route("/ro-link")
async def ro():
    return redirect(info.ro_url_auth)

@app.route("/rover")
async def rover():
    code = flask.request.args.get('code')
    if code:
        accesss = await roblox.getTokenResponse(code)
        if 'error' in accesss:
            return accesss['error']
        session['ro_tokens'] = accesss
        return redirect("/invite")
    else:
        return "Not found"

@app.route("/invite")
async def invite():
    return render_template("invite.html")

# TODO home
@app.route('/')
async def home():
    return render_template('home/home.html')

@app.route("/profile")
@check_discord_auth
@check_roblox_auth
async def profile():
    #Discord
    tokens = session['tokens']
    user = await discord.getUserDate(tokens)
    
    #Roblox
    rotokens = session['ro_tokens']
    user_id = roblox.getInfoResource(rotokens)
    user_ro = roblox.getUserInfo(user_id)
    
    #Sus
    metadata = {
            'platform_name': 'Roblox',
            'platform_username':user_ro['name'],
            'metadata':{
                'verified': True,
                'premuim':await roblox.isPremeiumRoblox(user_ro['id']),
                'data':user_ro['created'],
            }
        }
    await discord.pushMetadate(metadata,tokens)
    avatar = await roblox.getAvatarHeadshot(user_id)
    return render_template("profile.html",user_ro=user_ro,user_ds=user,avatar=avatar['data'][0]['imageUrl'])

@app.route("/guilds")
@check_discord_auth
async def guilds():
    tokens = session['tokens']
    gs = await discord.getGuilds(tokens)
    if 'message' in gs:
        return gs['message']
    guilds = []
    bot_guilds = []
    for g in gs:
        permission = int(g.get("permissions",0))
        permission = nextcord.Permissions(permission)
        if permission.manage_guild:
            guilds.append(g)
            responce = await discord.isBotGuild(g['id'])
            if responce:
                bot_guilds.append(str(g['id']))
    return render_template("home/guilds.html",guilds=guilds,bot_guilds=bot_guilds)


# TODO ofter
@app.errorhandler(404)
async def page_not_found(err):
    return '404'#render_template("page_not_found.html"),404

@app.route("/dashboard/<int:id>")
async def dashboard(id):
    res = await discord.isBotGuild(id)
    if res:
        return "sus"
    return redirect('/404')

@app.route("/embed-builder")
async def embed_builder():
    return render_template("embed-builder.html")

# TODO ToS and PP
@app.route("/terms")
async def terms():
    return render_template("terms_of_service.html")

@app.route("/terms_of_service")
async def terms_of_service():
    return render_template("terms_of_service.html")

@app.route("/privacy_policy")
async def privacy_policy():
    return render_template("privacy_policy.html")



if __name__ == "__main__":
    app.run("0.0.0.0")