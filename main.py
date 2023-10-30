import flask
from flask import (Flask,redirect,session,render_template,request)
from resources import (info,discord)

app = Flask(__name__)
app.secret_key = info.password

@app.route("/link-role-callback")
async def role_callback():
    code = request.args.get('code')
    if code:
        tokens = await discord.getOAuthTokens(code)
        if 'error' in tokens:
            return tokens['error']
        tokens['expires_in'] += time.time()
        session['tokens'] = tokens
        return redirect("/")
    else:
        return "Error no attribyte code"

@app.route("/register")
async def register():
    return redirect(info.url_auth)

@app.route("/")
async def home():
    if 'tokens' not in session:
        return redirect("register")

    tokens = session['tokens']
    if time.time() >= tokens['expires_in']:
        tokens = await discord.updateTokens(tokens)
        tokens['expires_in'] += time.time()
        session['tokens'] = tokens
    user = await discord.getUserDate(tokens)
    if 'code' in user:
        del session['tokens']
        return redirect(url_auth)
    
    return '1'

if __name__ == '__main__':
    app.run("0.0.0.0")