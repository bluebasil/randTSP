import argparse
from copy import deepcopy
import math
import time
import sys
from tkinter import *

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def _draw_point(self, x, y):
	return None#canvas.create_circle(x, y, 5, fill="#FFF")

def _create_line(self, x1, y1, x2, y2):
	return canvas.create_line(x1, y1, x2, y2, fill="#FFF")

def _create_text(self, x, y, text):
	return canvas.create_text(x, y, fill="#F55", text=text)

start = time.time()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputFile',
                   help='the randTSP file to import.  each city must be on its own line, consisting of a name, x quardinate, and y quardinate seperated by spaces')
#This is for easy exporting to excel to create the plots
parser.add_argument('-r','--raw', action="store_true",
                   help='only outputs the number of steps')

args = parser.parse_args()

canvas = None
root = None


class city:
	name = "_";
	x = 0
	y = 0
	potentailDist = 0
	def __init__(self):
		self.roads = []
	def replace(self,old,new):
		if self.roads.count(old) > 0:
			self.roads.remove(old)
			self.roads.append(new)
		else:
			print("err")
	def notRoad(self, road):
		if(self.roads[0] == road):
			return self.roads[1]
		else:
			return self.roads[0]


"""class road:
	dist = 0
	direction = True
	def __init__(self):
		self.cities = []
	def replace(self,old,new):
		if self.cities.count(old) > 0:
			self.cities.remove(old)
			self.cities.append(new)
		else:
			print("err")
	def notCity(self, city):
		if(self.cities[0] == city):
			self.direction = True
			return self.cities[1]
		else:
			self.direction = False
			return self.cities[0]
	#def findDirection(self, old):"""


cities = []
allCities = []
#roads = []


F = open(args.inputFile)

#import cities
i=0
for line in F:
  tempStr = line.split()
  if len(tempStr) > 1:
  	newCity = city()
  	newCity.name = tempStr[0]
  	newCity.x = int(tempStr[1])
  	newCity.y = int(tempStr[2])
  	allCities.append(newCity)


F.close()

length = 0

cities.append(allCities[0])
allCities.remove(cities[0])

"""for i in range(len(cities) - 1):
	newRoad = road()
	newRoad.cities.append(cities[i])
	newRoad.cities.append(cities[i + 1])
	cities[i].roads.append(newRoad)
	cities[i + 1].roads.append(newRoad)
	newRoad.dist = math.sqrt((cities[i].x - cities[i + 1].x)**2 + (cities[i].y - cities[i + 1].y)**2)
	#cities[i].to = cities[i + 1]
	#cities[i].diTo = math.sqrt((cities[i].x - cities[i + 1].x)**2 + (cities[i].y - cities[i + 1].y)**2)
	length += newRoad.dist
	roads.append(newRoad)
	print()
	#print(cities[i].diTo)


newRoad = road()
newRoad.cities.append(cities[-1])
newRoad.cities.append(cities[0])
cities[-1].roads.append(newRoad)
cities[0].roads.append(newRoad)
newRoad.dist = math.sqrt((cities[-1].x - cities[0].x)**2 + (cities[-1].y - cities[0].y)**2)
length += newRoad.dist
roads.append(newRoad)"""

#cities[-1].to = cities[0]
#cities[-1].diTo = math.sqrt((cities[-1].x - cities[0].x)**2 + (cities[-1].y - cities[0].y)**2)
#length += cities[-1].diTo

#for c in cities:
#	print(str(c) + "  ->  " + str(c.to))
print(length)



def printGraph(cities, allCities):#, roads):
	length = 0
	lastCity = None
	scale = 10
	canvas.delete(ALL)
	for c in cities:
		if lastCity != None:
			length += math.sqrt((c.x - lastCity.x)**2 + (c.y - lastCity.y)**2)
			canvas.create_ln(c.x * scale, c.y * scale,lastCity.x * scale,lastCity.y * scale)

		print(c.name)
		canvas.draw_text(c.x * scale,c.y * scale, c.name)
		lastCity = c
	length += math.sqrt((cities[0].x - lastCity.x)**2 + (cities[0].y - lastCity.y)**2)
	canvas.create_ln(cities[0].x * scale, cities[0].y * scale,lastCity.x * scale,lastCity.y * scale)
	print("COst: " + str(length))

	for c in allCities:
		canvas.draw_text(c.x * scale,c.y * scale, c.name)


	"""
	#print(cities[0].name)
	lastCity = cities[0]
	firstCity = cities[0]
	lastRoad = lastCity.roads[0]
	print(lastCity.name)
	length = 1
	cost = lastRoad.dist

	scale = 10

	canvas.delete(ALL)
	canvas.create_point(lastCity.x * scale,lastCity.y * scale)
	canvas.create_ln(lastRoad.cities[0].x * scale, lastRoad.cities[0].y * scale,lastRoad.cities[1].x * scale,lastRoad.cities[1].y * scale)
	canvas.draw_text(lastCity.x * scale,lastCity.y * scale, lastCity.name)
	while True:
		#print("::" + str(lastCity) + " c-r " + str(lastRoad))
		#print("::" + str(lastCity.roads) + " r-c " + str(lastRoad.cities))
		actualLast = lastCity
		lastCity = lastRoad.notCity(lastCity)
		lastRoad = lastCity.notRoad(lastRoad)


		canvas.create_ln(lastRoad.cities[0].x * scale, lastRoad.cities[0].y * scale,lastRoad.cities[1].x * scale,lastRoad.cities[1].y * scale)
		canvas.create_point(lastCity.x * scale,lastCity.y * scale)
		canvas.draw_text(lastCity.x * scale,lastCity.y * scale, lastCity.name)
		print(lastCity.name)
		length += 1
		
		if lastCity == firstCity:
			print("COST: " + str(cost))
			break
		cost += lastRoad.dist
		#lastRoad = lastCity
		#print(lastCity)
		#print(r.notCity(lastCity).name)
		#lastCity = r.notCity(lastCity)"""
