import sys
import copy
import os
import random

SAT = []
solved = {}
seed = 0
clauses = 0
vars = 0
flips = 0
max = 0

# var.clause.seed.cnf
def setSeed(file):
	global seed
	parts = file.split('.')
	seed = int(parts[2])

def parseInput(file):
	global vars
	global clauses
	with open(file) as f:
		for line in f:
			if line.startswith('c'):
				pass
			elif line.startswith('p'):
				l = line.split(' ')
				vars = int(l[2])
				clauses = int(l[3])
			else:
				clause = []
				chars = line.split(' ')
				for c in chars:
					if c != '0\n' and c != '':
						clause.append(int(c))
				SAT.append(clause)

def isSolved(clause, sol):
	for i in range(0, len(clause)):
		if clause[i] == (abs(clause[i]) * sol[abs(clause[i])]):
			return True
	return False

def gSat(set):
	global solved
	global flips
	global max

	lastVar = 0
	repeat = 0
	totalReps = 0
	currFlips = 0
	#find solved and unsolved clauses
	while repeat < 3 or currFlips < 10000:
		if repeat < 3 and currFlips > 10000:
		#	print("resetting")
			repeat = repeat + 1
			flips = flips + currFlips
			currFlips = 0
			genRandVars()
		lowVar = 1
		lowCount = -1
		badCount = 0
		for clause in set:
			if not isSolved(clause, solved):
				badCount = badCount + 1
		if badCount == 0:
			flips = flips + currFlips
			return "SATISFIABLE"
		elif (len(set) - badCount) > max:
			max = (len(set) - badCount)
		for i in range(1, vars+1):
			tempSolve = copy.deepcopy(solved)
			tempSolve[i] = tempSolve[i] * -1
			tempCount = 0
			for clause in set:
				if not isSolved(clause, tempSolve):
					tempCount = tempCount + 1
			if tempCount < lowCount or lowCount == -1:
				lowCount = tempCount
				lowVar = i
		#set solved to have best flipped var
		#print("switching", lowVar)
		solved[lowVar] = solved[lowVar] * -1
		currFlips = currFlips + 1
	return "UNKNOWN"

def genRandVars():
	global vars
	global solved
	#randomly assign vars
	for i in range(0, vars):
		x = random.randint(0,1)
		if x == 0:
			solved[i+1] = -1
		else:
			solved[i+1] = 1


def func(file):
	global SAT
	global solved
	global flips
	global max

	SAT = []
	solved = {}
	flips = 0
	max = 0

	if not file.endswith(".cnf"):
		return
	print("c testing file:", file)
	parseInput(file)
	setSeed(file)
	random.seed(seed)
	genRandVars()
	done = gSat(copy.deepcopy(SAT))
	print("c", flips)
	if done == "SATISFIABLE":
		print("s", done)
		res = "v"
		for i in solved:
			res = res + " " + str(i * solved[i])
		print(res)
	else:
		print('c', max, "clauses satisfied")
		print('v', done)


if len(sys.argv) < 2:
	print("usage: python satSolver.py <filename or dirname>")
	quit()

if(os.path.isdir(sys.argv[1])):
	for file in os.listdir(sys.argv[1]):
		func(os.path.join(sys.argv[1],file))
elif os.path.isfile(sys.argv[1]):
	func(sys.argv[1])
else:
	print("file/folder read error")
