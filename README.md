pyptch
======

A Python library for Ptch (http://ptch.com)

Currently features a single class PtchUser with the following features:
- logging in
- logging out
- registering
- following users by ID (async)
- setting profile thumbnail (async)
- retrieving user info (async)

To Use:

<code> 
 import pyptch
 loginuser = pyptch.PtchUser('username', 'password') #logs into this account
 registeruser = pyptch.PtchUser.register(full_name = "name", signup_email = "email", signup_password = "password")
  #registers an account with with information. optional parameters are invitation_email and invitation_code
 loginuser.follow(99999) #will follow user with ID 99999
 loginuser.set_thumbnail(file) #sets the user's thumbnail to image file
 loginuser.set_thumbnail('url') #sets the user's thumbnail to the image at 'url'
</code>
