import siaskynet as skynet
import os
os.system('bash fetch_swagger.sh')
client = skynet.SkynetClient()
midgard_link = client.upload_file("midgard.json")[6:]
skylink = f'https://siasky.net/{midgard_link}'
os.system(f'bash fetch_client.sh midgard {skylink}')
thornode_link = client.upload_file("thornode.json")[6:]
skylink = f'https://siasky.net/{thornode_link}'
os.system(f'bash fetch_client.sh thornode {skylink}')
