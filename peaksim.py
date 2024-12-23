import argparse
import random
import sys

def random_seq(n):
	seq = []
	for _ in range(n): seq.append(random.choice('ACGT'))
	return ''.join(seq)

def make_noise(rate, x, pos, nwidth, rsize):
	n = int(rate * x * nwidth / rsize)
	a = pos
	b = pos + nwidth
	return [random.randint(a, b) for _ in range(n)]

def make_peaks(rate, x, beg, end, rsize):
	peak_range = end - beg + 1 + 2 * (rsize -1)
	n = int(rate * x * peak_range / rsize)
	a = beg - rsize
	b = end + rsize
	return [random.randint(a, b) for _ in range(n)]

parser = argparse.ArgumentParser(description='chip-seq sampling simulator')
parser.add_argument('name', help='root name for files')
parser.add_argument('--rate', type=int, default=10,
	help='sampling rate [%(default)i]')
parser.add_argument('--pwidth', type=int, default=1,
	help='peak width (e.g. 1, 2000) [%(default)i]')
parser.add_argument('--rsize', type=int, default=100,
	help='read size [%(default)i]')
parser.add_argument('--locus', type=int, default=5000,
	help='size of a locus [%(default)i]')
parser.add_argument('--barrier', type=int, default=100,
	help='barrier space between loci [%(default)i]')
parser.add_argument('--peaks', nargs='+', default=(0, 2, 4, 8, 16, 32),
	help='height of foreground peaks [%(default)s]')
parser.add_argument('--bias', nargs='+', default=(0, 2, 4, 8),
	help='height of background peaks [%(default)s]')
parser.add_argument('--noise', nargs='+', default=(0, 1, 2),
	help='height of background noise [%(default)s]')
parser.add_argument('--loci', type=int, default=100,
	help='number of loci [%(default)i]')
parser.add_argument('--seed', type=int, default=1,
	help='random seed [%(default)i]')
arg = parser.parse_args()

random.seed(arg.seed)
if arg.peaks[0] != 0: sys.exit('start peaks with 0')
if arg.bias[0] != 0: sys.exit('start bias with 0')

freads = []                     # foreground read positions
breads = []                     # background read positions
nreads = []                     # noise read positions
gffs = []                       # peak positions
start = arg.barrier             # the current starting position of a locus
half = arg.locus // 2           # half locus size (peak at center)

for _ in range(arg.loci):
	for fg in arg.peaks:
		for bg in arg.bias:
			for n in arg.noise:
				n = int(n)

				# flat noise
				gffs.append( ('noise', start, start + arg.locus, n) )
				gs = make_noise(arg.rate, n, start, arg.locus, arg.rsize)
				nreads.extend(gs)

				# peaks
				m = start + half         # mid-point of peak
				a = m - arg.pwidth // 2  # start of peak
				b = a + arg.pwidth -1    # end of peak

				# peak noise
				gffs.append( ('back', a, b, bg) )
				bgs = make_peaks(arg.rate, bg, a, b, arg.rsize)
				breads.extend(bgs)

				# peak signal
				gffs.append( ('fore', a, b, fg) )
				fgs = make_peaks(arg.rate, fg, a, b, arg.rsize)
				freads.extend(fgs)

				# update
				start += arg.locus + arg.barrier

# create fasta
genome = random_seq(start)
with open(f'{arg.name}.fa', 'w') as fp:
	print(f'>{arg.name}', file=fp)
	for i in range(0, len(genome), 80):
		print(genome[i:i+80], file=fp)

# create gff
with open(f'{arg.name}.gff', 'w') as fp:
	for kind, a, b, level in gffs:
		if level == 0: continue
		print('\t'.join((arg.name, 'peak', kind, str(a+1), str(b+1),
			str(level), '.', '.')), file=fp)

# create fastq
with open(f'{arg.name}_noise.fq', 'w') as fp:
	for i, pos in enumerate(nreads):
		print(f'@{arg.name}.{pos+1}.{i}', file=fp)
		print(genome[pos:pos+arg.rsize], file=fp)
		print('+', file=fp)
		print('N' * arg.rsize, file=fp)

with open(f'{arg.name}_background.fq', 'w') as fp:
	for i, pos in enumerate(breads):
		print(f'@{arg.name}.{pos+1}.{i}', file=fp)
		print(genome[pos:pos+arg.rsize], file=fp)
		print('+', file=fp)
		print('B' * arg.rsize, file=fp)

with open(f'{arg.name}_foreground.fq', 'w') as fp:
	for i, pos in enumerate(freads):
		print(f'@{arg.name}.{pos+1}.{i}', file=fp)
		print(genome[pos:pos+arg.rsize], file=fp)
		print('+', file=fp)
		print('F' * arg.rsize, file=fp)
