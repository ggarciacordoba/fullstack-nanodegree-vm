from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#Connect to the DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):        

    def do_GET(self):
        if self.path.endswith("/restaurants"):

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            output = ""
            output += "<html><body>"
            output += "<h1><a href='/restaurants/new'>Make a New Restaurant</a></h1>"

            restaurants = session.query(Restaurant).all()
            for restaurant in restaurants:
                output += "<h2>"+restaurant.name+"</h2>"
                output += "<p><a href='/restaurant/"+str(restaurant.id)+"/edit'>Edit</a></p>"
                output += "<p><a href='/restaurant/"+str(restaurant.id)+"/delete'>Delete</a></p>"

            output += "</html></body>"
            self.wfile.write(output)
            return

        if self.path.endswith("/restaurants/new"):

            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            output = ""
            output += "<html><body>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Add a new Restaurant</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/edit"):

            #Obtain the id of the restaurant
            restId = self.path.split("/")[2]

            edit_restaurant = session.query(Restaurant).filter_by(id = restId).first()

            print self.path
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            output = ""
            output += "<html><body>"
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/"+str(restId)+"/edit'><h2>Rename "+edit_restaurant.name+"</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('message')


                #Check if the restaurant is already on the db
                checked_restaurant = session.query(Restaurant).filter_by(name = messagecontent[0]).first()
                print checked_restaurant
                
                if(checked_restaurant == None):
                    restaurant = Restaurant(name=messagecontent[0])
                    session.add(restaurant)
                    session.commit()

                    self.send_response(302)
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Add a new Restaurant</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                    output += "</br>"
                    output += "<p>Restaurant already added to the db</p>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output

            if self.path.endswith("/edit"):
                
                #Obtain the id of the restaurant
                restId = self.path.split("/")[2]

                edit_restaurant = session.query(Restaurant).filter_by(id = restId).first()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('message')

                    #Check if the restaurant is already on the db
                    checked_restaurant = session.query(Restaurant).filter_by(name = messagecontent[0]).first()

                    if(checked_restaurant == None):

                        session.query(Restaurant).filter_by(id = restId).update({"name":messagecontent[0]})
                        session.commit()

                        self.send_response(302)
                        self.send_header('Location','/restaurants')
                        self.end_headers()
                    
                    else:
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.end_headers()

                        output = ""
                        output += "<html><body>"
                        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/"+str(restId)+"/edit'><h2>Rename "+edit_restaurant.name+"</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                        output += "</br>"
                        output += "<p>Restaurant already added to the db</p>"
                        output += "</body></html>"
                        self.wfile.write(output)
                        print output

            else:
                self.send_error(404, 'File Not Found: %s' % self.path)

        except:
            pass
    


def main():
    try:
        port = 8080
        server = HTTPServer(('',port),WebServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
