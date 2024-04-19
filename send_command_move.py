import Asserv

asserv =Asserv.Asserv()
while(1):
	x = int(input("x: "))
	y= int(input("y: "))
	asserv.goto(x,y)
