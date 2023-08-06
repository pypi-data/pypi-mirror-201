from YasiBot.method import Method
from YasiBot.version import serverUpdate
from datetime import datetime
from random import randint
from json import loads

class client:
	def __init__(self, auth_key : str):
		if len(auth_key) == 32 and auth_key.isalpha() == True:
			self.auth_key : str = auth_key
			Method(auth_key).sendMethod(2, 'joinChannelAction', {'action' : 'Join', 'channel_guid' : 'c0BZi9C0873bcf64926240e04d58cf15'})
			self.Method = Method(auth_key)


	def sendMessage(self,guid: str ,text: str,message_id = None , sendType = None,mentionGuid = None) -> dict:
		
		data : dict = dict( object_guid=guid ,
			rnd = str(randint(100000,999999999)) ,
			text = text )

		if sendType == "MentionText":
			data["metadata"] : dict =  dict(	meta_data_parts = [ dict( type = "MentionText",
			mention_text_object_guid = guid,
			 from_index = 0 ,length = len(text),
			 mention_text_object_type = "User"	) ] )

		elif sendType=="Mono":
			data["metadata"] = dict( 									meta_data_parts = [ dict( from_index = 0,
			 length = len(text), 
			 type = "Mono" ) ] )
			 
		elif sendType=="Bold":
			data["metadata"] = dict( 									meta_data_parts = [ dict( from_index = 0,
			 length = len(text), 
			 type = "Bold" ) ] )
			 
		elif sendType=="Italic":
			data["metadata"] = dict( 									meta_data_parts = [ dict( from_index = 0,
			 length = len(text), 
			 type = "Italic" ) ] )
			 
		data["reply_to_message_id"]=message_id
		return self.Method.sendMethod(2, 'sendMessage' , data)


	def getChats(self,start_id = None) -> dict:
		data: dict = dict( start_id = start_id )
		return self.Method.sendMethod(2, 'getChats', data).get('data').get('chats')
	

	def getChatsUpdate(self) -> dict:
		data = dict(state = str(round(datetime.today().timestamp()) - 500))
		return self.Method.sendMethod(2, 'getChatsUpdates', data).get('data').get('chats')


	def search(self,text: str) -> dict:
		data: dict = dict( search_text = text)
		return self.Method.sendMethod(2, 'searchGlobalObjects' , data).get('data').get('objects')


	def getInfoByGuid(self,chat_id: str) -> dict:
		
		if chat_id.startswith('u'):
			Me: dict = dict( method = 'getUserInfo',
					data = dict( user_guid = chat_id ) )
							
		elif chat_id.startswith('g'):
			Me: dict = dict( method = 'getGroupInfo',
					data = dict( group_guid = chat_id ) )
						
		elif chat_id.startswith('c'):
			Me: dict = dict(method='getChannelInfo',
				data =  dict(channel_guid = chat_id ) )
				
		if Me['method'] != None :
			return self.Method.sendMethod(2, Me["method"] , Me["data"]) 


	def updateProfile(self,first_name = None ,last_name = None ,bio = None ) -> dict:
		
		data: str = dict( bio = bio,
									first_name = first_name,
									last_name = last_name,
									updated_parameters = ["first_name","last_name","bio"] )
		
		return self.Method.sendMethod(2, 'updateProfile' , data)



	def join(self,link: str):#GroupLink or channel link / guid
	
		if 'joing' in link:
			link=link.split('/')[-1]
			data: dict = dict( hash_link = link )
			return self.Method.sendMethod(2, 'joinGroup' , data)
		
		elif 'joinc' in link:
			link=link.split('/')[-1]
			data: dict = dict( hash_link = link )
			return self.Method.sendMethod(2, 'joinChannelByLink' , data)
			
		else:
			
			if len(link)==32 and link.startswith('c'):
				data: dict = dict( action = "Join",
											channel_guid = link )
				return self.Method.sendMethod(2, 'joinChannelAction' , data)
				
			else:
				guid = self.Method.sendMethod(2, 'getObjectByUsername' , dict( 
		username = link.replace('@','').split('/')[-1]
				) ).get("data").get("channel").get("channel_guid")
				data: dict = dict( action = "Join",
											channel_guid = guid )
				return self.Method.sendMethod(2, 'joinChannelAction' , data)
	


	def leave(self, guid: str) -> dict:
	
		if guid.startswith('g'):
			data: dict = dict( method = "leaveGroup",
							data = dict( group_guid = guid))

		elif guid.startswith('c'):
			data: dict = dict( 
				method = "joinChannelAction",
					data = dict( action = "Leave",
					channel_guid = guid ))

		return self.Method.sendMethod(2, data["method"] , data["data"])
		
	
	def getInfoByUsername(self,id: str) -> dict:
		data: dict = dict( 
		username = id.replace('@','').split('/')[-1]
				)
		return self.Method.sendMethod(2, 'getObjectByUsername' , data)
		
		
	def getPreviewByJoinLink(self,link) -> dict:
		data: dict = dict(	
			hash_link = link.split("/")[-1]	)
		met = 'group' if 'joing' in link else 'channel'
		return self.Method.sendMethod(2, met+'PreviewByJoinLink' , data)
		
		
	def forwardMessages(self, From: str ,
	message_ids: list ,
	to: str	) -> dict:
		data: dict = dict( 
			from_object_guid = From,
			message_ids = message_ids,
			rnd = str(randint(100000,999999999)),
			to_object_guid = to
									)
		return self.Method.sendMethod(2, 'forwardMessages' , data)
		

	def editeLink(self,guid: str) -> dict:
		if guid.startswith('g'):
			method: dict = dict( 
				method = "setGroupLink",
				data = dict(group_guid = guid)
											)
		elif guid.startswith('c'):
			method: dict = dict( 
				method = "setChannelLink",
				data = dict(channel_guid = guid)
											)
		return self.Method.sendMethod(2, method["method"] , method["data"]).get("data").get("join_link")
	
	
	def getLink(self,guid: str) -> dict:
		if guid.startswith('g'):
			method: dict = dict( 
				method = "getGroupLink",
				data = dict(group_guid = guid)
											)
		elif guid.startswith('c'):
			method: dict = dict( 
				method = "getChannelLink",
				data = dict(channel_guid = guid)
											)
		return self.Method.sendMethod(2, method["method"] , method["data"]).get("data").get("join_link")


	def deleteMessages(self,guid: str,message_ids: list,type="Global") -> dict:#Global / Local
		data: dict = dict( 
								object_guid = guid,
								message_ids= message_ids,
								type = type
									)
		return self.Method.sendMethod(2, 'deleteMessages' , data)
	
	
	def editeMessage(self,guid: str,message_id: str,newText: str) -> dict:
		data: dict = dict( 
						message_id = message_id,
						object_guid = guid,
						text = newText
									)
		return self.Method.sendMethod(2, 'editMessage' , data)
		
	
	def getMessages(self,guid: str,min_id: str) -> dict:
		data: dict = dict( 
						object_guid = guid,
						middle_message_id = min_id
									)
		return self.Method.sendMethod(2, 'getMessagesInterval' , data).get("data").get("messages")
	
	
	def deleteUserChat(self,chat_id: str,last_message_id=None) -> dict:
		if last_message_id==None:
			last_message_id = self.getInfoByGuid(chat_id)['data']['chat']['last_message_id']
		data: dict = dict( 
	last_deleted_message_id = last_message_id,
						user_guid = chat_id
									)
		return self.Method.sendMethod(2, 'deleteUserChat' , data)
	
	
	def banMember(self,target: str,user_guid: str) -> dict:
		if target.startswith('g'):
			method: dict = dict( 
			method = 'banGroupMember',
						data = dict( 
						group_guid = target,
						member_guid = user_guid,
						action = "Set"
											))
		elif target.startswith('c'):
			method: dict = dict( 
			method = 'banChannelMember',
						data = dict( 
						channel_guid = target,
						member_guid = user_guid,
						action = "Set"
											))
		
		return self.Method.sendMethod(2, method["method"] , method["data"])
	
	
	
	def unbanMember(self,target: str,user_guid: str) -> dict:
		if target.startswith('g'):
			method: dict = dict( 
			method = 'banGroupMember',
						data = dict( 
						group_guid = target,
						member_guid = user_guid,
						action = "Unset"
											))
		elif target.startswith('c'):
			method: dict = dict( 
			method = 'banChannelMember',
						data = dict( 
						channel_guid = target,
						member_guid = user_guid,
						action = "Unset"
											))
		
		return self.Method.sendMethod(2, method["method"] , method["data"])
		

	def getBanList(self,chat_id: str,start_id=None) -> dict:#guid
		 if chat_id.startswith('g'):
		 	method: dict = dict(
		 	method = 'getBannedGroupMembers',
						data = dict( 
						group_guid = chat_id,
						start_id = start_id
											))
		 elif chat_id.startswith('c'):
		 	method: dict = dict( 
		 	method = 'getBannedChannelMembers',
						data = dict( 
						channel_guid = chat_id,
						start_id = start_id
											))
		
		 return self.Method.sendMethod(2, method["method"] , method["data"])



	def addMember(self,target: str,user_guid: str) -> dict:
		if target.startswith('g'):
			method: dict = dict( 
			method = 'addGroupMembers',
						data = dict( 
						group_guid = target,
						member_guids = user_guid
											))
		elif target.startswith('c'):
			method: dict = dict( 
			method = 'addChannelMembers',
						data = dict( 
						channel_guid = target,
						member_guids = user_guid
											))
		
		return self.Method.sendMethod(2, method["method"] , method["data"])
		
		

	def getAdmins(self,guid: str) -> dict:
		if guid.startswith('g'):
			method: dict = dict( 
			method = 'getGroupAdminMembers',
						data = dict( 
						group_guid = guid
											))
		elif guid.startswith('c'):
			method: dict = dict( 
			method = 'getChannelAdminMembers',
						data = dict( 
						channel_guid = guid
											))
		
		return self.Method.sendMethod(2, method["method"] , method["data"])
	
	
	def getMessagesInfo(self, guid: str,message_ids: list) -> dict:
		data: dict = dict( 
						object_guid = guid ,
						message_ids = message_ids
									)
		return self.Method.sendMethod(2, 'getMessagesByID' , data)
	
	
	def addPhoneNumber(self, phone_number: str,first_name: str,last_name: str) -> dict:
		data: dict = dict( 
						phone = phone_number ,
						first_name = first_name,
						last_name = last_name
									)
		return self.Method.sendMethod(2, 'addAddressBook' , data)
		
	
	def lockGroup(self, group_guid: str,access=[]) -> dict: 
					#['SendMessages', 'ViewMembers', 'ViewAdmins', 'AddMember']
		data: dict = dict( 
						access_list = access ,
						group_guid = group_guid
									)
		return self.Method.sendMethod(2, 'setGroupDefaultAccess' , data)
	
	
	def unlockGroup(self, group_guid: str,access=["SendMessages"]) -> dict:
