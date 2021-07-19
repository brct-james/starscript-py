from SpacePyTraders import client

USERNAME = "Greenitthe"
TOKEN = "c8283f54-c08f-4773-8c40-fc99b0071a19"

api = client.Api(USERNAME, TOKEN)

print(api.account.info())