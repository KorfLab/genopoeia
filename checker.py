import sys

hit = {}
with open(sys.argv[1]) as fp:
	for line in fp:
		foo, pos, n = line.split('.')
		pos = int(pos)
		if pos not in hit: hit[pos] = 0
		hit[pos] += 1

for pos in sorted(hit):
	print(pos, hit[pos])
