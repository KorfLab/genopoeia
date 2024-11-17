import argparse
import random
import sys

def random_seq(n):
	seq = []
	for _ in range(n): seq.append(random.choice('ACGT'))
	return ''.join(seq)

def make_noise(rate, depth, start, length, size):
	n = int(rate * depth * length / size)
	return [random.randint(start, start+ length) for _ in range(n)]

def make_peaks(rate, depth, mu, sig, width, size):
	if width < size: width = size
	n = int(rate * depth * width / size)
	return [int(random.gauss(mu, sig)) for _ in range(n)]


parser = argparse.ArgumentParser(description='chip-seq sampling simulator')
parser.add_argument('rate', type=int, help='sampling rate (e.g. 1)')
parser.add_argument('width', type=int, help='peak width (e.g. 1 or 2000)')
parser.add_argument('space', type=int, help='space between peaks (e.g. 1000)')
parser.add_argument('name', help='root name for files')
parser.add_argument('--seed', type=int, default=1,
	help='random seed [%(default)i]')
parser.add_argument('--sigma', type=float, default=20,
	help='standard deviation for read placement [%(default).1f]')
parser.add_argument('--size', type=int, default=100,
	help='read size [%(default)i')
parser.add_argument('--peaks', type=list, default=(0, 2, 4, 8, 16, 32),
	help='height of foreground peaks [%(default)s]')
parser.add_argument('--bias', type=list, default=(0, 2, 4, 8),
	help='height of background peaks [%(default)s]')
parser.add_argument('--noise', type=list, default=(0, 1, 2),
	help='height of background noise [%(default)s]')
parser.add_argument('--loci', type=int, default=100,
	help='number of loci [%(default)i]')
arg = parser.parse_args()

random.seed(arg.seed)

reads = [] # sequencing read positions
gffs = [] # position of peaks (both foreground and background)
pos = arg.space # start of first peak
for _ in range(arg.loci):
	for f in arg.peaks:
		gffs.append( ('fore', pos, f) )
		for b in arg.bias:
			gffs.append( ('back', pos, b) )
			for n in arg.noise:
				gs = make_noise(arg.rate, n, pos, arg.width + arg.space, arg.size)
				fs = make_peaks(arg.rate, f, pos, arg.sigma, arg.width, arg.size)
				bs = make_peaks(arg.rate, b, pos, arg.sigma, arg.width, arg.size)
				reads.extend(gs)
				reads.extend(fs)
				reads.extend(bs)
				pos += arg.space

# create fasta
genome = random_seq(pos)
with open(f'{arg.name}.fa', 'w') as fp:
	print(f'>{arg.name}', file=fp)
	for i in range(0, len(genome), 80):
		print(genome[i:i+80], file=fp)

# create gff
with open(f'{arg.name}.gff', 'w') as fp:
	for kind, pos, level in gffs:
		print('\t'.join((arg.name, 'peak', kind, str(pos), str(pos + arg.size),
			str(level), '.', '.')), file=fp)

# create fastq
with open(f'{arg.name}.fq', 'w') as fp:
	for i, pos in enumerate(reads):
		print(f'@{arg.name}.{pos}.{i}', file=fp)
		print(genome[pos:pos+arg.size], file=fp)
		print('+', file=fp)
		print('B' * arg.size, file=fp)
