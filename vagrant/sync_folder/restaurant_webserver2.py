import cgi
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

#import libraries and modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#create and connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    """ class defined in the main method"""

    def do_GET(self):
        try:
            #look for url then ends with '/hello'
            if self.path.endswith("/restaurants"):
                self.send_response(200)

                #indicate reply in form of html to the client
                self.send_header('Content-type', 'text/html')

                #indicates end of https headers in the response
                self.end_headers()

                #obtain all restaurant names from databse
                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body><a href='/restaurants/new'>Add A New Restaurant</a>"
                output += "</br></br>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += """<div>
                            <a href='#'>Edit</a>
                            <a href='#'>Delete</a>
                            </div>"""
                    output += "</br></br>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return


            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Add New Restaurant</h1>"

                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurant' type='text' placeholder='New Restaurant Name'>"
                output += "<input name='Create' type='submit' label='Create'>"
                output += "</form></body></html>"

                self.wfile.write(output)
                return

        except IOError:

            self.send_error(404, "File %s not found" % self.path)



    def do_POST(self):

        try:

            if self.path.endswith("/restaurants/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

                print ctype

                #check of content-type is form
                if (ctype == 'multipart/form-data') or (ctype == 'application/x-www-form-urlencoded'):

                    #collect all fields from form, fields is a dictionary
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                    else:
                        content_length = self.headers.getheaders('Content-length')
                        length = int(content_length[0])
                        body = self.rfile.read(length)
                        fields = urlparse.parse_qs(body)

                    #extract the name of the restaurant from the form
                    messagecontent = fields.get('newRestaurant')

                    #create the new object
                    newRestaurantName = Restaurant(name = messagecontent[0])
                    session.add(newRestaurantName)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                    return

        except:
            pass




def main():
    """An instance of HTTPServer is created in the main method 
    HTTPServer is built off of a TCP server indicating the 
    transmission protocol
    """
    try:
        port = 8080

        #server address is tuple & contains host and port number
        #host is an empty string in this case
        server = HTTPServer(('', port), webServerHandler)


        print "Web server running on port %s"  % port

        #keep server continually listening until interrupt occurs
        server.serve_forever()


    except KeyboardInterrupt:
        print "^C entered, stopping web server...."

        #shut down server
        server.socket.close()


#run main method
if __name__ == '__main__':
    main()