import webapp2
import re
import cgi


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)
 
def valid_password(password):
    return PASSWORD_RE.match(password)
 
def valid_email(email):
    return EMAIL_RE.match(email)

def escape_html(s):
    return cgi.escape(s, quote = True)

def rot13(s):
    result = ''
    for char in s:
        o = ord(char) 
        if o >= 65 and o <= 90:
            result += chr((((o - 65) + 13 ) % 26 ) + 65)
        elif o >= 97 and o <= 122:
            result += chr((((o - 97) + 13 ) % 26 ) + 97)
        else:
            result += char
    return result

form="""
<!Doctype HTML>
<html>
    <head>
        <title> Signup </title>
    </head>
    <body>
        <h2> Signup </h2>
        <form method = "post">
            <table>
                <tr>
                    <td>
                        <label>
                        Username
                        <input type = "text" name = "username" value = "%(username)s">
                    </td>
                    <td style "color :red" class = "error">
                        %(username_error)s
                    </td>
                </tr>
		<tr>
		    <td>
                        <label>
			Password
			<input type = "password" name = "password" value = "%(password)s">
		    </td>
		    <td style "color:red" class = "error">
			%(password_error)s
		    </td>
		</tr>
		<tr>
		    <td>
                        <label>
			Verify Password
			<input type = "password" name = "verifypassword" value = "%(verifypassword)s">
		    </td>
		    <td style "color:red" class = "error">
			%(verifypassword_error)s
		    </td>
		</tr>
		<tr>
                    <td>
                        <label>
                        Email(optional)
                        <input type = "text" name = "email" value = "%(email)s">
                    </td>
                    <td style "color :red" class = "error">
                        %(email_error)s
                    </td>
                </tr>
				
            </table>

            <br>
            <input type = "submit">
                
        </form>
    </body>
</html>
"""

form2="""
<!DOCTYPE html>
<html>
	<head>
		<title>Unit 2 Signup - Welcome</title>
	</head>
	<body>
		<h2>Welcome, %s!</h2>
	</body>
</html>
"""

form3="""
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(input_area_text)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello World")

class SignupHandler(webapp2.RequestHandler):
    def write_form(self , username_error="" , password_error="", verifypassword_error="", email_error="" ,username="" , password = "" , verifypassword = "" ,email = "" ):
        self.response.write(form % {"username_error":username_error , "password_error":password_error , "verifypassword_error":verifypassword_error , "email_error":email_error ,"username" : escape_html(username) , "password":escape_html(password) , "verifypassword":escape_html(verifypassword) , "email":escape_html(email)})
    def get(self):
        self.write_form()

    def post(self):
        uname = self.request.get("username")
	password = self.request.get("password")
	verifypass = self.request.get("verifypassword")
        email = self.request.get("email")

        username_error = ""
        password_error = ""
        verifypassword_error = ""
        email_error = ""

        error = False


        if not valid_username(uname):
            username_error = "This is not a valid name!"
            error = True

        if not valid_password(password):
            password_error = "This is not a valid password!"
            error = True
        if not verifypass == password:
            verifypassword_error = "Password is not match!"
            error = True
        if not valid_email(email):
            email_error = "This is not a valid email!"
            error = True
        if error:
            self.write_form(username_error , password_error , verifypassword_error , email_error , uname , password , verifypass , email)
        else:
            self.redirect('/welcome?username=%s' % uname)
class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		self.response.out.write(form2 % username)

class RotHandler(webapp2.RequestHandler):
    def write_form(self, input_area_text=""):
        self.response.out.write(form3 % {"input_area_text" : input_area_text})
 
    def get(self):
        self.write_form()
 
    def post(self):
        user_text = self.request.get('text')
        converted_text = rot13(user_text)
        sani_text = escape_html(converted_text)
        self.write_form(sani_text)
            

app = webapp2.WSGIApplication([('/' , MainHandler) , ('/signup' , SignupHandler),('/welcome' , WelcomeHandler) , ('/Rot13' , RotHandler)] , debug = True)
