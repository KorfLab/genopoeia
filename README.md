Genopoeia
=========

Mythological genomes for testing bioinformatics algorithms.

## Design Goals ##

The initial design goal is to create a setting to evalute algorithms used for
peak-finding. In the future, it may be used for alignment, spliced alignment,
differential gene expression, variant detection, gene-prediction, or even
pan-genomic analyses.

## Genomes ##

A genome is a FASTA file of chromosomes and an associated GFF file that
describes the features on the chromosomes. Genomes are generated
pseudo-randomly using a seed, and the seed becomes part of the genome's name.
`g25` is a genome generated with a random seed of 25. All of its chromosome
names start with `g25`. Chromosomes are numbered from 0 upwards. Smaller
numbers are generally shorter and simpler chromosomes. For example, `g25.0` is
a short, simple chromosome made with seed 25.

## Chromosomes, Loci, and Zones ##

Chromosomes are organized into descrete units with obvious bounaries. A
chromosmal locus is defined as 10 kb. Each locus begins with 80 nts of Ns
followed by 320 nt of unbiased sequence. Sequences with "interesting" content
begin 401 bases into the locus and continue to 9600 bases into the locus. The
last 400 bases of a locus are 320 nt of unbiased sequence followed by 80 nts of
Ns.

An 'experimental zone' or just 'zone' is a collection of 100 loci, which
corresponds to 1M. The smallest chromosomes are just 1 zone, but larger
chromosomes may have several zones.

## Genome Generation ##

Genomes are generated by a generalized hidden Markov model (GHMM) stored as a
JSON file. The "name" of the GHMM should match the file name without the file
extension. The "source" is a free text field that describes how the GHMM was
built. Most of the GHMM is described as a dictionary of "state" objects.

Each "state" object is indexed by its name. State objects can be of three
types: "markov", "pwm", or "static". A "markov" state generates sequence 1 nt
at a time over a weighted random duration. This is used to generate features
with variable lengths, such as intergenic sequences. A "pwm" state generates
sequence from a position weight matrix. This is used for features with standard
lengths and specific misspellings, such as splice sites. A "static" state
generates an exact sequence and a corresponding "drift" rate. This is useful
for representing repeats of various ages. All states also specify "init" and
"term", which specifies the weight assoiciated with starting or ending in a
state.

To see how all this fits together, it's best to look at a simple example.

```
{
	"name": "toy",
	"source": "fabricated",
	"states": {
		"iid": {
			"type": "markov",
			"init": 1,
			"term": 1,
			"transitions": {"hom": 1.0},
			"durations": [0, 0, 0, 1, 1, 1],
			"emissions": {"": [1, 1, 1, 1]},
		},
		"hom": {
			"type": "markov",
			"init": 0,
			"term": 0,
			"transitions": {"iid": 0.5, "rep": 0.5},
			"durations": [2, 2, 2, 1, 1, 1],
			"emissions": {
				"A": [9, 1, 1, 1],
				"C": [1, 9, 1, 1],
				"G": [1, 1, 9, 1],
				"T": [1, 1, 1, 9]
			}
		}
	}
}
```

The toy GHMM above flip-flops back and forth between two states: iid and hom.
In the iid state, the emissions are unbiased and the states are 4-6 nt long. In
the hom state, the emissions tend to be homopolymers, and the states are more
likely to be 1-3 nt than 4-6.

Here are some more example states...

## GHMM Files ##

Pre-built GHMMs are stored in the `models` directory.

| Name | Description
|:-----|:----------------------------------------------------------
| iid  | all nucleotides equally probable
| ec.0 | inspired by E. coli
| ce.0 | inspired by C. elegans


### Repeat

A repeat is a sequence that shows up multiple times in a genome.

### Bias

A special GFF feature, "bias" is used to describe various kinds of
ascertainment bias. Bias can come from the sequence itself, or differences in
gene expression. The feature "source" is "bias" and the feature "type"
describes that bias in more detail.

+ dna - the bias is seen when sampling DNA (e.g. ChIP seq)
+ rna - the bias is seen when sampling RNA (e.g. differential gene expression)

The feature "score" describes the bias numerically, which is expressed in log2
units. A score of -1 has a weight of 0.5 (2**-1) while a score of 3 has a
weight of 8 (2***3). The score of a bias feature is required (no dot). Here's
an example bias feature from seed 25 on chromosome 000 with bias 2.1.

```
g25.000  bias  dna  2201  2300  2.1  .  .
```


## Sampling ##

To sample sequencing reads from a genome, use `sample_genome.py`. This program
uses various features of the genome.

+ genome
+ wide
+ narrow
+ mrna

## Reconstructions and Subsets ##

Every genome is procedurally generated from a random seed. Some chromosomes of
a genome might not be useful for a specific study. Therefore, it is often
useful to create a subset of a genome, which is done with `subset_genome.py`.



## Peak Feature ##



## Gene Feature ##

Genes require more complex sequence model

