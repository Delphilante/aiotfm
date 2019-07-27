from aiotfm.utils import chatCommu

class Message:
	def __init__(self, author, content, community, client):
		self.author = author
		self.community = chatCommu[community]
		self.content = content
		self._client = client

	def __str__(self):
		return '[{0.author}] {0.content}'.format(self)

	def __repr__(self):
		text = ' '.join('{}={}'.format(k,repr(v)[:32]) for k,v in vars(self).items() if not k.startswith('_'))
		return '<{.__class__.__name__} {}>'.format(self, text)

class Whisper(Message):
	def __init__(self, author, community, receiver, content, client):
		super().__init__(author, content, community, client)
		self.receiver = receiver

		self.sent = self.author==client.username

	async def reply(self, msg):
		return await self._client.whisper(self.author, msg)

	def __str__(self):
		direction = '<' if self.sent else '>'
		author = self.receiver if self.sent else self.author
		return f'{direction} [{self.community}] [{author}] {self.content}'

class Channel:
	def __init__(self, name, client):
		self.name = name
		self._client = client

	def __eq__(self, other):
		if isinstance(other, str):
			return self.name==other
		return self.name==other.name

	async def send(self, message):
		await self._client.sendChannelMessage(self, message)

	async def leave(self):
		await self._client.leaveChannel(self)

	async def who(self):
		pass

class ChannelMessage(Message):
	def __init__(self, author, community, content, channel):
		super().__init__(author, content, community, channel._client)
		self.channel = channel

	async def reply(self, message):
		await self.channel.send(message)

	def __str__(self):
		return '{0.channel.name} [{0.community}] [{0.author}] {0.content}'.format(self)