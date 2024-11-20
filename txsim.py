import argparse
import random
import sys

def random_seq(n):
	seq = []
	for _ in range(n): seq.append(random.choice('ACGT'))
	return ''.join(seq)

def make_snps(seq):
	pass

def make_indels(seq):
	pass

def generate_reads(seq, length, paired=False):
	pass

parser = argparse.ArgumentParser(description='spliced alignment tester')
parser.add_argument('--seed', type=int, default=1,
	help='random seed [%(default)i]')
parser.add_argument('--rsize', type=int, default=100,
	help='read size [%(default)i]')
arg = parser.parse_args()

random.seed(arg.seed)
fileroot = f'spat.{arg.seed}.{arg.rsize}'
fasta = fileroot + '.fa'
gff = fileroot + '.gff'
fastq = fileroot + '.fq'

"""

+ sequence variation
	+ snps
	+ indels
+ introns
	+ intron length
	+ splice site concensus
+ exons
	+ exon length
	+ exon low complexity
	+ exon paralogy
+ misc
	+ trans-splicing
	+ poly-A tail
	+ extra sequence (fused/hybrid)


"""

genes = []
