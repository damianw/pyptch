import requests
import threading
import string
import base64
from bs4 import BeautifulSoup

class PtchUser:
	SIGNUP_URL = "https://ptch.com/signup"
	STREAM_URL = "https://ptch.com/stream"
	USER_URL = "http://ptch.com/v1/user/"
	FOLLOW_SUFFIX = "/follow"
	THUMBNAIL_URL = "http://ptch.com/v1/user/thumbnail"
	SIGNIN_URL = 'https://ptch.com/login'
	SIGNOUT_URL = 'https://ptch.com/signout'
	COMMUNITY_URL = 'http://ptch.com/v1/community'
	LIST_SUFFIX = '/list'
	FRIENDS_SUFFIX = '/friends'
	FOLLOWERS_SUFFIX = '/followers'
	LIKES_SUFFIX = '/likes'
	PTCHES_SUFFIX = '/ptchs'

	REGISTER_TEMPLATE = {
		'full_name': 'None',
		'signup_email': 'None',
		'signup_password': 'None',
		'invitation_email': 'None',
		'invitation_code': 'None' }

	USER_FIELDS = ['likes', 'friends', 'followers', 'ptches']
	COMMUNITY_FIELDS = ['list']

	user_id = None
	session = None
	attributes = None
	logged_in = False

	def __init__(self, email, password):
		self.logged_in = False
		self.login(email, password)

	#TODO Error checking
	@classmethod
	def register(cls, **kwargs):
		rdata = cls.REGISTER_TEMPLATE
		for key in rdata:
			if key in kwargs: rdata[key] = kwargs[key]
		r = requests.post(cls.SIGNUP_URL, data = rdata)
		return cls(rdata['signup_email'], rdata['signup_password'])

	#TODO Error checking
	def login(self, email, password):
		self.logout()
		self.session = requests.session()
		ldata = {'signin_email': email, 'signin_password': password,
		 'signin_submit': 'Login'}
		r = self.session.post(self.SIGNIN_URL, data = ldata)
		self.update()
		self.logged_in = True

	def logout(self):
		if self.logged_in: self.session.get(self.SIGNOUT_URL)
		self.logged_in = False

	def update_async(self):
		thread = threading.Thread(target = self.update)
		thread.start()

	def update(self):
		self.user_id = self.get_user_id()
		uurl = self.USER_URL + str(self.user_id)
		curl = self.COMMUNITY_URL + self.LIST_SUFFIX
		self.attributes = self.session.get(uurl).json()
		self.community = self.session.get(curl).json()

	def get_user_data(self, field, **params):
		if field not in self.USER_FIELDS: 
			raise PtchError("No such field: " + field, None)
		url = self.USER_URL + str(self.user_id) + '/' + field
		print(url)
		return self.get_json(url, **params)

	def get_json(self, url, **params):
		return self.session.get(url, params = params).json()

	def get_user_id(self): 
		encoded = None
		for cookie in self.session.cookies:
			if cookie.name == 'ptch_sec_tkt':
				encoded = cookie.value
				break
		if encoded is None: raise PtchError('Not logged in.', None)
		decoded = base64.b64decode(encoded)
		decoded = ''.join(chr(s) for s in decoded if chr(s) in string.printable)
		far = decoded.rfind('|')
		near = far - 5
		#TODO fix this so that we can find this not-stupidly... help?
		#near = decoded.rfind('~', 0, far) + 1
		userid = int(decoded[near:far])
		return userid

	def follow_async(self, userid):
		thread = threading.Thread(target = self.follow, args = (userid,))
		thread.start()

	def follow(self, userid):
		postdata = '{"follow_user_id": "' + str(userid) + '"}'
		response = self.session.post(self.USER_URL + str(self.user_id) + self.FOLLOW_SUFFIX,
			data = postdata)
		if response.status_code != 200:	return False
		return True

	def set_thubmnail(self, mfile):
		response = self.session.post(self.THUMBNAIL_URL, files = mfile)
		if response.status_code != 200: return False
		return True

	def set_thumbnail_async(self, mfile):
		thread = threading.Thread(target = self.set_thumbnail, args = (mfile,))
		thread.start()

	def set_thumbnail_url(self, url):
		imgr = requests.get(url)
		mfile = dict(file=('image' + url[url.rfind('.'):], imgr.content))
		self.set_thumbnail(mfile)

	def set_thumbnail_url_async(self, url):
		thread = threading.Thread(target = self.set_thumbnail_url, args = (url,))
		thread.start()

	@staticmethod
	def resolve_userid(display_name):
		pass

class PtchError(Exception):
	def __init__(self, value, response):
		self.value = value
		self.response = response
	def __str__(self):
		return repr(self.value)
