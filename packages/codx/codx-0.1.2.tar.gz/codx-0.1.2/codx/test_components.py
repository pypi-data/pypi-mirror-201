from unittest import TestCase

from codx.components import create_db, \
    get_feature_from_gene_ids, three_frame_translation, get_geneids_from_uniprot



class Test(TestCase):
    def test_get_geneids_from_uniprot(self):
        result = get_geneids_from_uniprot(["P04637"])
        assert '7157' in result


    def test_get_feature_from_gene_ids(self):
        for f in get_feature_from_gene_ids(["11047", "83394", "9677", "81029", "23277", "11336"]):
            print(f.type, f.gene_name, f.start, f.end)

    def test_create_db(self):
        db = create_db(["120892", "11047", "83394"])
        gene = db.get_gene("LRRK2")
        print(gene.blocks)
        assert gene.gene_name == "LRRK2"

    def test_shuffle_blocks(self):
        db = create_db(["11047"])
        gene = db.get_gene("ADRM1")
        data = [i for i in gene.shuffle_blocks()]
        assert len(data) == 511
        for d in data:
            print(d.translate(to_stop=True))

    def test_three_frame_translation(self):
        db = create_db(["11047"])
        gene = db.get_gene("ADRM1")
        data = [three_frame_translation(i.seq, only_start_at_atg=True) for i in gene.shuffle_blocks()]
        print(data)

    def test_shuffle_blocks(self):
        db = create_db(["11047"])
        gene = db.get_gene("ADRM1")
        data = [i for i in gene.shuffle_blocks(include_intron=True)]
        assert len(data) == 262143



