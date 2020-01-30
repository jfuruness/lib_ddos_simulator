import random
import copy




rounds = 500

totalclients = 110
goodclients = 100

threshold = rounds/8 

# n = [0,1,2,3,4,5] #users
# br = [('a', [1,2,3]),('b', [0,4,5])] #bucket mapping
# r = 2 #round
# underAttack = ['b']
# moreletterstoappend = ['c', 'd', 'e', 'f', 'g']



# RA1 = [[],[1],[1],[],[1],[]]
#n is the list of clients. br is the list of buckers. r is the current round number, RA1 is the list of rounds the client was attacked in
def shuffle2 (n, br, r, RA1, underAttack, moreletterstoappend, blacklisted):
	# algorithm 7
	for bucket in br:
		if bucket[0] in underAttack:
			for client in bucket[1]:
				RA1[client].append(r)
	newmapping = []
	for element in br:
		newmapping.append((element[0],[]))
		### add or remove buckets
	if len(underAttack) == len(br):
		# print("adding buckets")
		max1 = (len(br) / 4)
		counter = 0
		while counter < max1:
			newmapping.append((moreletterstoappend[0],[]))
			moreletterstoappend.pop(0)
			counter +=1
			# print(newmapping)
	elif len(underAttack) < len(br) / 4:
		if len(br) == 1:
			pass
		else:
			counter = len(br) / 4
			while counter > 0:
				moreletterstoappend.append(newmapping[0])
				newmapping.pop(0)
				counter -=1
	### assign buckets randomly
	for client in n:
		if client not in blacklisted:
			integer = random.randint(0,len(newmapping)-1)
			newmapping[integer][1].append(client)
	r +=1
	br = newmapping
	return n, br, r, RA1, moreletterstoappend, blacklisted



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
			if element > totalclients:
				underAttack.append(bucket[0])
				break
	# print(underAttack)
	RA1 = list()
	blacklisted = list()
	for element in n:
		RA1.append(list())
	while r < rounds:
		# print("got here")
		n,br,r,RA1,underAttack, blacklisted = shuffle2(n, br, r, RA1, underAttack, moreletterstoappend, blacklisted)
		underAttack = []
		# print(RA)
		for bucket in br:
			for element in bucket[1]:
				if element > goodclients:
					if bucket[0] not in underAttack:
						underAttack.append(bucket[0])
		for client in n:
			if len(RA1[client]) > threshold:
				if client not in blacklisted:
					blacklisted.append(client)
	print(blacklisted, "= blacklisted")



run()