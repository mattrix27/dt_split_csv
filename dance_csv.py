import pandas as pd
import numpy as np
import os
import sys
from zipfile import ZipFile 

def parse_csv(csv_path, path='', zip_file=None):
    pref_dic = {}
    pref_df = pd.read_csv(csv_path, names=['#', 'Pref', 'Name', 'Desired', 'Dance Name'])
    pref_np = pref_df.values
    indexes = np.where(pref_np == "#")

    last_i = 1
    for index in indexes[0]:
        #print(index)
        if index != last_i:
            dance_df = pref_df.iloc[last_i-1:index-1, :]
            dance_name = dance_df.at[last_i+1, "Dance Name"]
            pref_title = get_type(dance_df.at[last_i-1, "#"])

            write_to_csv(dance_df, dance_name, pref_title, path, zip_file)
            pref_dic = update_prefs(pref_dic, dance_df, dance_name, pref_title)

        last_i = index
    dance_df = pref_df.iloc[index-1:, :]
    dance_name = dance_df.at[last_i+1, "Dance Name"]
    pref_title = get_type(dance_df.at[last_i-1, "#"])

    write_to_csv(dance_df, dance_name, pref_title, path, zip_file)
    pref_dic = update_prefs(pref_dic, dance_df, dance_name, pref_title)

    return pref_dic

def update_prefs(pref_dic, dance_df, dance_name, pref_title):
    if dance_name not in pref_dic:
        pref_dic[dance_name] = {}

    pref_type = ""
    if "Number" in pref_title:
        pref_type = "audition"
    elif "Pref" in pref_title:
        pref_type = "pref"

    pref_dic[dance_name][pref_type] = dance_df
    return pref_dic

def write_to_csv(df, d_name, d_type, path, zip_file):
    file_name = d_name + '_' + d_type + '.csv'
    file_path = path + file_name
    df.to_csv(file_path, header=False, index=False)
    if zip_file:
        with ZipFile(zip_file,'a') as zip:
            print("writing " + file_path)
            zip.write(file_path)

def get_type(pref_title):
    if "audition" in pref_title.lower():
        return "audition"
    elif "pref" in pref_title.lower():
        return "pref"
    else:
        return pref_title

#example call python3 dance_csv.py dance-audition-sheets-2.csv test/ spam.zip

def main():
    filename = sys.argv[1]
    path = sys.argv[2]
    zip_file = sys.argv[3]
    parse_csv(filename, path, zip_file)

if __name__ == "__main__":
    main()