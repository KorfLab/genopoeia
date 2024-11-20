import argparse
import itertools
import random
import sys

def random_seq(n):
	seq = []
	for _ in range(n): seq.append(random.choice('ACGT'))
	return ''.join(seq)

def random_intron(n, canonical=True):
	if canonical: return 'GT' + random_seq(n-4) + 'AG'
	else:         return 'AA' + random_seq(n-4) + 'TT'

def make_snps(seq):
	pass

def make_indels(seq):
	pass

def generate_reads(seq, rsize):
	for i in range(len(seq) -rsize + 1): yield seq[i:i+rsize]
	
def write_fasta(fp, name, seq, wrap=True):
	print(f'>{name}', file=fp)
	if wrap == False:
		print(seq, file=fp)
		return
	for i in range(0, len(seq), 80):
		print(seq[i:i+80], file=fp)


parser = argparse.ArgumentParser(description='splicing data simulator')
parser.add_argument('root', help='path to the project directory')
parser.add_argument('--seed', type=int, default=1,
	help='random seed [%(default)i]')
parser.add_argument('--rsize', type=int, default=100,
	help='read size [%(default)i]')
parser.add_argument('--flank', type=int, default=100,
	help='flanking sequence upstream and downstream [%(default)i]')
parser.add_argument('--exon', type=int, default=100,
	help='non-variable exon size [%(default)i]')
parser.add_argument('--intron', type=int, default=100,
	help='non-variable intron size [%(default)i]')
parser.add_argument('--vintron', nargs=2, default=[5, 40],
	help='variable intron size min & max %(default)s')
parser.add_argument('--vexon', nargs=2, default=[1, 40],
	help='variable exon size min & max %(default)s')
arg = parser.parse_args()

random.seed(arg.seed)

# globals
cid = 0 # unique chromosome id
rid = 0 # unique read id
vimin = int(arg.vintron[0])
vimax = int(arg.vintron[1])
vemin = int(arg.vexon[0])
vemax = int(arg.vexon[1])

# how do intron lengths affect alignment?
# [exon]---v.intron---[exon]

gfp = open(f'{arg.root}/vi.genome.fa', 'w')
rfp = open(f'{arg.root}/vi.reads.fa', 'w')
ifp = open(f'{arg.root}/vi.info.txt', 'w')

for ilen in range(vimin, vimax +1):
	cid += 1
	f1 = random_seq(arg.flank)
	e1 = random_seq(arg.exon)
	iv = random_intron(ilen)
	e2 = random_seq(arg.exon)
	f2 = random_seq(arg.flank)
	write_fasta(gfp, f'c{cid}', f1 + e1 + iv + e2 + f2)
	for read in generate_reads(e1 + e2, arg.rsize):
		rid += 1
		write_fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)
	ibeg = arg.flank + arg.exon + 1
	iend = ibeg + ilen
	text = f'intron-{ilen}'
	print(f'c{cid}', 'intron', ibeg, iend, text, file=ifp)

gfp.close()
rfp.close()
ifp.close()

# how do exon lengths affect alignment?
# [exon]---intron---[v.exon]---intron---[exon]

gfp = open(f'{arg.root}/ve.genome.fa', 'w')
rfp = open(f'{arg.root}/ve.reads.fa', 'w')
ifp = open(f'{arg.root}/ve.info.txt', 'w')

for elen in range(vemin, vemax + 1):
	cid += 1
	f1 = random_seq(arg.flank)
	e1 = random_seq(arg.exon)
	i1 = random_intron(arg.intron)
	ev = random_seq(elen)
	i2 = random_intron(arg.intron)
	e2 = random_seq(arg.exon)
	f2 = random_seq(arg.flank)
	write_fasta(gfp, f'c{cid}', f1 + e1 + i1 + ev + i2 + e2 + f2)
	for read in generate_reads(e1 + ev + e2, arg.rsize):
		rid += 1
		write_fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)
	i1b = arg.flank + arg.exon
	i1e = i1b + arg.intron
	i2b = arg.flank + arg.exon + elen
	i2e = i2b + arg.intron
	text = f'exon-{elen}'
	print(f'c{cid}', 'intron', i1b, i1e, text, file=ifp)
	print(f'c{cid}', 'intron', i2b, i2e, text, file=ifp)

gfp.close()
rfp.close()
ifp.close()

"""
+ vi vary intron length
+ ve vary exon length
- low complexity
- paralogy
- non-canonical
- trans-splicing
- poly-A tail
- fusions
- substitutions
- indels
"""

