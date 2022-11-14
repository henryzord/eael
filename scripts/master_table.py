import json
import pandas as pd
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from pylatexenc.latex2text import LatexNodes2Text


def render_author_names(string):
    text = render_bibtex(string)
    molecules = text.split(' and ')
    rendered = []
    et_al = False
    for particle in molecules:
        particle = particle.strip()
        if particle == 'others':
            rendered += ['et al.']
            et_al = True
            break

        this_author = []
        atoms = particle.split(',')
        last_name = atoms[0].strip()
        other_names = atoms[-1].split(' ')
        for name in other_names:
            if len(name) > 0:
                this_author += [name.strip()[0]]
        this_author += [last_name]
        rendered += [' '.join(this_author)]

    if not et_al:
        return ', '.join(rendered)
    return ' '.join(rendered)

def render_bibtex(string):
    text = LatexNodes2Text().latex_to_text(string)
    return text


def build_dataframe(d: dict) -> pd.DataFrame:
    composed = dict()

    for category, v1 in d.items():
        # v1 is always a dict at this level
        for value, v2 in v1.items():
            # if there is only one level of taxonomy
            if isinstance(v2, list):
                for ref in v2:
                    if ref not in composed:
                        composed[ref] = dict()

                    if category in composed[ref]:
                        composed[ref][category] = composed[ref][category] + ', ' + value
                    else:
                        composed[ref][category] = value

            # else if there is another level
            elif isinstance(v2, dict):
                for subcategory, reflist in v2.items():
                    for ref in reflist:
                        if ref not in composed:
                            composed[ref] = dict()

                        if category in composed[ref]:
                            composed[ref][category] = composed[ref][category] + ', ' + subcategory
                        else:
                            composed[ref][category] = value + ': ' + subcategory

    df = pd.DataFrame(composed).T
    return df


def build_html_table(df: pd.DataFrame, refs: BibDatabase) -> str:
    string = '''<table id="master_table">\n'''

    string += '\t<tr>\n'
    string += '\t\t<th onclick="sortTable(0)">Authors</th>\n\t\t<th onclick="sortTable(1)">Title</th>\n'
    for i, column in enumerate(df.columns):
        string += '\t\t<th onclick="sortTable({0})">'.format(i + 2) + column + '</th>\n'
    string += '\t</tr>\n'

    for i, row in df.iterrows():
        string += '\t<tr>\n'
        string += '\t\t<td>' + render_author_names(refs.entries_dict[row.name]['author']) + '</td>\n'
        string += '\t\t<td>' + render_bibtex(refs.entries_dict[row.name]['title'][1:-1]) + '</td>\n'
        string += '\n'.join(['\t\t<td>' + str(x) + '</td>' for x in row])
        string += '\t</tr>\n'

    string += '''\t</table>\n'''
    return string


def main(data_path, bibliography_path, template_path, write_path):
    with \
            open(data_path, 'r') as references_file, \
            open(bibliography_path, 'r') as refs_file, \
            open(template_path, 'r') as template_file, \
            open(write_path, 'w', encoding='utf-8') as write_file:
        data = json.load(references_file)  # type: dict
        df = build_dataframe(data)

        refs = bibtexparser.load(refs_file)
        html_table = build_html_table(df, refs)
        template_file_lines = ''.join(template_file.readlines())
        master_table = template_file_lines.replace('{{ master_table }}', html_table)

        write_file.write(master_table)


if __name__ == '__main__':
    main(
        data_path='../data.json',
        bibliography_path='../bibliography.bib',
        template_path='../templates/master_table_template.html',
        write_path='../master_table.html'
    )
