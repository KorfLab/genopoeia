#!/bin/env python3

import argparse
import json
import random

from grimoire.feature import Feature
from grimoire.sequence import DNA

def make_sequence(model_file):
	with open(model_file) as fp:
		model = json.load(fp)
	k = len(list(model.keys())[0])
	seqlen = 100
	seq = []
	for i in range(k): seq.append(random.choice('ACGT'))
	for i in range(k, seqlen):
		ctx = ''.join(seq[i-k:i])
		nt = random.choices('ACGT', weights=model[ctx])[0]
		seq.append(nt)
	return ''.join(seq)


## CLI

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=1,
	help='random seed [%(default)i]')
parser.add_argument('--chromosomes', type=int, default=0,
	help='number of chromosomes to generate (0 means all)')
arg = parser.parse_args()

s = make_sequence('models/ce2.json')
print(s)
