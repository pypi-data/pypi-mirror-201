# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codx']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.81,<2.0',
 'click>=8.1.3,<9.0.0',
 'pandas>=1.5.3,<2.0.0',
 'uniprotparser>=1.0.9,<2.0.0']

entry_points = \
{'console_scripts': ['codx = codx.cli:main']}

setup_kwargs = {
    'name': 'codx',
    'version': '0.1.1',
    'description': 'A package used to retrieve exon for protein sequences from RefSeqGene database',
    'long_description': '# CODX\n---\n\n`codx` is a python package that allow retrieval of exons data from NCBI RefSeqGene database.\n\n## Installation\n\n```bash\npip install codx\n```\n\n## Usage\n---\nThe package uses gene id in order to retrieve exons data from NCBI RefSeqGene database. The gene id can be obtained from the Uniprot database using the accession id of the gene. The `get_geneids_from_uniprot` function can be used to obtain the gene id from RefSeqGene database of NCBI.\n\n\n```python\n# if you only have accession id, you must first use the get_geneids_from_uniprot function to get the gene id from Uniprot\nfrom codx.components import get_geneids_from_uniprot\n\ngene_ids = get_geneids_from_uniprot(["P35568", "P05019", "Q99490", "Q8NEJ0", "Q13322", "Q15323"])\n# the result will be a set of gene ids that can be obtained from the Uniprot database using the list of Uniprot accession above\n```\n\n\n\n```python\n# Import the create_db function to create a sqlite3 database with gene and exon data from NCBI\nfrom codx.components import create_db\n\n\n# 120892 is the gene id for LRRK2 gene\ndb = create_db(["120892"], entrez_email="your@email.com") # You need to provide an email address to use the NCBI API\n\n# From the database object, you can retrieve a gene object using its gene name\ngene = db.get_gene("LRRK2")\n\n# From the gene objects you can retrieve exons data from the blocks attribute each exon object has its start and end location as well as the associated sequence\nfor exon in gene.blocks:\n    print(exon.start, exon.end, exon.sequence)\n\n# Using the gene object it is also possible to create all possible ordered combinations of exons\n# This will be a generator object that yield a SeqRecord object for each combination\n# There however may be a lot of combinations so depending on the gene, you may not want to use this with a very large gene unless there are no other options\nfor exon_combination in gene.shuffle_blocks():\n    print(exon_combination)\n\n# To create six frame translation of any sequence, you can use the three_frame_translation function twice, one with and one without the reverse complement option enable\n# Each output is a dictionary with the translatable sequence as value and the frame as key\nfrom codx.components import three_frame_translation\nfor exon_combination in gene.shuffle_blocks():\n    three_frame = three_frame_translation(exon_combination.seq, only_start_at_atg=True)\n    three_frame_complement = three_frame_translation(exon_combination.seq, only_start_at_atg=True, reverse_complement=True)\n\n```\n',
    'author': 'Toan Phung',
    'author_email': 'toan.phungkhoiquoctoan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
