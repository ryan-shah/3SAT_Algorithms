import sys
import copy
import os

SAT = []
solved = {}

def parseInput(file):
	with open(file) as f:
		for line in f:
			if line.startswith('c'):
				pass
			elif line.startswith('p'):
				pass
			else:
				clause = []
				chars = line.split(' ')
				for c in chars:
					if c != '0\n' and c != '':
						clause.append(int(c))
				SAT.append(clause)

def trimSet(set, item):
	index = 0
	#unit propogation
	while (index != len(set)):
		toRemove = False
		for it in set[index]:
			#if found the item whole clause is true
			if it == item:
				toRemove = True
				break
			#if found -item, remove that item
			elif it == (-1*item):
				set[index].remove(it)
		if toRemove:
			set.pop(index)
			index = index -1
		index = index+1

def assignVar(item):
#	print("assigning", item)
#	input()
	if item < 0:
		solved[item * -1] = -1
	else:
		solved[item] = 1

def DPLL(set):
	global solved
	#all clauses satisfied
	if(len(set) == 0):
		return "SATISFIABLE"
	#empty clause, so unsatisfiable
	for clause in set:
		if(len(clause) == 0):
			return "UNSATISFIABLE"
	global solved
	#check for unit clauses
	index = 0
	for clause in set:
		#if clause only has 1 variable
		if(len(clause) == 1):
			item = clause[0]
			#assign the variable to true or false
			#if its a not then false
			assignVar(item)
			#remove from set
			set.pop(index)
			trimSet(set, item)
			#continue DPLL
			return DPLL(copy.deepcopy(set))
		index = index + 1
	#no unit clauses, find shortest
	shortClause = set[0]
	for clause in set:
		if len(clause) < len(shortClause):
			shortClause = clause
	#pick an item to test on
	item = shortClause[0]
	#make copy of set
	tempSet = copy.deepcopy(set)
	#remove shortest clause (were assigning item as true)
	tempSet.remove(shortClause)
	#unit propogation
	trimSet(tempSet, item)
	#make backup of solutions
	tempSolve = copy.deepcopy(solved)
	#check solution
	done = DPLL(tempSet)
	#if it worked assign item as true & return
	if done == "SATISFIABLE":
		assignVar(item)
		return done
	#else item is false. reset to previous state
	else:
		solved = copy.deepcopy(tempSolve)
		item = item * -1
		tempSet = copy.deepcopy(set)
		#unit propogation
		trimSet(tempSet, item)
		assignVar(item)
	#continue DPLL on tempSet
	return DPLL(tempSet)

def func(file):
	global SAT
	global solved

	SAT = []
	solved = {}


	if not file.endswith(".cnf"):
		return
	print("c testing file:", file)
	parseInput(file)
	done = DPLL(copy.deepcopy(SAT))
	if done == "SATISFIABLE":
		print("s", done)
		res = "v"
		for i in solved:
			res = res + " " + str(i * solved[i])
		print(res)
	else:
		print(done)


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
