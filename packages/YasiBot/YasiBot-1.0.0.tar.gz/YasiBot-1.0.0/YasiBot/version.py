from os import system
from requests import get
from json import load,loads

version: dict = dict(
							version = 1.0 ,
							TextView = 'TextStartLibrary ' ,
						Update = 'versionLibraryYasiBot'
								)

class serverUpdate:
	server_1: str = f"https://coderapi.ir/api/{version['TextView']}.json"
	server_2: str = f"https://coderapi.ir/api/{version['Update']}.json"
	server: dict = dict(get(server_2).json())
	textView: str = get(server_1).text
	if server['version'] == version['version']:
		print(textView)
	else:
		print('\033[92m'+'Update Library . . .\n\n')
		system(f'pip install {server["install"]=={server["version"]}}')
	if server['status'] != 'OK':print('\033[1m'+'\033[96m'+'Library YasiBot'+'\033[92m'+' OFF'),exit()