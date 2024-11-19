import argparse
import random
import sys

def random_seq(n):
	seq = []
	for _ in range(n): seq.append(random.choice('ACGT'))
	return ''.join(seq)

def make_noise(rate, x, pos, pwidth, rsize):
	n = int(rate * x * pwidth / rsize)
	a = pos - rsize + 1
	b = pos + rsize
	print('noise', a, b)
	return [random.randint(a, b) for _ in range(n)]

def make_peaks(rate, x, pos, pwidth, rsize):
	n = int(rate * x * pwidth / rsize)
	a = pos - rsize + 1
	b = pos + rsize
	print('peak', a, b)
	return [random.randint(a, b) for _ in range(n)]

parser = argparse.ArgumentParser(description='chip-seq sampling simulator')
parser.add_argument('name', help='root name for files')
parser.add_argument('rate', type=int, help='sampling rate (e.g. 1)')
parser.add_argument('--pwidth', type=int, default=1,
	help='peak width (e.g. 1, 2000) [%(default)i]')
parser.add_argument('--buffer', type=int, default=5000,
	help='buffer space after peaks [%(default)i]')
parser.add_argument('--barrier', type=int, default=100,
	help='barrier space between regions [%(default)i]')
parser.add_argument('--rsize', type=int, default=100,
	help='read size [%(default)i]')
parser.add_argument('--peaks', type=list, default=(0, 2, 4, 8, 16, 32),
	help='height of foreground peaks [%(default)s]')
parser.add_argument('--bias', type=list, default=(0, 2, 4, 8),
	help='height of background peaks [%(default)s]')
parser.add_argument('--noise', type=list, default=(0, 1, 2),
	help='height of background noise [%(default)s]')
parser.add_argument('--loci', type=int, default=100,
	help='number of loci [%(default)i]')
parser.add_argument('--seed', type=int, default=1,
	help='random seed [%(default)i]')
arg = parser.parse_args()

random.seed(arg.seed)

reads = [] # sequencing read positions
gffs = [] # position of peaks (both foreground and background)
pos = arg.buffer + arg.barrier # start of first peak
info = []
for _ in range(arg.loci):
	for f in arg.peaks:
		gffs.append( ('fore', pos, f) )
		for b in arg.bias:
			gffs.append( ('back', pos, b) )
			for n in arg.noise:
				info.append(f'pos:{pos} fore:{f} back:{b} noise:{n}')
				gs = make_noise(arg.rate, n, pos, arg.pwidth, arg.rsize)
				fs = make_peaks(arg.rate, f, pos, arg.pwidth, arg.rsize)
				bs = make_peaks(arg.rate, b, pos, arg.pwidth, arg.rsize)
				reads.extend(gs)
				reads.extend(fs)
				reads.extend(bs)
				pos += arg.pwidth + arg.buffer + arg.barrier

# create fasta
genome = random_seq(pos)
with open(f'{arg.name}.fa', 'w') as fp:
	print(f'>{arg.name}', file=fp)
	for i in range(0, len(genome), 80):
		print(genome[i:i+80], file=fp)

# create gff
with open(f'{arg.name}.gff', 'w') as fp:
	for kind, pos, level in gffs:
		print('\t'.join((arg.name, 'peak', kind, str(pos),
			str(pos + arg.pwidth -1), str(level), '.', '.')), file=fp)

# create fastq
with open(f'{arg.name}.fq', 'w') as fp:
	for i, pos in enumerate(reads):
		print(f'@{arg.name}.{pos}.{i}', file=fp)
#		print(genome[pos:pos+arg.size], file=fp)
#		print('+', file=fp)
#		print('B' * arg.size, file=fp)

# create info
with open(f'{arg.name}.info', 'w') as fp:
	for s in info: print(s, file=fp)