"""
	cur = graph[0]
	start = cur.name
	i=0
	while True:
		i+=1
		print(cur.name)
		cur = cur.to
		if cur.name == start:
			print(cur.name)
			break
		if i>20:
			for c in graph:
				print(str(c) + "  ->  " + str(c.to))
			break
"""
"""
def matchRoad(r1,r2):
	for a in r1.cities:
		for b in r2.cities:
			if a == b:
				return False
	return True"""

def sortDist(c):
	global cities

	return c.Dist

def startCompute():
	global start
	global cities
	global allCities
	global length
	if True:
		current = time.time()
		if current - start >=30:
			print("timeout... current length: " + str(length))
			printGraph(cities, allCities)#,roads)
			sys.exit()
		found = False
		

		found = compute(cities,allCities)
		#count += 1
		"""if count > 3:
			print("count3")
			found = False
		"""

		if found == True:
			print("found: " + str(length) + " in time: " + str(time.time() - start))
			printGraph(cities, allCities)#, roads)
			root.mainloop()
			sys.exit()

	root.after(1000, startCompute)


def compute(cities,allCities):
	#print("AHHHH")
	#for a in graph:
	#	print(a.name)
	minDist = 9999
	minA = None
	minC = -1
	if len(allCities) < 1:
		return True

	for a in allCities:
		for c in range(len(cities)):
			curDist = math.sqrt((cities[c].x - a.x)**2 + (cities[c].y - a.y)**2)
			print(a.name + " curDist: " + str(curDist))
			if curDist < minDist:
				minDist = curDist
				minA = a
				minC = c
	print("chose: " + minA.name + " with " + cities[minC].name + " at dist: " + str(minDist))
	#should always have something
	if len(cities) > 2:
		bef = minC - 1
		aft = minC + 1
		cur = cities[minC]
		if c == 0:
			print("start")
			bef = len(cities) - 1
			aft = 1
		elif minC == len(cities) - 1:
			

			bef	= len(cities) - 2
			aft = 0
			print("end: " + str(len(cities)))
		print("me: " + cities[minC].name + " bef: " + cities[bef].name + " aft:" + cities[aft].name)
		befDist = math.sqrt((cities[bef].x - minA.x)**2 + (cities[bef].y - minA.y)**2)
		aftDist = math.sqrt((cities[aft].x - minA.x)**2 + (cities[aft].y - minA.y)**2)

		if befDist < aftDist:
			print("ChoseBef:" + cities[bef].name)
			cities.insert(minC,minA)
		else:
			print("ChoseAft:" + cities[aft].name)
			cities.insert(aft,minA)
	else:
		cities.append(minA)
	allCities.remove(minA)
	printGraph(cities, allCities)
	return False


"""
	
	for a in roads:
		for b in roads:
			if matchRoad(a,b):
				afirst = 0
				asec = 1
				bfirst = 0
				bsec = 1
				di = "forward"
				if a.direction != b.direction:
					bfirst  = 1
					bsec = 0
					di = "backward"

				newDist1 = math.sqrt((a.cities[0].x - b.cities[bfirst].x)**2 + (a.cities[0].y - b.cities[bfirst].y)**2)
				newDist2 = math.sqrt((a.cities[1].x - b.cities[bsec].x)**2 + (a.cities[1].y - b.cities[bsec].y)**2)

				if newDist1 + newDist2 < a.dist + b.dist:
					#printGraph(cities,roads)
					print(di + ":" + str(length) + "=l :: new= " + str(newDist1 + newDist2) + " old=" + str(a.dist + b.dist))
					print(str(a.cities[0].name) + "-" + str(a.cities[1].name) + ", " + str(b.cities[bfirst].name) + "-" + str(b.cities[bsec].name) + " :TO-> " + str(a.cities[0].name) + "-" + str(b.cities[bfirst].name) + ", " + str(a.cities[1].name) + "-" + str(b.cities[bsec].name))
					length = length - a.dist - b.dist + newDist1 + newDist2
					a.cities[1].replace(a,b)
					b.cities[bfirst].replace(b,a)
					temp = a.cities[1]
					a.replace(a.cities[1],b.cities[bfirst])
					b.replace(b.cities[bfirst],temp)
					a.dist = newDist1
					b.dist = newDist2
					printGraph(cities,roads)
					print(":::::")
					
					return length, True
						#compute(cities,roads,newLength)
	return length, False"""

		
