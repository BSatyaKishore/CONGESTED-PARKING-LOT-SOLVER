import sys

print '''(define (domain car_game)
(:predicates
   (left ?r1 ?r2) 
   (top ?c1 ?c2) 
   (same ?a ?b) 
   (is_horizontal ?car) 
   (is_vertical ?car) 
   (free ?r1 ?c1)
   (cars_1 ?car ?r1 ?c1)
   (goal_truth ?t_or_f)
   (driver_is ?out_or_in)
   (driver_in_car ?car)'''

for j in range(2,15):
	sumanth = '(cars_'+str(j)+' ?car' 
	for i in range(1,j+1):
   		sumanth += ' ?r'+str(i) +' ?c'+str(i)
	sumanth = sumanth +')'
	print '   '+sumanth
print ')'

driver_actions = '''(:action change_car
:parameters (?car_i ?car_f) 
:precondition (or (driver_in_car ?car_i) (driver_is out))
:effect (and  (not (driver_in_car ?car_i)) (driver_in_car ?car_f) (not (driver_is out)))
)
'''

def move_strips(towards,n): # n is car_length
	print "(:action move_"+towards+'_'+str(n)
	precondition = []
	effect = []

	# parameters
	stri = "?car"
	for i in range(1,n+1):
		stri =stri +' ?r'+str(i) +' ?c'+str(i)
	stri += ' ?to_r ?to_c'
	parameters = stri

	# pre-condition
	temp_str = 'cars_'+str(n)+' ?car'
	for i in range(1,n+1):
		temp_str = temp_str + ' ?r'+str(i)+' ?c'+str(i)
	precondition.append(temp_str)
	precondition.append("free ?to_r ?to_c")
	precondition.append("driver_in_car ?car")
	if towards == "left":
		precondition.append('left ?c1 ?to_c')
		precondition.append('same ?r1 ?to_r')
		precondition.append('is_horizontal ?car')
	elif towards == "right":
		temp_str1 = 'left ?to_c ?c'+str(n)
		precondition.append(temp_str1)
		precondition.append('same ?r1 ?to_r')
		precondition.append('is_horizontal ?car')
	elif towards == "top":
		precondition.append('top ?r1 ?to_r')
		precondition.append('same ?c1 ?to_c')
		precondition.append('is_vertical ?car')
	else:
		temp_str1 = 'top ?to_r ?r'+str(n)
		precondition.append(temp_str1)
		precondition.append('same ?c1 ?to_c')
		precondition.append('is_vertical ?car')

	effect.append('not ('+temp_str+')')

	if (towards == 'left') or (towards == 'top'):
		temp_str = 'cars_'+str(n)+' ?car ?to_r ?to_c'
		for i in range(1,n):
			temp_str += ' ?r' + str(i) + ' ?c'+str(i)
		effect.append(temp_str)
		effect.append('free ?r'+str(n) +' ?c'+str(n))
	else:
		temp_str = 'cars_'+str(n)+' ?car'
		for i in range(2,n+1):
			temp_str += ' ?r' + str(i) + ' ?c'+str(i)
		effect.append(temp_str+' ?to_r ?to_c')
		effect.append('free ?r1 ?c1')
	effect.append('not (free ?to_r ?to_c)')

	print ":parameters ("+parameters+") "
	print ":precondition (and ", 
	for i in precondition:
		print "(" + i + ")" ,
	print ")"
	print ":effect (and ", 
	for i in effect:
		print "(" + i + ")" ,
	print ")"
	print ")"

m_n = raw_input().split(' ')
no_of_cars = input()

board = []
hor_cars = []
ver_cars = []
occupied_squares = []
free_squares = []
same = []
left = []
top = []
car_length = [0]*no_of_cars

def print_board():
	for i in board:
		for j in i:
			print >> sys.stderr, j, '\t',
		print >> sys.stderr, ""

for i in range(int(m_n[0])):
	tem = []
	for j in range(int(m_n[1])):
		tem.append(0)
	board.append(tem)

cars = []
# 1 2 10 7 H
for i in range(no_of_cars):
	#print_board()
	inp = raw_input().split(' ')
	if inp[4] == 'H':
		hor_cars.append(int(inp[0]))
		car_length[int(inp[0])-1] = int(inp[1]) 
		temp = []
		for i in range(int(inp[1])):
			board[int(inp[3])-1][i-1+int(inp[2])] = int(inp[0])
			occupied_squares.append((int(inp[0]),(int(inp[3])-1),(i-1+int(inp[2]))))
			temp.append((int(inp[3]), i+int(inp[2])))
		cars.append((inp[0],inp[1], temp))
	else:
		ver_cars.append(int(inp[0]))
		car_length[int(inp[0])-1] = int(inp[1])
		temp = []
		for i in range(int(inp[1])):
			board[i+int(inp[3])-1][int(inp[2])-1] = int(inp[0])
			occupied_squares.append((int(inp[0]),(i + int(inp[3])-1),(int(inp[2])-1)))
			temp.append((i+int(inp[3]),inp[2]))
		cars.append((inp[0],inp[1], temp))

