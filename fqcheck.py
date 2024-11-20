import sys

count = {}
with open(sys.argv[1]) as fp:
	for line in fp:
		if not line.startswith('@'): continue
		f = line.split('.')
		n = int(f[1])
		if n not in count: count[n] = 0
		count[n] += 1

for n, c in sorted(count.items()):
	print(n, c, sep='\t')