"""
	for a in range(len(graph)):
		for b in range(len(graph)):
			c = graph[a]
			d = graph[b]
			#print(c.to != d)
			if a != b and c.to != d and d.to != c:
				
				

				cd = math.sqrt((c.x - d.x)**2 + (c.y - c.y)**2)
				cto = c.to
				dto = d.to
				#print(str(cto) + " :: " + str(dto))
				ctodto = math.sqrt((cto.x - dto.x)**2 + (cto.y - dto.y)**2) 
				if cd + ctodto < c.diTo + d.diTo:
					print(c.name + " and " + d.name )
					#print("cd + stodto: " + str(cd + ctodto) + "  c.dito + d.dito: " + str(c.diTo + d.diTo))
					#print(c.diTo + d.diTo - (cd + ctodto))
					minusLen = c.diTo + d.diTo
					newGraph = deepcopy(graph)

					#for x in newGraph:
					#	print(str(x) + "  ->  " + str(x.to) + " c:" + str(c) + " d:" + str(d))


					c = newGraph[a]
					d = newGraph[b]
					temp1 = c.to
					temp2 = d.to
					c.to = d
					c.diTo = cd




					c.to = d
					
					d.to = temp
					d.diTo = ctodto

					#for x in newGraph:
					#	print(str(x) + "  ->  " + str(x.to) + " c:" + str(c) + " d:" + str(d))

					compute(newGraph,length - minusLen + cd + ctodto)
"""
	







"""def compute(order, left, length):
	global length
	if len(left) == 0:
		length += math.sqrt((order[-1].x - order[0].x)**2 + (order[-1].y - order[0].y)**2)
		order.append(order[0])
		if length < length:
			print(length)
			for c in order:
				print(c.name)
			print()
			length = length
			optimumOrder = deepcopy(order)
	current = time.time()
	global start
	if current - start >=300:
		print("timeout... current length: " + str(length))
		sys.exit()

	for c in left:
		c.curDist = math.sqrt((order[-1].x - c.x)**2 + (order[-1].y - c.y)**2)

	left.sort(key = sortDist)

	for c in left:
		newOrder = order[:]
		newOrder.append(c)
		newLeft = left[:]
		newLeft.remove(c)
		partLength = c.curDist
		compute(newOrder,newLeft,length + partLength)

"""


#order = []
#left = []
#order.append(cities[0])
#cities.pop(0)
#compute(order, cities, 0)

def main():
	global canvas
	global root
	root = Tk()
	canvas = Canvas(root, width=1000, height=1000, borderwidth=0, highlightthickness=0, bg="black")
	canvas.grid()


	Canvas.create_circle = _create_circle

	Canvas.create_ln = _create_line
	Canvas.create_point = _draw_point
	Canvas.draw_text = _create_text

	root.wm_title("n Planetary Simulator")


	"""
	random.seed()
	for x in range(0, 500):
		pl = Planet()
		pl.ox = random.uniform(-maxX, maxX)
		pl.oy = random.uniform(-maxX, maxX)
		pl.surface = random.uniform(minSurf, maxSurf)
		pl.mass = random.uniform(minMass(pl.surface), maxMass(pl.surface))
		pl.fill = "#" + toHex(int(random.uniform(0,15))) + toHex(int(random.uniform(0,15))) + toHex(int(random.uniform(0,15)))
		planArr.append(pl)
	"""


	"""global p
	p = Pool(processes=1)  """

	root.after(1000, startCompute)
	root.mainloop()



if __name__ == '__main__':
    main()
"""

root = Tk()
canvas = Canvas(root, width=1000, height=1000, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()

Canvas.create_line = _draw_line
Canvas.create_point = _draw_point

root.wm_title("n Planetary Simulator")



root.after(1, startCompute)

printGraph(cities, roads)
print(":::")
startCompute(cities, roads, length)

print("length distance: " + str(length) + " in time: " + str(time.time() - start))

for c in optimumOrder:
	print(c.name)"""