goal = raw_input().split(' ')

def goal_truth():
	if goal[1] is '1':          # or (goal[1] is str(m_n[1])):
		if 1 in ver_cars:
			print >> sys.stderr, '(goal_truth t)'
		else:
			print >> sys.stderr, '(goal_truth f)'
	if (goal[0] is '1') or (goal[0] is str(m_n[0])):
		if 1 in hor_cars:
			print >> sys.stderr, '(goal_truth t)'
		else:
			print >> sys.stderr, '(goal_truth f)'

def print_init():
	global left, top
	
	for i in hor_cars:
		print >> sys.stderr, "(is_horizontal car_"+str(i)+')',
	print >> sys.stderr, ''
	for i in ver_cars:
		print >> sys.stderr, "(is_vertical car_"+str(i)+')',
	print >> sys.stderr,  ''	
	# TO_DO: write 2 for loops
	for i in range(int(m_n[0])):
		for j in range(int(m_n[1])):
			if board[i][j] == 0:
				print >> sys.stderr, "(free r_"+str(i+1)+ " c_"+str(j+1)+')',
	print >> sys.stderr, ''
	# left
	for i in range(int(m_n[1])-1):
		print >> sys.stderr, '(left c_'+str(i+2)+' c_'+str(i+1)+')',
	print >> sys.stderr, ''
	# top
	for i in range(int(m_n[0])-1):
		print >> sys.stderr, '(top r_'+str(i+2)+' r_'+str(i+1)+')',
	print >> sys.stderr, ''
	# TODO: same function
	for i in range(int(m_n[0])): #,int(m_n[1]))):
		print >> sys.stderr, '(same r_'+str(i+1) + ' r_'+str(i+1)+')', #same.append((i,i))
	print >> sys.stderr, ''	
	for i in range(int(m_n[1])): #,int(m_n[1]))):
		print >> sys.stderr, '(same c_'+str(i+1) + ' c_'+str(i+1)+')', #same.append((i,i))
	print >> sys.stderr, ''
	# vertical goal and horizontal goal
	goal_truth()
	# cars
	for i in cars:
		tempo = 'cars_'+str(i[1]) + ' car_'+str(i[0])
		for k in i[2]:
			tempo = tempo + ' r_'+str(k[0]) + ' c_'+str(k[1])
		print  >> sys.stderr, '('+tempo+')',
	print  >> sys.stderr, '(driver_is out)'


def print_objects(m,n, car_count):
	for i in range(1,m):
		print >> sys.stderr, "r_"+str(i),
	print >> sys.stderr, "r_"+str(m),
	for i in range(1,n):
		print >> sys.stderr, "c_"+str(i),
	print >> sys.stderr, "c_"+str(n),
	for i in range(1,car_count):
		print >> sys.stderr, "car_"+str(i),
	print >> sys.stderr, "car_"+str(car_count),
	print >> sys.stderr, "t","f", "out", 

# (and (cars_2 car_1 r_1 c_3 r_2 c_3) (goal_truth t)) horizontal

def print_goal():
	print >> sys.stderr, "(and ",
	if goal[1] is '1':		# or str(m_n[1])):
		if 1 in ver_cars:
			string = "(cars_"+str(car_length[0])+" car_1"
			for i in range(1,car_length[0]+1):
				string = string + " r_"+str(i)+" c_"+goal[0]
			print >> sys.stderr, string+")",
	if goal[1] is str(m_n[1]):
		if 1 in ver_cars:
			string = "(cars_"+str(car_length[0])+" car_1"
			for i in range(int(m_n[1])+1-car_length[0] ,int(m_n[1])+1):
				string = string + " r_"+str(i)+" c_"+goal[0]
			print >> sys.stderr, string	+ ")",
	if goal[0] is '1':		# or str(m_n[1])):
		if 1 in hor_cars:
			string = "(cars_"+str(car_length[0])+" car_1"
			for i in range(1,car_length[0]+1):
				string = string + " r_"+goal[1] + " c_"+str(i)
			print >> sys.stderr, string+")",
	if goal[0] is str(m_n[0]):
		if 1 in hor_cars:
			string = "(cars_"+str(car_length[0])+" car_1"
			for i in range(int(m_n[0])+1-car_length[0] ,int(m_n[0])+1):
				string = string +" r_"+goal[1] + " c_"+str(i)
			print >> sys.stderr, string	+ ")",
	print >> sys.stderr, " (goal_truth t))" 

###########################

print driver_actions
for i in range(1,max(car_length)+1): # TODO: max car_size
	move_strips('top',i)
	move_strips('bottom',i)
	move_strips('left',i)
	move_strips('right',i)

print >> sys.stderr, '''(define (problem prob1)
(:domain car_game)'''
print >> sys.stderr, '(:objects',
print_objects(int(m_n[0]),int(m_n[1]),no_of_cars)
print  >> sys.stderr, ')'

print >> sys.stderr, '(:init'
print_init()
print >> sys.stderr, ')'

print >> sys.stderr, '(:goal'
print_goal()
print >> sys.stderr, ')'
print >> sys.stderr, ')'

print ')'
