import random
import copy


rounds = 100000
totalclients = 110
goodclients = 100
threshold = 5000



# n = [0,1,2,3,4,5] #users
# br = [('a', [1,2,3]),('b', [0,4,5])] #bucket mapping
# r = 2 #round
# underAttack = ['b']
# moreletterstoappend = ['c', 'd', 'e', 'f', 'g']
# s = [0+ .00,1/3+.001,1/3+.002,0+.003,1/3+.004,0+.005]

#n is the list of clients. br is the list of buckers. r is the current round number
def shuffle3 (n, br, r, s, underAttack, moreletterstoappend, blacklisted):
	# algorithm 7
	for bucket in br:
		if bucket[0] in underAttack:
			for client in bucket[1]:
				# print(bucket[0], len(bucket[1]))
				s[client] += 1/ len(bucket[1])
		newmapping = []
	for element in br:
		newmapping.append((element[0],[]))
		### add or remove buckets
	if len(underAttack) == len(br):
		max1 = (len(br) / 4)
		counter = 0
		while counter < max1:
			newmapping.append((moreletterstoappend[0], list()))
			moreletterstoappend.pop(0)
			counter +=1
	elif len(underAttack) < len(br) / 4:
		if len(br) == 1:
			pass
		else:
			counter = len(br) / 4
			while counter > 0:
				moreletterstoappend.append(newmapping[0])
				newmapping.pop(0)
				counter -=1
	### assign buckets based on reputation!
	#first sort based on reputation
	temp = {val: key for key, val in enumerate(sorted(s))} 
	positions = list(map(temp.get, s))
	# print(s)
	# print(positions, "!!!!!!!!!!!!!!")
	perbucket = len(n)/ len(newmapping)
	# print(perbucket)

	for value in range(0, len(positions)):
		# print(newmapping)
		# print(int(positions[value]/perbucket))
		integer = int((positions[value]/perbucket)+ random.randrange(-9,0)/10)
		# print(integer, "integer")
		# print(integer)
		newmapping[integer][1].append(value)
		
	r +=1
	br = newmapping
	return n, br, r, s, underAttack, moreletterstoappend, blacklisted

# print(shuffle3(n, br, r, s, underAttack))




def run():
	n = list()
	moreletterstoappend = list()
	underAttack = list()
	for i in range(0,totalclients):
		n.append(i)
		moreletterstoappend.append(str(i))
	r = 0
	br = list()
	br.append(("a", copy.deepcopy(n)))
	for bucket in br:
		for element in bucket[1]:
			if element > goodclients:
				underAttack.append(bucket[0])
				break
	# print(underAttack)
	s = list()
	blacklisted = list()
	for element in n:
		s.append(element / 10000)
	# print(s)
	while r < rounds:
		# print("got here")
		n,br,r,s,underAttack, moreletterstoappend, blacklisted = shuffle3(n, br, r, s, underAttack, moreletterstoappend, blacklisted)
		underAttack = []
		# print(RA)
		for bucket in br:
			for element in bucket[1]:
				if element > goodclients:
					if bucket[0] not in underAttack:
						underAttack.append(bucket[0])
		for client in n:
			if s[client] > threshold:
				if client not in blacklisted:
					blacklisted.append(client)
	print(s)
	print(blacklisted, "= blacklisted")



run()
run()
run()
run()