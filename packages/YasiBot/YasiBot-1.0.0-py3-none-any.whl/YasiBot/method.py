from json import loads, dumps
from aiohttp import ClientSession
from YasiBot.encryption import Crypto
from asyncio import get_event_loop
from random import choice
	
class Client:
	web = {"app_name" : "Main", "app_version" : "4.0.7", "platform" : "Web", "package" : "web.rubika.ir", "lang_code" : "fa" }
	android = {"app_name" : "Main", "app_version" : "2.5.4", "platform" : "Android", "package" : "ir.resaneh1.iptv", "lang_code" : "fa"}
	url = choice(
	
	   ['https://messengerg2c36.iranlms.ir',
		'https://messengerg2c28.iranlms.ir',
		'https://messengerg2c39.iranlms.ir',
		'https://messengerg2c46.iranlms.ir',
		'https://messengerg2c58.iranlms.ir']
)

async def main(url: str, data: dict) -> dict:
	async with ClientSession() as response:
		async with response.post(url, data=data) as post:
			return await post.text()
			
def _Post(url, data):
	loop = get_event_loop()
	return loop.run_until_complete(main(url, data))
	
class Method:
	def __init__(self, auth:str):
		self.auth : str = auth
		self.en_options = Crypto(auth)
	
	def sendMethod(self, Type:int, method, data):
		if Type == 1:
			data_dict = dumps({
				"api_version" : "4",
					"auth" : self.auth,
					"client" : Client.android,
					"method" : method,
					"data_enc" : self.en_options.encrypt(dumps(data)
				)}).encode()
			return loads(self.en_options.decrypt(loads(_Post(Client.url , data_dict)).get('data_enc')))
			
		elif Type == 2:
			data_dict = dumps({
				"api_version" : "5",
					"auth" : self.auth,
					"data_enc" : self.en_options.encrypt(
					dumps({
						"method" : method,
						"input" : data,
						"client" : Client.web
				}))}).encode()
			return loads(self.en_options.decrypt(loads(_Post(Client.url , data_dict)).get('data_enc')))