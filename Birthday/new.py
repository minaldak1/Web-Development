import webapp2
	
###code for form
form = """
<form method = "post">
                <label>
                        Month
                        <input type = "text" name = "month">
                </label>
                <label>
                        Day
                        <input type = "text" name = "day">
                </label>
                <label>
                        Year
                        <input type = "text" name = "year">
                </label>
                <br>
                <input type="submit">
</form>
"""

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August','September', 'October', 'November', 'December']
						
def valid_day(day):
	if(day and day.isdigit()):
		day = int(day)
	if(day < 32 and day > 0):
		return day

def valid_month(month):
	if(month):
		month = month.capitalize()
	if(month in months):
		return month

def valid_year(year):
	if(year and year.isdigit()):
		year = int(year)
	if(year < 2020 and year > 1880):
		return year
	
class MainPage(webapp2.RequestHandler):
        def get(self):
                #self.response.headers['Content-Type'] = 'text/plain'
                self.response.out.write(form)
        def post(self):
		userMonth=valid_month(self.request.get('month'))
		userDay=valid_day(self.request.get('day'))
		userYear=valid_year(self.request.get('year'))
		
		if not(userDay and userMonth and userYear):
			self.response.out.write(form)
		else:
			self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)
