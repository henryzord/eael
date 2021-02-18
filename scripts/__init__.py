import json

import numpy as np
import pandas as pd


def __recursive_search__(fragment):
    if isinstance(fragment, dict):
        names = []
        for sub_name, sub_data in fragment.items():
            names += __recursive_search__(sub_data)
        return names
    elif isinstance(fragment, list):
        return fragment
    return [fragment]


def __get_citations__(json_file):
    names = __recursive_search__(json_file)
    return list(set(names))


def load_data(path_data):
    tables = dict()
    with open(path_data, 'r', encoding='utf-8') as fh:
        data = json.load(fh)    

        bibtex = __get_citations__(data)

        for field_name, field_value in data.items():
            some_data = next(iter(field_value.values()))

            if isinstance(some_data, list):
                df = pd.DataFrame(data=False, index=bibtex, columns=field_value.keys(), dtype=np.bool)
                for column, list_bibtex in field_value.items():
                    df.loc[list_bibtex, column] = True
            elif isinstance(some_data, dict):
                columns = []
                for super_name, super_data in field_value.items():
                    for sub_name, sub_data in super_data.items():
                        columns += [(super_name, sub_name)]

                columns = pd.MultiIndex.from_tuples(columns, names=['super', 'sub'])

                df = pd.DataFrame(data=False, columns=columns, index=bibtex, dtype=np.bool)
                for super_name, super_data in field_value.items():
                    for sub_name, sub_data in super_data.items():
                        df.loc[sub_data, (super_name, sub_name)] = True
            else:
                raise TypeError('unknown data type.')

            tables[field_name] = df

    return tables
