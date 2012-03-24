import webapp2
import cgi
import datetime
import urllib
import wsgiref.handlers
import random

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Quote(db.Model):
  quote = db.StringProperty(multiline=True)
  link = db.StringProperty()
  name = db.StringProperty()

class ReplyQuote(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write('<html><head><meta name="txtweb-appkey" content="1f8cf77b-c013-4f4b-a374-41406d2635b9" /></head><body>')
     
      query = db.Query(Quote)
      searchkey = self.request.get('txtweb-message')
      results = query.filter('name =',searchkey).fetch(limit=100)
      rand_num = random.randrange(0,len(results))
      
      self.response.out.write(results[rand_num].quote)
     
      self.response.out.write('</body></html>')

class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write('<html><body>')

      self.response.out.write("""
          <form action="/success" method="post">
            Quote <div><textarea name="quotetext" rows="3" cols="60"></textarea></div>
	  <br>
          Link <input type="text" name="wikiquote_link">
          <input type="submit" value="Submit Quote"></form>
        </body>
      </html>""" #% (urllib.urlencode({'guestbook_name': guestbook_name}),
                 #         cgi.escape(guestbook_name))
		)

class StoreQuote(webapp2.RequestHandler):
  def post(self):
      quote = Quote()
      quote.quote = self.request.get('quotetext')
      quote.link = self.request.get('wikiquote_link')
      quote.name = quote.link[quote.link.rfind('/')+1:]
      quote.put()
      self.response.out.write("Thanks machi, your quote has been submitted")

app = webapp2.WSGIApplication([('/submitquote', MainPage),('/success',StoreQuote),('/quote',ReplyQuote)],
                              debug=True)
