import argparse
from copy import deepcopy
import sys
import math
import time

start = time.time()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('inputFile',
                   help='the randTSP file to import.  each city must be on its own line, consisting of a name, x quardinate, and y quardinate seperated by spaces')

#This is for easy exporting to excel to create the plots
parser.add_argument('-r','--raw', action="store_true",
                   help='only outputs final length')

parser.add_argument('-t','--time', action="store_true",
                   help='only outputs time it took to complete')

parser.add_argument('-n','--nodes', action="store_true",
                   help='only outputs the number of nodes created')

args = parser.parse_args()

F = open(args.inputFile)

#keeps track of the number of states
numNodes = 0

#setup empty city list
path = []
cities = []

class city:
	name = "_";
	x = 0
	y = 0

class stateClass:
	g = 0
	h = 0
	goal = False
	def __init__(self,cities,paths):
		self.cities = cities
		self.path = paths


#import cities
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
  	cities.append(newCity)


F.close()


#start the path at A
path.append(cities[0])
cities.remove(cities[0])

initalState = stateClass(cities,path)
initalState.g = 0


stateList = []
stateList.append(initalState)


def distance(city1, city2):
	return math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

def printPath(path):
	for city in path:
		print(city.name)


def newCopyOfState(state):
	newState = stateClass
	newState.g = state.g
	newState.h = state.h
	newState.cities = deepcopy(state.cities)
	newState.path = deepcopy(state.path)
	return newState


#stores the upper bound, which will also be the shortest path found so far
upperCost = 999999
upperState = None


def sort(state):
	#sorting by the huristic slowed things down fractionally.
	#sorting implies that we will find lower bounds faster, so that we can ignore more branches
	return state.g #+ state.h

#the recursive function
def compute(state):
	global stateList
	global start
	global args
	global upperCost
	global upperState
	global numNodes


	if state.g > upperCost:
		#This will usually not be reached, because we prune these out before they are made
		return

	#add to tge number of states
	numNodes += 1

	if len(state.cities) < 1:
		#a new upper bound is found
		if state.g < upperCost:
			upperCost = state.g
			upperState = state
		return

	#check for timeout
	current = time.time()
	if current - start >=300:
		print("timeout... current length: " + str(upperCost))
		printPath(upperState.path)
		sys.exit()

	stateList = []

	#test all possible next cities
	for c in range(len(state.cities)):
		#although a state is temporarily created, it is really check feasibility, and may get destroyed later.
		#i wont count this as a new state (yet) because it is really just a temporary variable holder
		oldDist = distance(state.path[-1],state.path[0])
		newState = stateClass(state.cities[:],state.path[:])
		newState.g = state.g
		newState.h = 0
		newState.path.append(newState.cities[c])
		newState.cities.remove(newState.cities[c])
		#we remove the path from the last city to the first city (which created a cycle)
		fakeDist =  distance(newState.path[-1], newState.path[0])
		#recalculate the new cyclic length
		newDist = distance(newState.path[-2], newState.path[-1]) + fakeDist
		#this represents the cost of this path
		newState.g += newDist - oldDist

		#our heuristic.  its the distance to the farthest, un-connected city from both the last node and the first node
		#we know that this will always be less than or equal to the real distance because we have to connect that node somehow
		#the shortest possible way is if it was the last node left to connect and so we directly connect it to both te first and last node
		#to complete the cycle... and that distacne is exactly what the heuristic calculates
		maxDist = fakeDist
		to = None
		for r in newState.cities:
			d = distance(newState.path[-1],r) + distance(r,newState.path[0])
			if d > maxDist:
				maxDist = d
				to = r

		#This will always be positive
		newState.h = maxDist - fakeDist

		#if our huristic causes a cost over the upperBound, then we know that this course of action is perilious
		if upperCost >= newState.g: # + newState.h:
			stateList.append(newState)


	#sort by the current cost
	stateList.sort(key = sort)


	#recurse over all states
	for s in stateList:
		compute(s)

#start recursion
compute(initalState)

#print, depending on flags
if args.time:
	print(time.time() - start)
elif args.raw:
	print(upperState.g)
elif args.nodes:
	print(numNodes)
else:
	printPath(upperState.path)
	print("Solution: " + str(upperState.g) + " in time " + str(time.time() - start))












"""


class cell():
	value = 0

#convert board to a series of cells
for i in range(9):
	for j in range(9):
		newcell = cell()
		newcell.value = ord(board[i][j]) - 48
		board[i][j] = newcell

def printBoard(board):
	for i in range(9):
		for j in range(9):
			print(board[i][j].value, end=' ')
		print()

#This checks if the move of val at i,j on the board would be legal
#if any conflict is found, return false, otherwise return true
def isLegal(val,i,j,board):
	#looks for a vertical conflict
	for ci in range(9):
		if i != ci and board[ci][j].value == val:
			return False
	#looks for a horizontal conflict
	for cj in range(9):
		if j != cj and board[i][cj].value == val:
			return False
	#determines the sub-square that i,j is in
	seci = int(i/3)
	secj = int(j/3)
	#determines sub-square conflicts
	for subi in range(seci*3,seci*3+3):
		for subj in range(secj*3,secj*3+3):
			if not(i==subi and j==subi) and board[subi][subj].value == val:
				return False
	return True


#Recursive function that traverses the search space
#returns true if a legal filled version of the board has been found
def compute(board,depth):
	global stepNumber
	stepNumber += 1
	if stepNumber == 10000:
		print("10,000 steps...quiting")
		sys.exit()
	#makes the copy of the board to work with
	newboard = deepcopy(board)
	fail = True
	#traverse the board until the first empty cell is found
	for i in range(9):
		for j in range(9):
			if newboard[i][j].value == 0:
				#try all values on the cell
				for k in range(1,10):
					#if the move is legal, the move is made and we compute on the coresponding board
					if isLegal(k,i,j,newboard):
						newboard[i][j].value = k
						tempboard, fail = compute(newboard,depth + 1)
						if fail == False:
							#apparenly a valid configuration was found in thie branch, pass it up to the parent
							return tempboard, fail
				#all values were tested, none of which led to a valid configuration
				#we are therefore in the wrong branch
				return newboard, fail
	#the board is filled!  we have found a valid configuration
	return board, False


#start recursion
board, fail = compute(board,0)

#output findings
if args.raw:
	if fail:
		print("err")
	else:
		print(str(stepNumber))
else:
	if fail:
		print("No valid configurations (" + str(stepNumber) + " steps)")
	else:
		printBoard(board)
		print(str(stepNumber) + " steps")"""
