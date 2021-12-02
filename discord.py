from requests import post, get
from json import loads, dumps
from time import sleep

class User:
	def __init__(self, email, password):
		self.email = email
		self.password = password

		self.headers = {
			'content-type':'application/json'
		}

		self.token = self.get_token()
		self.headers['authorization'] = self.token

		

	def get_token(self):
		url = 'https://discord.com/api/v9/auth/login'

		data = {
			'login': self.email,
			'password': self.password
		}
		data = dumps(data)

		return post(url, headers=self.headers, data=data).json()['token']

	def get_guild_info(self, guild_id):
		return get(f'https://discord.com/api/guilds/{guild_id}/channels', headers=self.headers).json()

	def get_guild_text_channels(self, guild_id):
		guild_info = self.get_guild_info(guild_id)
		text_channels = [ channel for channel in guild_info if channel['type'] == 0 ]
		return text_channels

	def get_channel_msgs(self, channel_id, limit=10):
		url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}'
		return get(url, headers=self.headers).json()

	def send_msg(self, channel_id, content):
		url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
		data = {'content': content, 'tts': 'false'}
		data = dumps(data)

		return post(url, data=data, headers=self.headers).json()
