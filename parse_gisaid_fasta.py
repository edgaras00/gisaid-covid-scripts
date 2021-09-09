from Bio import SeqIO
import argparse


def main():

    # CLI arguments
    parser = argparse.ArgumentParser(
        description='Script that parses GISAID FASTA files and formats headers'
    )

    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='Input FASTA file'
    )

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='gisaid_output.fasta',
        help='Output path'
    )

    args = parser.parse_args()

    # Parse seqs
    seqs = list(SeqIO.parse(args.input, 'fasta'))

    for seq in seqs:
        header = seq.name.split('|')[-2]
        seq.id = header
        seq.name = header
        seq.description = header

    SeqIO.write(seqs, args.output, 'fasta')
    return

if __name__== '__main__':
    main()