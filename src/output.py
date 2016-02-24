import sys
output = ""
moves = [0,0,0,0]
to_print = []
for line in sys.stdin:
	if "no solution" in line:
		print -1
		sys.exit(0)
	elif 'move_top' in line:
		 output = line[line.index('car_')+4:line.index(' r_')]+ ' U '
		 moves[0] = moves[0]+1
	elif 'change_car' in line:
		for i in moves:
			if i != 0:
				to_print.append( output+str(i))
				break
		moves = [0,0,0,0]
	elif 'move_bottom' in line:
		 output = line[line.index('car_')+4:line.index(' r_')]+' D '
		 moves[1] = moves[1]+1
	elif 'move_left' in line:
		 output = line[line.index('car_')+4:line.index(' r_')]+' L '
		 moves[2] = moves[2]+1
	elif 'move_right' in line:
		 output = line[line.index('car_')+4:line.index(' r_')] + ' R '
		 moves[3] = moves[3]+1
for i in moves:
	if i != 0:
        	to_print.append( output+str(i))
            	break

print len(to_print)
for i in to_print:
	print i

