#!/usr/bin/env python3

import csv
import os
import pandas as pd
from pathlib import Path
import sys

def get_macula_df(file, sep="\t"):
    macula_df = pd.read_csv(file, dtype=str, sep=sep)
    macula_df.fillna('', inplace=True)
    
    return macula_df

def load_macula_data(file):
    
    csv.register_dialect('default')
        
    #fieldnames  = ["ref", "Original unicode", "Hebrew Original", "Aramaic Original", "Greek Original", "Greek lemma", "Greek normalized", "Greek gloss", "English gloss", "Mandarin gloss"]
    
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i,row in enumerate(reader):
           if i == 0:
               fieldnames = row.split("\t")
               print(f"fieldnames are : {fieldnames}")
           
    return 
    

def get_name_matrix(folder):
    
    all_names = dict()
    
    folder = Path(folder)
    files = sorted(folder.glob(r'*'))
    #print([file.name[0:3] for file in files])
    
    for file in files:
        with open(file, 'r', encoding='utf-8') as fin:
            names = [name.strip('\n').title() for name in fin.readlines()]
            all_names[file.name] = names   
    
    return all_names

def get_matches(source_df, source_column , target_values):
    matches = []
    non_matches = []
    fixed_matches = dict()
    
    source_values = set(source_df[source_column])
    for target_value in set(target_values):
       if target_value in source_values:
           matches.append(target_value)
       else:
           non_matches.append(target_value)
    
    for non_match in sorted(non_matches):
        # print(f"Try to match {non_match}")
        
        for source_value in source_values:
                                        
            #First try splitting into single words
            try:
                source_words = source_value.split(' ')                    
                if non_match in source_words:
                    if non_match in fixed_matches :
                        fixed_matches[non_match].append(source_value)
                        #print(f"\nLooking for {non_match}.  Found it in {source_words}.\n{fixed_matches[non_match]}\n")
                    else :    
                        fixed_matches[non_match] = [source_value]
                        #print(f"Added to match {fixed_matches[non_match]}")
                        
            except ValueError:
                continue
                
    # Remove newly matched from non_matches    
    not_matched = [non_match for non_match in non_matches if non_match not in fixed_matches.keys()]
            
    
    return matches, not_matched, fixed_matches

if __name__ == '__main__':
    
    data_folder = Path("D:/GitHub/trabina/data") 
    by_lang_folder = data_folder / "by-lang"
    english_names_file = by_lang_folder / "eng"
    
    macula_data_tsv = data_folder / "macula_names.tsv"
    macula_df = get_macula_df(macula_data_tsv)
    
    #print(macula_df.columns)
    #Index(['ref', 'Original unicode', 'Hebrew Original', 'Aramaic Original', 'Greek Original', 'Greek lemma', 'Greek normalized', 'Greek gloss', 'English gloss', 'Mandarin gloss']
      

    
    
    #load_macula_data(macula_data_tsv)
    #english_jhu_names = get_english_names(english_names_file)
    #jhu_dict = dict("English": english_jhu_names)
    
    #print(f"JHU dataframe is:\n{jhu_df}")
    
    #Get all the names and make a dataframe
    all_jhu_names = get_name_matrix(by_lang_folder)
    jhu_df = pd.DataFrame.from_dict(all_jhu_names, dtype=str)
    
    # Make the English name the index
    jhu_df.set_index('eng', inplace=True)
      
    #print(jhu_df.index)
    #for name in jhu_df.index:
    #    print(name)
        
    #Match up the JHU English names with the Macula English Glosses    
    matches, non_matches, fixed_matches = get_matches(macula_df, "English gloss",jhu_df.index)
    
    print(f"\nNo matches were found for these {len(non_matches)} words.")
    print(non_matches)
    

