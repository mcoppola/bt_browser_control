# bt server and extremely basic browser driver implementation
# opens a webpage and allows user to scroll up or down from client

from bluetooth import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys, json, math

class MyScrollDecoder(json.JSONDecoder):

	def __init__(self, client_height):
		json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)
		self.client_height = client_height

	def dict_to_object(self, d):
		if 'y' in d:
			y = int(math.floor(float(d.pop('y'))))
			if (y > self.client_height/2):
				self.down = True
			else:
				self.down = False
		return self

class MyWindowDecoder(json.JSONDecoder):

	def __init__(self):
		json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

	def dict_to_object(self, d):
		if 'width' in d:
			self.width = int(math.floor(float(d.pop('width'))))
			self.height = int(math.floor(float(d.pop('height'))))
		return self

# init bluetooth server
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",22))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                   protocols = [ OBEX_UUID ] 
                    )
                
# Wait for client connection
print "Waiting for connection on RFCOMM channel %d" % port
client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info

# get client screen dimentions in first message
windowData = client_sock.recv(1024)
clientWindow = MyWindowDecoder().decode(windowData)
print 'Opening Browser...'

# start browser
browser = webdriver.Firefox()
browser.get('http://nytimes.com/')
print 'Ready to receive'

# accept loop
try:
	while True:

		data = client_sock.recv(1024)
		if len(data) == 0: break
		print "received [%s]" % data
		# parse JSON to get up or down command
		scroll = MyScrollDecoder(clientWindow.height).decode(data)
		if (scroll.down):
			browser.execute_script("window.scrollBy(0,100)")
		else:
			browser.execute_script("window.scrollBy(0, -100)")
except Exception, e:
	print e