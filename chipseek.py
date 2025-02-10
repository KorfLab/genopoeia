import argparse
import random

def random_dna(n): return ''.join(random.choices('ACGT', k=n))

parser = argparse.ArgumentParser(description='ChIP-Seq virtual data maker')
parser.add_argument('name')
parser.add_argument('--chromosomes', type=int, default=2,
	help='number of chromosomes [%(default)i]')
parser.add_argument('--regions', type=int, default=5,
	help='number of peak-containing regions per chromosome [%(default)i]')
parser.add_argument('--padding', type=int, default=1000,
	help='spacing between peaks [%(default)i]')
parser.add_argument('--width', type=int, default=1000,
	help='peak width [%(default)i]')
parser.add_argument('--depth', type=int, default=10,
	help='target sequencing read depth [%(default)i]')
parser.add_argument('--min-bias', type=int, default=-2)
parser.add_argument('--max-bias', type=int, default=4)
parser.add_argument('--seed', type=int, help='set random seed')
arg = parser.parse_args()

if arg.seed: random.seed(arg.seed)


# start a "peak containing region"
# decide the amount of bias (randomly)
# generate input reads over the region
# generate reads over the region
# generate the feature description

for cn in range(arg.chromosomes):
	ffp = open(f'{arg.name}.fa', 'w')
	gfp = open(f'{arg.name}.gff', 'w')

	for rn in range(arg.regions):
		rseq = random_dna(arg.width)
		bias = arg.min_bias + random.random() * (arg.max_bias - arg.min_bias)
		print(cn, rn, bias)
