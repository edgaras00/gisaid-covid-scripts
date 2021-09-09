import pandas as pd
import argparse


def open_file(path):
    '''Function to open GISAID metadata file.'''
    metadata = pd.read_csv(path, sep='\t')
    return metadata


def filter_by_date(df, start=None, end=None):
    '''Function that filters the GISAID DataFrame by date interval'''
    if not start and not end:
        return df
    if not start and end:
        filtered_df = df[df['Submission date'] < end]
        return filtered_df
    if start and not end:
        filtered_df = df[df['Submission date']>= start]
        return filtered_df
    if start and end:
        filtered_df = df[
            (df['Submission date'] >= start)
            &
            (df['Submission date'] < end)
        ]
        return filtered_df

def filter_by_host(df):
    '''Function to filter out non-human hosts'''
    return df[df.Host == 'Human']


def get_country(df):
    '''Function that creates a country column'''
    df['country'] = df.Location.str.split(' / ').str[1]
    return df

def filter_columns(df):
    '''Function that takes the relevant columns and formats column names'''
    # Rename columns
    print(df.columns)
    df = df.rename(columns={
        'Accession ID': 'accession_id',
        'Virus name': 'virus_name',
        'Collection date': 'collection_date',
        'Location': 'location',
        'Additional location information': 'additional_location_information',
        'Patient age': 'patient_age',
        'Gender': 'gender',
        'Submission date': 'submission_date',
        'Variant': 'variant',
        'Pango lineage': 'pango_lineage'
    })
    # Order columns
    df_ordered = df[[
        'accession_id',
        'virus_name',
        'collection_date',
        'country',
        'location',
        'additional_location_information',
        'patient_age',
        'gender',
        'submission_date',
        'variant',
        'pango_lineage'
    ]]
    return df_ordered


def output_file(df, path, output_accession=0):
    '''
        Function that writes output to a .tsv file.

        It can also output a separate .tsv file
        for accession ids.
    '''
    df.to_csv(path, sep='\t', index=False)
    if output_accession:
        df.accession_id.to_csv('acc.tsv', sep='\t',
                               index=False, header=False)


def main():

    # Command line arguments
    parser = argparse.ArgumentParser(
        description='GISAID metadata parser'
    )

    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='Path to GISAID metadata .tsv file'
    )

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='Output path'
    )

    parser.add_argument(
        '-s',
        '--start',
        type=str,
        default=None,
        help='Starting submission date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '-e',
        '--end',
        type=str,
        default=None,
        help='Last submission date (YYYY-MM-DD)'
    )

    parser.add_argument(
        '-a',
        '--acc',
        type=int,
        default=0,
        choices=[0,1],
        help='Output accession ID file (1 = True, 0 = False)'
    )
    args = parser.parse_args()
    metadata = open_file(args.input)
    metadata = filter_by_date(metadata, args.start, args.end)
    metadata = filter_by_host(metadata)
    metadata = get_country(metadata)
    metadata = filter_columns(metadata)
    output_file(metadata, args.output, args.acc)
    return

if __name__ == '__main__':
    main()


