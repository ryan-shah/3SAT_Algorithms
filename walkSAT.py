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

def walkSat(set):
	global solved
	global flips
	global max

	lastVar = 0
	repeat = 0
	totalReps = 0
	currFlips = 0
	#find solved and unsolved clauses
	while repeat < 3 or currFlips < 10000:
		if currFlips > 10000 and repeat < 3:
			flips = flips + currFlips
			currFlips = 0
			repeat = repeat +1
			genRandVars()

		good = []
		bad = []
		for clause in set:
			if isSolved(clause, solved):
				good.append(copy.deepcopy(clause))
			else:
				bad.append(copy.deepcopy(clause))
		if len(bad) == 0:
			flips = flips + currFlips
			return "SATISFIABLE"
		elif len(good) > max:
			max = len(good)
		#randomly pick bad clause
		x = random.randint(0, len(bad)-1)
		badC = copy.deepcopy(bad[x])
		#30% chance of rand var
		y = random.randint(0,9)
		if y < 3:
			z = badC[random.randint(0, len(badC) -1)]
			solved[abs(z)] = solved[abs(z)] * -1
			currFlips = currFlips+1
		else:
			#pick var in clause that ruins the fewest good clauses
			lowRuined = -1
			lowVar = 0
			for var in badC:
				tempSolved = copy.deepcopy(solved)
				#flip var
				tempSolved[abs(var)] = tempSolved[abs(var)] * -1
				count = 0
				#count ruined clauses
				for clause in good:
					if not isSolved(clause, tempSolved):
						count = count +1
				#if new low, set
				if count < lowRuined or lowRuined == -1:
					lowRuined = count
					lowVar = abs(var)
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
	done = walkSat(copy.deepcopy(SAT))
	print("c", flips)
	if done == "SATISFIABLE":
		print("s", done)
		res = "v"
		for i in solved:
			res = res + " " + str(i * solved[i])
		print(res)
	else:
		count = 0
		print("c", max, "clauses satisfied")
		print("v", done)

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
