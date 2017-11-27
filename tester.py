from scidash_api import client

client_instance = client.ScidashClient()

print(client_instance.login('admin', 'kavabanga').upload_object({}))
