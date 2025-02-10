Genopoeia
=========

Mythological genomes for testing bioinformatics algorithms.

## Design Goals ##

The initial design goal is to create a setting to evalute algorithms used for
peak-finding. In the future, it may be used for other purposes.

## Genomes ##

A genome is a FASTA file of chromosomes and an associated GFF file that
describes the features on the chromosomes. Genomes are generated
pseudo-randomly using a seed, and the seed becomes part of the genome's name.
`g25` is a genome generated with a random seed of 25. All of its chromosome
names start with `g25`.

### Bias

A special GFF feature, "bias" is used to describe genomic seqeuncing
ascertainment bias (i.e. some areas of a genome are easier to sequence than
others). The source of a bias feature is "dna".

The feature "score" describes the bias numerically, which is expressed in log2
units. A score of -1 has a weight of 0.5 (2**-1) while a score of 3 has a
weight of 8 (2***3). The score of a bias feature is required (no dot). Here's
an example bias feature from seed 25 on chromosome 000 with bias 2.1.

```
g25.000  bias  dna  2201  2300  2.1  .  .
```
