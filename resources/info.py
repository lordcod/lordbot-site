import random
import string
password = 'dev'#''.join(random.choice(string.ascii_letters + string.digits) for _ in range(26))

lord = "http://localhost:5000"

api = 'https://discord.com/api/v10'

class client():
    id = 1095713975532007434
    secret = 'Dq0HY3D3sAxauD2_HxEsIxzZoyBT5_4H'

redirect_uri = f'{lord}/link-role-callback'
scope = 'role_connections.write+guilds+identify+applications.commands.permissions.update+guilds.join'
url_auth = (
    f"https://discord.com/api/oauth2/authorize"
    f"?client_id={client.id}"
    f"&redirect_uri={redirect_uri}"
    "&response_type=code"
    f"&scope={scope}"
)



token = "MTA5NTcxMzk3NTUzMjAwNzQzNA.GdoeFJ.RuUbalItmQArVDmqcKLLK_2eImRpt-glwLyarI"
