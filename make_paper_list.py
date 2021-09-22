
import os
from glob import glob

import pandas as pd


class PaperSummary:
    def __init__(self, md_filepath):
        self.md_filepath = md_filepath

        self.columns = []
        self.summary_dict = {}

        self.add_paper_index()
        self.md2dict()

        self.__key = None

    def get_columns(self):
        return self.columns

    def get_summary_dict(self):
        return self.summary_dict

    def get_md_txt_lines(self):
        with open(self.md_filepath, 'r', encoding='utf8') as f:
            md_txt_lines = f.readlines()
        return md_txt_lines

    def add_paper_index(self):
        key = '文献番号'
        self.columns.append(key)
        value = os.path.basename(self.md_filepath.split('_')[0])
        self.summary_dict[key] = value

    def md2dict(self):
        txt_lines = self.get_md_txt_lines()
        for line_num ,line in enumerate(txt_lines):
            line_num += 1
            if line=='---\n':break
            try:
                self.md2dict_line(line)
            except:
                print('')
                print(f'Error Occured while transform markdown file: {self.md_filepath}')
                print(f'    line number: {line_num}')
                print(f'    txt: {line}')
                import traceback
                traceback.print_exc()

    def md2dict_line(self, line):
        if line.replace(' ', '').replace('\n', '')=='':
            return
        if line[:3]=='## ':
            key = line[3:].replace('\n', '')
            self.columns.append(key)
            self.summary_dict[key] = ''
            self.__key = key
            return
        self.summary_dict[self.__key] += line


def make_paper_list_csv(src_md_filepath_expression='summary/*/summary.md',
                        dst_csv_filepath='paper_summary.csv'):
    md_filepath_list = glob(src_md_filepath_expression)

    print(f'MarkDown files:')
    print(md_filepath_list)
    print('')

    summary_df = pd.DataFrame()

    for filepath in md_filepath_list:
        summary = PaperSummary(filepath)
        summary_dict = summary.get_summary_dict()
        summary_df = summary_df.append(summary_dict, ignore_index=True)

    summary_df.to_csv(dst_csv_filepath, index=None, line_terminator='\r\n', encoding='utf8')
    print(f'CSV format paper list file is made in {os.path.abspath(dst_csv_filepath)}')


if __name__ == '__main__':
    make_paper_list_csv()
