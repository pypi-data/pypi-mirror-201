# CODX
---

`codx` is a python package that allow retrieval of exons data from NCBI RefSeqGene database.

## Installation

```bash
pip install codx
```

## Usage Python Package
---
The package uses gene id in order to retrieve exons data from NCBI RefSeqGene database. The gene id can be obtained from the Uniprot database using the accession id of the gene. The `get_geneids_from_uniprot` function can be used to obtain the gene id from RefSeqGene database of NCBI.


```python
# if you only have accession id, you must first use the get_geneids_from_uniprot function to get the gene id from Uniprot
from codx.components import get_geneids_from_uniprot

gene_ids = get_geneids_from_uniprot(["P35568", "P05019", "Q99490", "Q8NEJ0", "Q13322", "Q15323"])
# the result will be a set of gene ids that can be obtained from the Uniprot database using the list of Uniprot accession above
```



```python
# Import the create_db function to create a sqlite3 database with gene and exon data from NCBI
from codx.components import create_db


# 120892 is the gene id for LRRK2 gene
db = create_db(["120892"], entrez_email="your@email.com") # You need to provide an email address to use the NCBI API

# From the database object, you can retrieve a gene object using its gene name
gene = db.get_gene("LRRK2")

# From the gene objects you can retrieve exons data from the blocks attribute each exon object has its start and end location as well as the associated sequence
for exon in gene.blocks:
    print(exon.start, exon.end, exon.sequence)

# Using the gene object it is also possible to create all possible ordered combinations of exons
# This will be a generator object that yield a SeqRecord object for each combination
# There however may be a lot of combinations so depending on the gene, you may not want to use this with a very large gene unless there are no other options
for exon_combination in gene.shuffle_blocks():
    print(exon_combination)

# To create six frame translation of any sequence, you can use the three_frame_translation function twice, one with and one without the reverse complement option enable
# Each output is a dictionary with the translatable sequence as value and the frame as key
from codx.components import three_frame_translation
for exon_combination in gene.shuffle_blocks():
    three_frame = three_frame_translation(exon_combination.seq, only_start_at_atg=True)
    three_frame_complement = three_frame_translation(exon_combination.seq, only_start_at_atg=True, reverse_complement=True)

```

## Usage Command Line
---
In addition to the python API, installation also provide a cli interface that can be used for the same purpose


```bash
Usage: codx [OPTIONS] IDS

Options:
  -o, --output TEXT              Output file
  -i, --include-intron           Include intron
  -u, --uniprot                  Input is Uniprot accession ids
  -t, --translate                Translate to protein
  -3, --three-frame-translation  Translate to protein in 3 frames
  -6, --six-frame-translation    Translate to protein in 6 frames (3 forward
                                 and 3 reverse complement)
  --help                         Show this message and exit.
```

Here IDS positional argument are a list of gene ids or uniprot accession ids delimited by `,`.

Example usage can be seen below

```bash
codx -o output.fasta -u P35568,P05019,Q99490,Q8NEJ0,Q13322,Q15323
```

```bash
codx -o output.fasta 1190,120892
```