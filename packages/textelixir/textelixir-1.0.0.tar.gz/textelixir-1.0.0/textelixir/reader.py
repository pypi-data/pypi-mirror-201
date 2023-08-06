from glob import glob
import pandas as pd
import io

def read_tsv(filename):
    data = pd.read_csv(filename, sep='\t', header=0, index_col=None)
    columns = list(data.columns)

    if 'text' not in columns:
        raise Exception('`text` column needs to be in TSV column headers.')
    columns.remove('text')

    return columns, data


def read_txt(filename):
    with io.open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        data = pd.DataFrame({'filename': [filename for i in range(0, len(lines))], 'text': [line for line in lines]})
    
    return ['filename'], data


def read_glob_txt(filename_glob):
    data_dict = {}
    for filename in filename_glob:
        with io.open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            data_dict['filename'].extend([filename for i in range(0, len(lines))])
            data_dict['text'].extend(lines)
            data = pd.DataFrame(data_dict)

    return ['filename'], data

def read_docx(filename):
    pass
