import argparse
from copy import deepcopy
import math
import time
import sys

start = time.time()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputFile',
                   help='the randTSP file to import.  each city must be on its own line, consisting of a name, x quardinate, and y quardinate seperated by spaces')
#This is for easy exporting to excel to create the plots
parser.add_argument('-r','--raw', action="store_true",
                   help='only outputs the number of steps')

args = parser.parse_args()


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


class road:
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
	#def findDirection(self, old):


cityList = []
roadList = []


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
  	cityList.append(newCity)


F.close()

minimum = 0

for i in range(len(cityList) - 1):
	newRoad = road()
	newRoad.cities.append(cityList[i])
	newRoad.cities.append(cityList[i + 1])
	cityList[i].roads.append(newRoad)
	cityList[i + 1].roads.append(newRoad)
	newRoad.dist = math.sqrt((cityList[i].x - cityList[i + 1].x)**2 + (cityList[i].y - cityList[i + 1].y)**2)
	#cityList[i].to = cityList[i + 1]
	#cityList[i].diTo = math.sqrt((cityList[i].x - cityList[i + 1].x)**2 + (cityList[i].y - cityList[i + 1].y)**2)
	minimum += newRoad.dist
	roadList.append(newRoad)
	print()
	#print(cityList[i].diTo)


newRoad = road()
newRoad.cities.append(cityList[-1])
newRoad.cities.append(cityList[0])
cityList[-1].roads.append(newRoad)
cityList[0].roads.append(newRoad)
newRoad.dist = math.sqrt((cityList[-1].x - cityList[0].x)**2 + (cityList[-1].y - cityList[0].y)**2)
minimum += newRoad.dist
roadList.append(newRoad)

#cityList[-1].to = cityList[0]
#cityList[-1].diTo = math.sqrt((cityList[-1].x - cityList[0].x)**2 + (cityList[-1].y - cityList[0].y)**2)
#minimum += cityList[-1].diTo

#for c in cityList:
#	print(str(c) + "  ->  " + str(c.to))
print(minimum)



def printGraph(cities, roads):
	#print(cities[0].name)
	lastCity = cities[0]
	firstCity = cities[0]
	lastRoad = lastCity.roads[0]
	print(lastCity.name)
	length = 1
	cost = lastRoad.dist
	while True:
		#print("::" + str(lastCity) + " c-r " + str(lastRoad))
		#print("::" + str(lastCity.roads) + " r-c " + str(lastRoad.cities))
		lastCity = lastRoad.notCity(lastCity)
		lastRoad = lastCity.notRoad(lastRoad)
		print(lastCity.name)
		length += 1
		
		if lastCity == firstCity:
			"""if length < 10:
				print("error!!!")
				sys.exit()"""
			print("COST: " + str(cost))
			break
		cost += lastRoad.dist
		#lastRoad = lastCity
		#print(lastCity)
		#print(r.notCity(lastCity).name)
		#lastCity = r.notCity(lastCity)
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

def matchRoad(r1,r2):
	for a in r1.cities:
		for b in r2.cities:
			if a == b:
				return False
	return True

def sortDist(c):
	return c.Dist

def startCompute(cities,roads,length):
	global start
	count = 0
	while True:
		current = time.time()
		if current - start >=30:
			print("timeout... current minimum: " + str(length))
			printGraph(cities,roads)
			sys.exit()
		found = False
		

		length, found= compute(cities,roads,length)
		count += 1
		"""if count > 3:
			print("count3")
			found = False
		"""

		if found == False:
			print("found: " + str(length) + " in time: " + str(time.time() - start))
			printGraph(cities, roads)
			sys.exit()


def compute(cities,roads,length):
	#print("AHHHH")
	#for a in graph:
	#	print(a.name)
	
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
					printGraph(cities,roads)
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
	return length, False

		
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
	global minimum
	if len(left) == 0:
		length += math.sqrt((order[-1].x - order[0].x)**2 + (order[-1].y - order[0].y)**2)
		order.append(order[0])
		if length < minimum:
			print(length)
			for c in order:
				print(c.name)
			print()
			minimum = length
			optimumOrder = deepcopy(order)
	current = time.time()
	global start
	if current - start >=300:
		print("timeout... current minimum: " + str(minimum))
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
#order.append(cityList[0])
#cityList.pop(0)
#compute(order, cityList, 0)
printGraph(cityList, roadList)
print(":::")
startCompute(cityList, roadList, minimum)

print("Minimum distance: " + str(minimum) + " in time: " + str(time.time() - start))

for c in optimumOrder:
	print(c.name)