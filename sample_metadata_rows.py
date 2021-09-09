import pandas as pd
import argparse


def open_file(path):
    '''Function to open GISAID metadata file'''
    df = pd.read_csv(path, sep='\t')
    return df


def sample_rows(df, n, random_state=42):
    '''Function that randomly samples n rows from input DataFrame'''

    sample = df.sample(n, random_state=random_state)
    return sample


def output_file(df, path, output_accession=0):
    '''
     Function that writes output to a .tsv file.

     It can also output a separate .tsv file
     for accession ids.

    '''
    df.to_csv(path, sep='\t', index=False)
    if output_accession:
        df.accession_id.to_csv(
            'acc-sample.tsv',
            sep='\t',
            index=False,
            header=False
        )


def main():

    # Command line arguments
    parser = argparse.ArgumentParser(
        description='''Script that randomly samples n rows 
                       from a GISAID metadata file'''
    )

    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='Path to GISAID metadata file'
    )

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='Output path'
    )

    parser.add_argument(
        '-n',
        '--num_samples',
        type=int,
        help='Number of samples'

    )

    parser.add_argument(
        '-a',
        '--acc',
        type=int,
        default=0,
        choices=[0, 1],
        help='Output accession ID file (1 = True, 0 = False)'

    )

    args = parser.parse_args()

    metadata = open_file(args.input)
    sample = sample_rows(metadata, args.num_samples)
    output_file(sample, args.output, args.acc)
    return


if __name__ == '__main__':
    main()
