import requests
import threading
from bs4 import BeautifulSoup

class PtchUser:
	SIGNUP_URL = "https://ptch.com/signup"
	STREAM_URL = "https://ptch.com/stream"
	USER_URL = "http://ptch.com/v1/user/"
	FOLLOW_SUFFIX = "/follow"
	THUMBNAIL_URL = "http://ptch.com/v1/user/thumbnail"
	SIGNIN_URL = 'https://ptch.com/login'
	SIGNOUT_URL = 'https://ptch.com/signout'

	REGISTER_TEMPLATE = {
		'full_name': 'None',
		'signup_email': 'None',
		'signup_password': 'None',
		'invitation_email': 'None',
		'invitation_code': 'None' }

	userid = None
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
		self.update_helper()
		self.logged_in = True

	def logout(self):
		if self.logged_in: self.session.get(self.SIGNOUT_URL)
		self.logged_in = False

	def update(self):
		thread = threading.Thread(target = self.update_helper)
		thread.start()

	def update_helper(self):
		self.userid = self.get_user_id()
		self.attributes = self.session.get(self.USER_URL + str(self.userid)).json()

	def get_user_id(self): 
		soup = BeautifulSoup(self.session.get(self.STREAM_URL).text)
		try:
			index = soup.text.find('_current_user_id')
			endindex = soup.text.find(';', index)
		except IndexError as e:
			raise PtchError('Not logged in or login failure.', None)
		return int(soup.text[index:endindex].split()[2])

	#follow() is multithreaded. take that bitches
	def follow(self, userid):
		thread = threading.Thread(target = self.follow_helper, args = (userid,))
		thread.start()

	def follow_helper(self, userid):
		postdata = '{"follow_user_id": "' + str(userid) + '"}'
		response = self.session.post(self.USER_URL + str(self.userid) + self.FOLLOW_SUFFIX,
			data = postdata)
		if response.status_code != 200:	raise PtchError("Failed to follow " + str(userid), response)

	def set_thubmnail_helper(self, mfile):
		response = self.session.post(self.THUMBNAIL_URL, files = mfile)
		if response.status_code != 200: raise PtchError("Could not update thumbnail.", response)

	def set_thumbnail(self, mfile):
		thread = threading.Thread(target = self.set_thumbnail_helper, args = (mfile,))
		thread.start()

	def set_thumbnail_url(self, url):
		imgr = requests.get(url)
		mfile = dict(file=('image' + url[url.rfind('.'):], imgr.content))
		self.set_thumbnail(mfile)

class PtchError(Exception):
	def __init__(self, value, response):
		self.value = value
		self.response = response
	def __str__(self):
		return repr(self.value)
