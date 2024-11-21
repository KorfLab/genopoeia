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

#-----------------------------------------------------------------------------
# Experiment 1
# Junk sequences: none of the sequences align
# [junk]

gfp = open(f'{arg.root}/junk.genome.fa', 'w')
rfp = open(f'{arg.root}/junk.reads.fa', 'w')
ifp = open(f'{arg.root}/junk.info.txt', 'w')

cid += 1
for _ in range(arg.exon):
	rid += 1
	read = random_seq(arg.rsize)
	write(fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)

gfp.close()
rfp.close()
ifp.close()

#-----------------------------------------------------------------------------
# Experiment 2
# Vanilla alignment: create and align all reads
# [exon]---intron---[exon]

gfp = open(f'{arg.root}/vanilla.genome.fa', 'w')
rfp = open(f'{arg.root}/vanilla.reads.fa', 'w')
ifp = open(f'{arg.root}/vanilla.info.txt', 'w')

cid += 1
f1 = random_seq(arg.flank)
e1 = random_seq(arg.exon)
i1 = random_intron(arg.intron)
e2 = random_seq(arg.exon)
f2 = random_seq(arg.flank)
write_fasta(gfp, f'c{cid}', f1 + e1 + i1 + e2 + f2)
for read in generate_reads(e1 + e2, arg.rsize):
	rid += 1
	write_fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)
ibeg = arg.flank + arg.exon + 1
iend = ibeg + arg.intron -1
text = f'intron-{arg.intron}'
print(f'c{cid}', 'intron', ibeg, iend, text, file=ifp)

gfp.close()
rfp.close()
ifp.close()

#-----------------------------------------------------------------------------
# Experiment 3
# Extra sequences: reads polluted with junk
# [exon]---intron---[exon]
# [junk]

gfp = open(f'{arg.root}/extra.genome.fa', 'w')
rfp = open(f'{arg.root}/extra.reads.fa', 'w')
ifp = open(f'{arg.root}/extra.info.txt', 'w')

cid += 1
f1 = random_seq(arg.flank)
e1 = random_seq(arg.exon)
i1 = random_intron(arg.intron)
e2 = random_seq(arg.exon)
f2 = random_seq(arg.flank)
write_fasta(gfp, f'c{cid}', f1 + e1 + i1 + e2 + f2)
for read in generate_reads(e1 + e2, arg.rsize):
	rid += 1
	write_fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)
ibeg = arg.flank + arg.exon + 1
iend = ibeg + arg.intron -1
text = f'intron-{arg.intron}'
print(f'c{cid}', 'intron', ibeg, iend, text, file=ifp)
for _ in range(arg.exon *2):
	rid += 1
	read = random_seq(arg.rsize)
	write(fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)

gfp.close()
rfp.close()
ifp.close()

#-----------------------------------------------------------------------------
# Experiment 4
# how do intron lengths affect alignment?
# [exon]---v.intron---[exon]

vimin = int(arg.vintron[0])
vimax = int(arg.vintron[1])

gfp = open(f'{arg.root}/var_intron.genome.fa', 'w')
rfp = open(f'{arg.root}/var_intron.reads.fa', 'w')
ifp = open(f'{arg.root}/var_intron.info.txt', 'w')

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
	text = f'vanilla-{ilen}'
	print(f'c{cid}', 'intron', ibeg, iend, text, file=ifp)

gfp.close()
rfp.close()
ifp.close()

#-----------------------------------------------------------------------------
# Experiment 5
# how does middle exon length affect alignment?
# [exon]---intron---[v.exon]---intron---[exon]

vemin = int(arg.vexon[0])
vemax = int(arg.vexon[1])

gfp = open(f'{arg.root}/var_exon.genome.fa', 'w')
rfp = open(f'{arg.root}/var_exon.reads.fa', 'w')
ifp = open(f'{arg.root}/var_exon.info.txt', 'w')

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

#-----------------------------------------------------------------------------
# Experiment 6
# how does initial exon length affect alignment?
# [v.exon]---intron---[exon]

gfp = open(f'{arg.root}/var_einit.genome.fa', 'w')
rfp = open(f'{arg.root}/var_einit.reads.fa', 'w')
ifp = open(f'{arg.root}/var_einit.info.txt', 'w')

for elen in range(vemin, vemax + 1):
	cid += 1
	f1 = random_seq(arg.flank)
	ev = random_seq(elen)
	i1 = random_intron(arg.intron)
	e2 = random_seq(arg.exon)
	f2 = random_seq(arg.flank)
	write_fasta(gfp, f'c{cid}', f1 + ev + i1 + e2 + f2)
	for read in generate_reads(ev + e2, arg.rsize):
		rid += 1
		write_fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)
	ibeg = arg.flank + elen
	iend = ibeg + arg.intron
	text = f'einit-{elen}'
	print(f'c{cid}', 'intron', ibeg, iend, text, file=ifp)

gfp.close()
rfp.close()
ifp.close()

#-----------------------------------------------------------------------------
# Experiment 7
# how does terminal exon length affect alignment?
# [exon]---intron---[v.exon]

gfp = open(f'{arg.root}/var_eterm.genome.fa', 'w')
rfp = open(f'{arg.root}/var_eterm.reads.fa', 'w')
ifp = open(f'{arg.root}/var_eterm.info.txt', 'w')

for elen in range(vemin, vemax + 1):
	cid += 1
	f1 = random_seq(arg.flank)
	e1 = random_seq(arg.exon)
	i1 = random_intron(arg.intron)
	ev = random_seq(elen)
	f2 = random_seq(arg.flank)
	write_fasta(gfp, f'c{cid}', f1 + e1 + i1 + ev + f2)
	for read in generate_reads(e1 + ev, arg.rsize):
		rid += 1
		write_fasta(rfp, f'c{cid}.r{rid}', read, wrap=False)
	ibeg = arg.exon
	iend = ibeg + arg.intron
	text = f'eterm-{elen}'
	print(f'c{cid}', 'intron', ibeg, iend, text, file=ifp)

gfp.close()
rfp.close()
ifp.close()

#-----------------------------------------------------------------------------
# Experiment
# how does trans-splicing affect alignment
# [ts.exon]---intron---[exon]

#-----------------------------------------------------------------------------
# Experiment
# how does poly-A tail affect alignment?
# [exon]---intron---[exon][poly-A]

#-----------------------------------------------------------------------------
# Experiment
# how do 5' artefacts affect alignment?
# [v.artefact][exon]---intron---[exon]

#-----------------------------------------------------------------------------
# Experiment
# how do 3' artefacts affect alignment?
# [exon]---intron---[exon][v.artefact]

#-----------------------------------------------------------------------------
# Experiment
# how do 5' internal artefacts affect alignment?
# [exon][v.artefact]---intron---[exon]

#-----------------------------------------------------------------------------
# Experiment
# how do 3' internal artefacts affect alignment?
# [exon]---intron---[v.artefact][exon]

#-----------------------------------------------------------------------------
# Experiment
# how do substitutions affect alignment?
# [s.exon]---intron---[s.exon]

#-----------------------------------------------------------------------------
# Experiment
# how do indels affect alignment?
# [i.exon]---intron---[i.exon]

#-----------------------------------------------------------------------------
# Experiment
# how does low complexity affect alignment?
# [lc.exon]---intron---[lc.exon]

#-----------------------------------------------------------------------------
# Experiment
# how does duplication affect alignment?
# [exon1]---intron---[exon2] ... [exon1]---intron---[exon2]

#-----------------------------------------------------------------------------
# Experiment
# how do non-canonical splice sites affect alignment?
# [exon]---nc.intron---[exon]


