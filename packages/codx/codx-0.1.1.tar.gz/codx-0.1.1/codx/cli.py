import codx.components as cc
import click

@click.command()
@click.argument("ids", required=True)
@click.option("--output", "-o", default="output.fasta", help="Output file")
@click.option("--include-intron", "-i", is_flag=True, help="Include intron")
@click.option("--uniprot", "-u", is_flag=True, help="Input is Uniprot accession ids")
@click.option("--translate", "-t", is_flag=True, help="Translate to protein")
@click.option("--three-frame-translation", "-3", is_flag=True, help="Translate to protein in 3 frames")
@click.option("--six-frame-translation", "-6", is_flag=True, help="Translate to protein in 6 frames (3 forward and 3 reverse complement)")
def main(ids, output, include_intron, uniprot, translate, three_frame_translation, six_frame_translation):
    if uniprot:
        ids = cc.get_geneids_from_uniprot(ids.split(","))
    else:
        ids = ids.split(",")
    print(ids)
    db = cc.create_db(ids)
    with open(output, "wt") as fasta:
        for gene in db.iterate_genes():
            for combination in gene.shuffle_blocks(include_intron=include_intron):
                header = f">{gene.gene_name}.{combination.id}"
                seq = combination.seq
                if translate:
                    seq = cc.translate(seq)
                    if not seq:
                        continue
                    fasta.write(f"{header}\n{seq}\n")
                elif three_frame_translation:
                    results = cc.three_frame_translation(seq)
                    for frame in results:
                        fasta.write(f"{header}.frame-{frame}\n{results[frame]}\n")
                elif six_frame_translation:
                    results = cc.three_frame_translation(seq)
                    for frame in results:
                        fasta.write(f"{header}.frame-{frame}\n{results[frame]}\n")
                    results = cc.three_frame_translation(seq, reverse=True)
                    for frame in results:
                        fasta.write(f"{header}.frame-reverse-{frame}\n{results[frame]}\n")
                else:
                    fasta.write(f"{header}\n{seq}\n")
                