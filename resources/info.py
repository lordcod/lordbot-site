import random
import string

password = '1'#.join(random.choice(string.ascii_letters + string.digits) for _ in range(26))

invite_bot_link = (
    'https://discord.com/api/oauth2/authorize'
    '?client_id=1095713975532007434'
    '&permissions=-1'
    '&scope=bot%20applications.commands'
    # '&response_type=code'
    # '&redirect_uri=https://lordbot.ru/link-role-callback'
)


lord = "http://localhost:5000"


dis_redirect_uri = f'{lord}/link-role-callback'
dis_client_id = '1095713975532007434'
dis_client_secret = 'Dq0HY3D3sAxauD2_HxEsIxzZoyBT5_4H'
dis_scope = 'role_connections.write%20guilds%20identify'
dis_url_auth = f"https://discord.com/api/oauth2/authorize?client_id={dis_client_id}&redirect_uri={dis_redirect_uri}&response_type=code&scope={dis_scope}"
token = "MTA5NTcxMzk3NTUzMjAwNzQzNA.GdoeFJ.RuUbalItmQArVDmqcKLLK_2eImRpt-glwLyarI"

ro_client_id = '6296235449675032791'
ro_client_secret = "RBX-7pnQsYKEQEu2V4mjq1dQAFkMJKVF4SMy00WJMHS-4MY98tb8tpnV3QRInxzOWucE"
ro_redirect_uri = f'{lord}/rover'

ro_url_auth = f"https://apis.roblox.com/oauth/v1/authorize\
?client_id={ro_client_id}\
&redirect_uri={ro_redirect_uri}\
&scope=openid\
&response_type=code\
&nonce=1234\
&state=world"

my_roblox_cookie = (
    '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_'
    'AEC4F78B993738F0B9DFE2FD39A5ADEB9CF3EB71D9F8424770305BD396368B57DAD8CEAC9A9DB03DF29BE61F2D50E16AF7F3C9EBD1DFBA6BE1D81A1722EEAF4399C36C047245AFA9D3DF2A513E4399AD0BA00D9DC7EF0C31A1AF485069DC9BDED3718016364818AFBE126B378DEAAA47238C139B77A0338632E0F63E81FD9401F2F272B0BB7FD6EE5D950D0A06DA24B839ACFF577F459C70ECFD2B2A2678A34B515A880E25ED318828AA9B001E0312A5AA8391D5F19ECEDD8F48EA2334BB33DD83328FAA452117046A5D2183EF442CF68848AE10AD5521811C367BAB7F14E79F2B19BF4C0FC2AD7C1EC657260485BD864092309413D09655BBB475E3841AC98811D0EF8CA77755895F5D4E2706F210A4082847D24B6E356AFE1D2B8DF7874513ED8D2271EE391F53F2644B9C91072A7AAECC0E6D87442AE2EE58F40C6E78A4EEDD5BAF2F3E3312095EF50B4D5011C48EF593CCE7B3962FC1744309E4728A7F87059B8C482DEDB0E4D14980234555FB8C92080B822A7BC2488526AD87EF0BBE11E3ACF507751AF057FB49392717BE8BE809FFF70349162F47D4A5D6E439482700694B553812FA6816734CC7AB76B625A3ADE84D655BFEFC885A5E32D7223F6A59AD38FDB4'
)