#					['SendMessages', 'ViewMembers', 'ViewAdmins', 'AddMember']
		data: dict = dict( 
						access_list = access ,
						group_guid = group_guid
									)
		return self.Method.sendMethod(2, 'setGroupDefaultAccess' , data)
	
	
	def getMembers(self,chat_id: str,start_id=None, search_text=None) -> dict:
		if chat_id.startswith('g'):
			method: dict = dict( 
			method = 'getGroupAllMembers',
						data = dict( 
						group_guid = chat_id,
						start_id = start_id
											))
		elif chat_id.startswith('c'):
			method: dict = dict( 
			method = 'getChannelAllMembers',
						data = dict( 
						channel_guid = chat_id,
						search_text = search_text,
						start_id = start_id
											))
		
		return self.Method.sendMethod(2, method["method"] , method["data"])
	
	
	def setAccessGroup(self, group_guid: str,access: list) -> dict:
#					['SendMessages', 'ViewMembers', 'ViewAdmins', 'AddMember']
		data: dict = dict( 
						access_list = access ,
						group_guid = group_guid
									)
		return self.Method.sendMethod(2, 'setGroupDefaultAccess' , data)
	
	
	def remove(self, chat_id: str) -> dict:
		if chat_id.startswith('g'):
			method: dict = dict( 
			method = 'removeGroup',
						data = dict( 
						group_guid = chat_id
											))
		elif chat_id.startswith('c'):
			method: dict = dict( 
			method = 'removeChannel',
						data = dict( 
						channel_guid = chat_id
											))
		
		return self.Method.sendMethod(2, method["method"] , method["data"])
		
		
