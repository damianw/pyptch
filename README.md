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
---------

<code> import pyptch </code>

To log in:
<code> loginuser = pyptch.PtchUser('username', 'password') </code>

To register:
<code> registeruser = pyptch.PtchUser.register(full_name = "name", signup_email = "email", signup_password = "password") </code>
optional parameters are invitation_email and invitation_code

To follow user with ID 99999:
<code> loginuser.follow(99999) </code>

To set user's thumbnail to an image file:
<code> loginuser.set_thumbnail(file) </code>

To set the user's thumbnail to an image URL:
<code> loginuser.set_thumbnail('url') </code>

