#!/usr/bin/env python3

import csv
from collections import Counter
import numpy as np
import os
import pandas as pd
from pathlib import Path
import sys

def get_macula_df(file, sep="\t"):

    # Load the 
    macula_df = pd.read_csv(file, dtype=str, sep=sep)
    macula_df.fillna('', inplace=True)
    
    #print(macula_df)
    
    #Index(['ref', 'Original unicode', 'Hebrew Original', 'Aramaic Original', 'Greek Original', 'Greek lemma', 'Greek normalized', 'Greek gloss', 'English gloss', 'Mandarin gloss']
    
    return macula_df


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
    
def get_matches(sources, targets):
    sources = set(sources)
    exact_matches = [target for target in targets if target in sources]
    non_matches   = [target for target in targets if target not in sources]
           
    return exact_matches, non_matches


    

def fix_matches_on_words(source_values,non_matches):

    still_dont_match = []

    # Get only sources with spaces:
    split_sources = [source.split(' ') for source in source_values if ' ' in source]
    sources = [source for source in source_values if ' ' in source]
    print(sources)
    exit()
    
    # Now check whether each non-match has a match:
    non_exact_matches = []
    for non_match in non_matches:
        pass

    return matches
    
if __name__ == '__main__':
    
    data_folder = Path("D:/GitHub/trabina/data") 
    by_lang_folder = data_folder / "by-lang"
    jhu_filename = "eng"
    compare_col = "English gloss"
    english_names_file = by_lang_folder / jhu_filename
    updated_macula_data_tsv = data_folder / "updated_macula_names.tsv"
    
    macula_data_tsv = data_folder / "macula_names.tsv"
    macula_df = get_macula_df(macula_data_tsv)
    
    simple_df = macula_df.drop(columns= ['ref','Hebrew Original', 'Aramaic Original', 'Greek Original'])
    print(f"\nThe simple macula dataframe has these columns:\n{simple_df.columns}")
    #print(simple_df)
    
    #Get all the names and make a dataframe
    all_jhu_names = get_name_matrix(by_lang_folder)
    jhu_df = pd.DataFrame.from_dict(all_jhu_names, dtype=str)
    
    print(f"\nThe JHU dataframe has these columns:\n {jhu_df.columns}")  
    print(jhu_df.eng)
        
    # Get the unique set of English names from both datasets.
    macula_eng_names = simple_df[compare_col].unique()
    jhu_eng_names = jhu_df.eng.unique()
    
    print(f"\nThere are {len(macula_eng_names)} unique macula_eng_names and {len(jhu_eng_names)} unique jhu_eng_names.\n")
    
    #Concatenate the two dataframes joining on exact matches of 
    # 'English gloss' and jhu_eng columns. Retain both.

    new_macula_df = pd.merge(macula_df,jhu_df, how='outer', left_on=compare_col, right_on= jhu_filename, indicator=True)
    new_macula_df = new_macula_df.rename(columns={"_merge": "matched_on_eng"})
#    new_macula_df['_merge'].cat.rename_categories({'left_only':'left_only', 'right_only':'right_only', 'both': 'matched on eng'})
#    new_macula_df['_merge'] = new_macula_df['_merge'].replace(['both'],'matched on eng')
    print(new_macula_df['matched_on_eng'])
    print(new_macula_df)
    #exit()
    
    #Select unmatched  and try to match on Greek, Hebrew or partial English matches.
    
    
    
    
    
    # Leave non-exact_matching for later.
    #print(f"\nInitially, found {len(exact_matches)} exact matches between the macula English gloss and the JHU eng name.\n There are {len(non_matches)} that don't match exactly.")
    
    #non_exact_matches = fix_matches_on_words(macula_df[compare_col],non_matches)
    
    #print(f"\nFound {len(non_exact_matches)} non exact matches between the macula English gloss and the JHU eng name.")
    #print(non_exact_matches)
    
    #print(f"\nMatches were found for these {len([match for match in matches if match ])} words.")
    
    ## Make the English name the index
    #jhu_df.set_index('eng', inplace=True)

    # Count every word.
    #word_counter = Counter()
    
    #for source in sources:
    #    word_counter.update(source)
    
    #print(len(word_counter))
    # Notice that some very common ones are names.
    # Notice that some very uncommon ones are not names.
    # Uncommon ones that aren't names tend to include common words.
    # Uncommon ones that aren't names tend to include punctuation.
    
    # The list isn't too long 309.
    
        #Match up the JHU English names with the Macula English Glosses    
    #exact_matches, non_matches = get_matches(macula_df[compare_col], jhu_eng_names)
    
    #Match up the JHU English names with the Macula English Glosses preserving the macula index.
    
    
     # Add the exact matches to the macula_data_tsv.
    # This can probably be done in one line by someone familiar with pandas.
    
    # new_col_name = "jhu_" + jhu_filename

    # macula_df["jhu_eng"] = macula_df[compare_col].isin(jhu_eng_names)
    # mask = macula_df["jhu_eng"] == True
    # macula_df.loc[mask, 'jhu_eng'] = macula_df[compare_col]
   
    # other_mask = macula_df.jhu_eng == False
    # macula_df.loc[other_mask, 'jhu_eng'] = ''
    
    # print(macula_df[[compare_col, 'jhu_eng']])

