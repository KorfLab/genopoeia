Genopoeia
=========

A mythological (fantasy, synthetic, virtual) version of a genome. Each
chromosome has specific qualities used for testing various algorithms.

## Genome ##

A genome is a FASTA file of chromosomes and an associated GFF file that
describes the features on the chromosomes. A special feature, "bias" is used to
describe sequencing ascertainment bias. This has "bias" for source and "seq"
for type. The "score" field is the bias, which is expressed in log2 units. A
score of -1 has a weight of 0.5 (2**-1) while a score of 3 has a weight of 8
(2***3). A dot in the score field is interpreted as a zero (no bias).

```
Ch00  bias  seq  2201  2300  2.1  .  .
```

## Chromosomes ##

A chromosome is a collection of 'loci'. A locus is defined as a 10 kb subset of
a chromosome. The first and last 500 bp of a locus are never used, which
creates at least 1 kb of free space between loci.

A 'region' is a collection of 100 loci.

A 'zone is a collection of 10 regions.

The typical chromosome has 10 zones, each with 10 regions

A locus may be used for a single experiment (e.g. peak) or multiple
experiments.

-


- Names begin with 'Ch' followed by a number
- Size is always 1Mbp (1e6 not 2**20)
- Chromosomes are segmented by factors of 10
	- experiments take place in 1 kb loci
	-
	- There are 10 zones per chromosome (1e5)
	- There are 10 regions per zone (1e4)
	- There are 10 loci per __ (1e3)

| Name | Model | Bias | Features
|:----:|:-----:|:----:|:------------------
| Ch00 |  IID  | none | none
| Ch01 |  IID  | B1   | none

- Size - given in megabases where M = 1e6 not 2e20
- Model
	- IID - all nucleotides equally probable
- Bias
	- None - no sequencing bias
	- B1 - 7 zones from -3 to + 3 bias

