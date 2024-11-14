Genopoeia
=========

A mythological (fantasy, synthetic, virtual) version of a genome. Each
chromosome has specific qualities used for testing various algorithms.

## Genome ##

A genome is a FASTA file of chromosomes and an associated GFF file that
describes the features on the chromosomes. Genomes are generated
pseudo-randomly using a seed, and the seed becomes part of the genome's name.
`g25` is a genome generated with a random seed of 25.

A special feature, "bias" is used to describe various kinds of ascertainment
bias. Bias can come from the sequence itself, or differences in gene
expression. The feature "source" is always "bias". There are several types of
bias.

+ dna - the bias is seen when sampling DNA (e.g. ChIP seq)
+ rna - the bias is seen when sampling RNA (e.g. differential gene expression)


This has "bias" for source and "seq" for type. The "score" field is the
bias, which is expressed in log2 units. A score of -1 has a weight of 0.5
(2**-1) while a score of 3 has a weight of 8 (2***3).

Here's an example bias feature from seed 25 on chromosome c01.

```
g25.c00  bias  dna  2201  2300  2.1  .  .
```

## Chromosomes ##

The smallest subset of a chromosome is called a locus. A locus is defined as 10
kb. The first and last 500 bp of a locus are never used, which creates at least
1 kb of free space between loci.

A 'zone' is a collection of 100 loci, which corresponds to 1M. Each zone can be
a different experiment. A chromosome typically has 10 zones. In aggregate, a
typical chromosome has the following features:

+ 10 Mbp total length
+ 10 zones, each 1 Mbp long
+ 100 loci per zone, each 10 kbp long

| Name | Model | Bias | Features
|:----:|:-----:|:----:|:------------------
| c00  |  IID  | none | none
| c01  |  IID  | B1   | none

- Size - given in megabases where M = 1e6 not 2e20
- Model
	- IID - all nucleotides equally probable
- Bias
	- None - no sequencing bias
	- B1 - 7 zones from -3 to + 3 bias

