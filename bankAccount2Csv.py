# みずほの入出金帳票のPDFをCSVに変換する

from argparse import ArgumentParser
import sys
import os
import glob
import json

import numpy
import pandas as pd
import tabula
import csv

DEFAULT_DIRECTORY = "."

MAPFILE = "./expenditure_item_map.json"
HEADER = ["月", "出金額", "入金額", "取引先", "費目"]

def parser():
    usage = 'python {} [-d directory] [--help]'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('-d', '--directory', type=str, default=DEFAULT_DIRECTORY, help='directory to read')
    args = argparser.parse_args()
    return args


def read_parse_pdf(file_path: str):
    # lattice=Trueでテーブルの軸線でセルを判定
    dfs = tabula.read_pdf(file_path, lattice=True, pages = 'all')
    #print(dfs[0].iloc[:, [0,1,2,3,8]])

    lines = list()
    for df in dfs:
        for ln in df.to_numpy().tolist():
            if ln[0] is numpy.NAN: continue
            for i in [0, 2, 3, 8]:
                if ln[i] is numpy.NAN: ln[i] = ""
                ln[i] = ln[i].replace("\n", "").replace("\r", "").replace(",", "")
            for i in [2, 3]:
                if ln[i] != "": ln[i] = int(ln[i])
            lines.append([ln[0], ln[2], ln[3], ln[8]])
    return lines


if __name__ == "__main__":
    args = parser()
    if args.directory is None:
        print("*** -d option is mandatory")
        sys.exit(1)

    months = dict()
    try:
        with open(MAPFILE, "r") as f:
            maps = json.load(f)
    except:
        maps = dict()

    for filepath in glob.glob(os.path.join(args.directory, "*.pdf")):
        print("** processing:", filepath)
        lines = read_parse_pdf(filepath)
        mon = lines[0][0].split("/")[0]
        months[f"{mon}月"] = lines
        for ln in lines:
            ln[0] = mon
            if ln[3] not in maps:
                maps[ln[3]] = ""
            ln.append(maps[ln[3]])

    os.makedirs("results", exist_ok=True)
    for mon in months.keys():
        with open(os.path.join("results", f"{mon}.csv"), 'w', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
            for row in months[mon]:
                writer.writerow(row)

    tmp = list()
    for mon in months.keys():
        for row in months[mon]:
            tmp.append(row)
    df = pd.DataFrame(tmp, columns=HEADER)
    df.to_excel(os.path.join("results", "全結合データ.xlsx"), sheet_name='sheet1', index=False)

    with open(MAPFILE, "w", encoding="utf-8") as f:
        json.dump(maps, f, ensure_ascii=False, indent=4)
