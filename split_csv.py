import sys
import random

print("spliting {} ratio {}/{} into {} and {}...".format(sys.argv[1], sys.argv[2], 100-int(sys.argv[2]), sys.argv[3], sys.argv[4]))

f = open(sys.argv[1])
csv_list = f.readlines()
f.close()
print(len(csv_list))
f1 = open(sys.argv[3], "w")
f2 = open(sys.argv[4], "w")
c1 = 0
c2 = 0

f1.write(csv_list[0])
f2.write(csv_list[0])

for i in range(1, len(csv_list)):
	if random.randint(1, 100) <= int(sys.argv[2]):
		f1.write(csv_list[i])	
		c1 += 1
	else:
		f2.write(csv_list[i])	
		c2 += 1

f2.close()
f1.close()

print("wrote {} records into {}, {} records into {}".format(c1, sys.argv[3], c2, sys.argv[4]))
