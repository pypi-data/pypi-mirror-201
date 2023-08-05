import io
import sqlite3
from typing import List, Generator, Set
import pandas as pd
from Bio import SeqIO, Seq, Entrez, SeqRecord
from itertools import product, compress
from uniprotparser.betaparser import UniprotParser
Entrez.email = "tphung001@dundee.ac.uk"


def  get_geneids_from_uniprot(uniprot_accs: Set[str]|List[str]) -> Set[str]:
    # Get gene ids from uniprot accession ids using uniprot REST api
    parser = UniprotParser(columns="accession,id,gene_names,protein_name,organism_name,organism_id,length,xref_refseq,xref_geneid")
    results = []
    for i in parser.parse(ids=uniprot_accs):
        results.append(pd.read_csv(io.StringIO(i), sep="\t"))

    if len(results) > 1:
        results = pd.concat(results, ignore_index=True)
    else:
        results = results[0]

    gene_ids = set()
    print(results.columns)
    for i in results["GeneID"]:
        if pd.notnull(i):
            arr = i.split(";")
            if len(arr) > 0:
                gene_ids.add(arr[0].strip())
    return gene_ids

def translate(seq: str | Seq.Seq, only_start_with_codons = ["ATG"]):
    seq_length = len(seq)
    if only_start_with_codons:
        for c in range(0, seq_length, 3):
            if c + 3 <= seq_length:
                if str(seq[c: c + 3]).upper() in only_start_with_codons:
                    return Seq.translate(seq[c: seq_length], to_stop=True)

