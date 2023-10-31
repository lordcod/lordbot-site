import aiohttp
from resources import info
import orjson


async def getTokenResponse(code):
    url = "https://apis.roblox.com/oauth/v1/token"
    data = {
        'client_id':info.ro_client_id,
        'client_secret':info.ro_client_secret ,
        'grant_type':'authorization_code',
        'code':code
    }
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data,headers=headers) as res:
            json = await res.json()
            return json

async def updateRefreshToken(tokens):
    url =  'https://apis.roblox.com/oauth/v1/token' 
    data = {
        'grant_type':'refresh_token',
        'refresh_token':tokens['refresh_token'],
        'client_id':info.ro_client_id,
        'client_secret':info.ro_client_secret
    }
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data,headers=headers) as res:
            json = await res.json()
            return json

async def introspect(tokens):
    url = 'https://apis.roblox.com/oauth/v1/token/introspect' 
    data = {
        'token':tokens["access_token"],
        'client_id':info.ro_client_id,
        'client_secret':info.ro_client_secret
    }
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data,headers=headers) as res:
            json = await res.json()
            return json


async def getInfoResource(tokens):
    url = 'https://apis.roblox.com/oauth/v1/token/resources' 
    data = {
        'token':tokens["access_token"],
        'client_id':info.ro_client_id,
        'client_secret':info.ro_client_secret
    }
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=data,headers=headers) as res:
            json = await res.json()
            return json


async def getUserInfo(uid):
    url = f"https://users.roblox.com/v1/users/{uid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            json = await res.json()
            return json

async def isPremeiumRoblox(uid):
    url = f"https://premiumfeatures.roblox.com/v1/users/{uid}/validate-membership"
    cookies = {".ROBLOSECURITY":info.my_roblox_cookie}
    async with aiohttp.ClientSession() as session:
        async with session.get(url,cookies=cookies) as res:
            json = await res.json()
            return json

async def getAvatar(uid):
    url = f"https://thumbnails.roblox.com/v1/users/avatar"
    params = {
        'userIds':uid,
        'size':'720x720',
        'format':'Png',
        'isCircular':'true'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url,params=params) as res:
            json = await res.json()
            return json

async def getAvatarHeadshot(uid):
    url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot"
    params = {
        'userIds':uid,
        'size':'720x720',
        'format':'Png',
        'isCircular':'true'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url,params=params) as res:
            json = await res.json()
            return json