def three_frame_translation(seq: str | Seq.Seq, reverse: bool = False, only_start_with_codons = ["ATG"]):
    # Translate a sequence into all 3 frames
    """

    :param seq: dna or rna sequence
    :param reverse: whether to reverse complement the sequence
    :param only_start_with_codons: whether or not to only start translation with these codons
    :return: a dictionary of frames and translated sequences
    """
    if reverse:
        seq = Seq.Seq(seq).reverse_complement()
    else:
        seq = Seq.Seq(seq)
    length = len(seq)
    frames = {}
    for i in range(0, 3):
        fragment_length = 3 * ((length - i) // 3)
        start_pos = i
        if only_start_with_codons:
            for c in range(i, i + fragment_length, 3):
                if c + 3 <= i + fragment_length:
                    if str(seq[c: c+3]).upper() in only_start_with_codons:
                        start_pos = c
                        break
            if start_pos != c:
                continue
        frames[i + 1] = Seq.translate(seq[start_pos: i + fragment_length], to_stop=True)
    return frames


class BaseTranscriptBlock:
    # Base class for Exon and Intron
    def __init__(self, seq: str | Seq.Seq = "", start: int = None, end: int = None, position=0):
        if type(seq) == str:
            self.seq = Seq.Seq(seq)
        else:
            self.seq = seq
        self.start = start
        self.end = end
        self.position = 0
        self.strand = 1
        self.gene_name = ""

    def __str__(self):
        return f"{str(self.start)}--{self.end}"

    def __repr__(self):
        return f"{str(self.start)}--{self.end}"


class Exon(BaseTranscriptBlock):
    # Exon class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "exon"
        self.transcript_name = ""
        self.genomic_start = 0
        self.genomic_end = 0

    def __str__(self):
        return f"Exon: {str(self.start)}--{self.end}"

    def __repr__(self):
        return f"Exon: {str(self.start)}--{self.end}"


class Intron(BaseTranscriptBlock):
    # Intron class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "intron"
        self.transcript_name = ""
        self.genomic_start = 0
        self.genomic_end = 0

    def __str__(self):
        return f"Intron: {str(self.start)}--{self.end}"

    def __repr__(self):
        return f"Intron: {str(self.start)}--{self.end}"


class Gene:
    # Transcript class that hold the entire transcript sequence and its blocks of exons and introns
    def __init__(self, seq: str | Seq.Seq, start: int = None, end: int = None, gene_name=""):
        self.seq = seq
        self.start = start
        self.end = end
        self.gene_name = gene_name
        self.blocks: List[Exon | Intron] = []
        self.block_count = 0
        self.type = "gene"


    def __str__(self):
        return f"Gene: {str(self.start)}-{self.seq}-{self.end}"

    def __repr__(self):
        return f"Gene: {str(self.start)}-{self.seq}-{self.end}"

    def add_block(self, block: Exon | Intron):
        # Add a block to the transcript
        block.position = self.block_count
        self.blocks.append(block)
        self.block_count += 1

    def shuffle_blocks(self, include_intron: bool = False):
        # Shuffle the blocks of the transcript using different combinations of exons and introns
        # This is used to generate different isoforms from the same transcript
        blocks = self.blocks[:]
        if not include_intron:
            blocks = [b for b in self.blocks if b.type == "exon"]
        for i in product([0, 1], repeat=len(blocks)):
            seq = []
            id = []
            for b in list(compress(blocks, i)):
                seq.append(str(b.seq))
                id.append(f"{b.start}-{b.end}")
            if len(seq) > 0:
                yield SeqRecord.SeqRecord(Seq.Seq("".join(seq)), id=".".join(id), name=self.gene_name)


    def fill_intron(self, transcript=None):
        # Fill in the introns of the transcript
        blocks = []
        if transcript is not None:
            self.transcript = transcript
        for i in range(1, len(self.blocks)):
            blocks.append(self.blocks[i - 1])
            if self.blocks[i].type == "exon" and self.blocks[i - 1].type == "exon":
                intron = Intron(start=self.blocks[i - 1].end, end=self.blocks[i].start)
                intron.seq = Seq.Seq(str(self.seq)[self.blocks[i - 1].end - self.start:self.blocks[i].start - self.start])
                blocks.append(intron)
        if len(blocks) != len(self.blocks):
            self.blocks = blocks[:]
            self.block_count = len(blocks)


class Transcript(Gene):
    def __init__(self, seq: str | Seq.Seq, start: int = None, end: int = None, transcript_name=""):
        super().__init__(seq, start, end)
        self.type = "transcript"
        self.transcript_name = transcript_name

    def __str__(self):
        return f"Transcript: {str(self.start)}-{self.seq}-{self.end}"

    def __repr__(self):
        return f"Transcript: {str(self.start)}-{self.seq}-{self.end}"


class GeneDatabase:
    # An object for storing and accessing the gene, exon and intron data

    def __init__(self):
        # a sqlite database to store the gene, exon and intron data
        self.conn = sqlite3.connect("./db.sqlite3")
        self.cursor = self.conn.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS gene")
        self.cursor.execute("DROP TABLE IF EXISTS exon")
        #self.cursor.execute("DROP TABLE IF EXISTS transcript")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS gene (id TEXT PRIMARY KEY, seq TEXT, start INTEGER, end INTEGER, strand INTEGER)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS exon (gene_name TEXT, seq TEXT, start INTEGER, end INTEGER, strand INTEGER, genomic_start INTEGER, genomic_end INTEGER, transcript_name TEXT)")
        #self.cursor.execute("CREATE TABLE IF NOT EXISTS transcript (id TEXT PRIMARY KEY, seq TEXT, start INTEGER, end INTEGER, strand INTEGER, gene_name TEXT)")

    def add_gene(self, gene: Gene):
        self.cursor.execute("INSERT INTO gene VALUES (?, ?, ?, ?, ?)", (gene.gene_name, str(gene.seq), gene.start, gene.end, gene.strand))
        self.conn.commit()

    def add_exon(self, exon: Exon):
        self.cursor.execute("INSERT INTO exon VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (exon.gene_name, str(exon.seq), exon.start, exon.end, exon.strand, exon.genomic_start, exon.genomic_end, exon.transcript_name))
        self.conn.commit()

    #def add_transcript(self, transcript):
    #    self.cursor.execute("INSERT INTO transcript VALUES (?, ?, ?, ?, ?, ?)", (transcript.transcript_name, str(transcript.seq), transcript.start, transcript.end, transcript.strand, transcript.gene_name))

    def get_gene(self, gene_name: str):
        gene_rec = self.cursor.execute("SELECT * FROM gene WHERE id=?", (gene_name,)).fetchone()
        gene = Gene(seq=gene_rec[1], start=gene_rec[2], end=gene_rec[3], gene_name=gene_rec[0])
        gene.strand = gene_rec[4]
        #transcript_rec = self.cursor.execute("SELECT *, length(seq) seq_length FROM transcript WHERE gene_name=? order by seq_length desc LIMIT 1", (gene_name,)).fetchone()
        #transcript = Transcript(seq=Seq.Seq(transcript_rec[1]), start=transcript_rec[2], end=transcript_rec[3], transcript_name=transcript_rec[0])

        exon_recs = self.cursor.execute("SELECT * FROM exon WHERE gene_name=?", (gene_name,)).fetchall()
        for exon_rec in exon_recs:
            exon = Exon(start=exon_rec[2], end=exon_rec[3])
            exon.gene_name = exon_rec[0]
            exon.seq = Seq.Seq(exon_rec[1])
            exon.strand = exon_rec[4]
            gene.add_block(exon)
        gene.fill_intron()
        return gene

    def remove_duplicates(self):
        self.cursor.execute("DELETE FROM exon WHERE EXISTS( SELECT 1 FROM exon AS e2 WHERE e2.start = exon.start AND e2.end = exon.end AND e2.gene_name = exon.gene_name AND e2.rowid > exon.rowid)")
        self.conn.commit()

    def iterate_genes(self):
        gene_recs = self.cursor.execute("SELECT * FROM gene").fetchall()
        for gene_rec in gene_recs:
            yield self.get_gene(gene_rec[0])


def get_gene_from_geneid(gene_ids: List[str] | Set[str], interval = 100):
    # create input string from gene id list with 100 gene ids per string
    gene_count = len(gene_ids)
    results = []
    gene_ids = list(gene_ids)
    for i in range(0, gene_count, interval):
        gene_id_str = ",".join(gene_ids[i:i + interval])
        results.append(gene_id_str)
    leftover = gene_count % interval
    if leftover > 0 and gene_count > interval:
        gene_id_str = ",".join(gene_ids[-leftover:])
        results.append(gene_id_str)

    fin_df = []

    for r in results:
        print(f"Getting gene info from NCBI with {r}")
        res = Entrez.efetch(db="gene", id=r, rettype="tabular", retmode="text")
        df = pd.read_csv(res, sep="\t")
        fin_df.append(df)

    if len(fin_df) > 1:
        fin_df = pd.concat(fin_df)
    else:
        fin_df = fin_df[0]

    return fin_df


def get_chromosome(chromosome):
    # get chromosome from NCBI and return as SeqRecord
    res = Entrez.efetch(db="nuccore", id=chromosome, rettype='gb', style='withparts')
    chr = SeqIO.read(res, "genbank")
    return chr


def get_gene_table(gene_id: str):
    e = Entrez.efetch(db="gene", id=gene_id, rettype="gene_table", retmode="text")
    for line in e:
        if line.startswith("Exon table"):
            break

def get_gene_report(gene_id: str):
    e = Entrez.efetch(db="gene", id=gene_id, rettype="xml", retmode="text")
    res = Entrez.read(e)
    return res[0]


def get_refseqgene_acc_from_report(gene_report):
    # get refseq gene accession from gene report
    return gene_report["Entrezgene_locus"][1]["Gene-commentary_accession"] + "." + gene_report["Entrezgene_locus"][1]["Gene-commentary_version"]

def get_refseqgene_gb_from_ncbi(refseqgene_acc):
    # get refseq gene genbank from accession
    res = Entrez.efetch(db="nuccore", id=refseqgene_acc, rettype="gb", retmode="text")
    return SeqIO.read(res, "genbank")


def get_feature_from_gene_ids(gene_ids: List[str] | Set[str]):
    """
    Get gene features from gene ids
    :param gene_ids: list or set of gene id strings
    :return: Generator of Gene and Exon objects from SeqFeatures
    """
    assert len(gene_ids) > 0, "gene_ids must be a list or set of gene ids with more than 0 elements"
    gene_df = get_gene_from_geneid(gene_ids)
    gene_symbol_set = set(gene_df["Symbol"].values)
    for g in gene_ids:
        report = get_gene_report(g)
        if report is not None:
            refseqgene_acc = get_refseqgene_acc_from_report(report)
            refseqgene_gb = get_refseqgene_gb_from_ncbi(refseqgene_acc)
            print(refseqgene_acc)
            for f in refseqgene_gb.features:
                if f.type == "gene":
                    if f.qualifiers["gene"][0] not in gene_symbol_set:
                        continue
                    gene = Gene(seq=str(refseqgene_gb.seq)[f.location.start:f.location.end], start=f.location.start, end=f.location.end)
                    gene.strand = f.location.strand
                    gene.gene_name = f.qualifiers["gene"][0]
                    yield gene

                elif f.type == "exon":
                    if f.qualifiers["gene"][0] not in gene_symbol_set:
                        continue
                    exon = Exon(seq=str(refseqgene_gb.seq)[f.location.start:f.location.end], start=f.location.start, end=f.location.end)
                    exon.strand = f.location.strand
                    exon.gene_name = f.qualifiers["gene"][0]
                    yield exon



def create_db(gene_ids: List[str] | Set[str], entrez_email: str = ""):
    """
    Create a gene database from a list of gene ids
    :param gene_ids: list or set of gene id strings
    :return: database object that can be used to retrieve exon and gene information
    """
    if entrez_email != "":
        Entrez.email = entrez_email
    db = GeneDatabase()
    for rec in get_feature_from_gene_ids(gene_ids):
        #print(rec.type, rec.start, rec.end, rec.gene_name)
        if rec.type == "exon":
            db.add_exon(rec)
        elif rec.type == "gene":
            db.add_gene(rec)
        #elif rec.type == "transcript":
        #    db.add_transcript(rec)

    # db.remove_duplicates()

    return db
