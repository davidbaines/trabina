#!/usr/bin/env python3

from argparse import ArgumentParser
import csv
from collections import Counter
import glob
import json
import numpy as np
import os
import pandas as pd
import re
from pathlib import Path
import sys
from tqdm import tqdm 
import urllib.request

def get_bible_text_from_url(url: str) -> list:
    """
    Reads a text file from a URL, returns a list of lines.
    Inputs:
        filename:  URL or local filepath
    Outputs:
        :      Dictionary mapping semantic domains to descriptions
    """
    f = urllib.request.urlopen(filename)
    return  [line.decode('utf-8').strip('\n') for line in f.readlines()]
    
    
def get_bible_from_file(filename: str):
    """
    Reads a text file, returns a DataFrame.
    Inputs:
        filename:  Local filepath
    Outputs:
        :      DataFrame with the verses and verse references.
    """
    # Read in a Bible
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]
    
    # Convert to dictionary
    bible_dict = {vref + 1 : verse for vref,verse in enumerate(lines)}

    # Make a Dataframe from the dictionary
    bible = pd.DataFrame.from_dict(bible_dict, orient='index', dtype=str, columns=['verse'])
    
    return bible

    
def read_terms_from_json(json_file):
    
    with open(json_file, 'r', encoding = 'utf-8') as json_f:
        json_data = json.load(json_f)
        
    return pd.DataFrame(json_data)
    
    
def get_vrefs(silnlp_vref_file):    
    # Get the silnlp references to line numbers:
    with open(silnlp_vref_file, 'r', encoding='utf-8') as vrefs_file:
        vrefs_dict = {ref.strip('\n'): i+1 for i, ref in enumerate(vrefs_file.readlines())}
    
    #print(f"vrefs_dict is {vrefs_dict}")
    #try :
    #    print(f"vrefs dict contains Mark 16:99? {vrefs_dict['MRK 16:99']}")
    #except KeyError:
    #    print(f"vrefs dict doesn't contain Mark 16:99.")
    vrefs = pd.DataFrame([vrefs_dict]).T
    vrefs.rename({0:'silnlp_line_number'}, axis='columns', inplace=True)

    # To convert reference to line number get the 1st (index 0) element of the vrefs for that reference. E.g.:
    #print(vrefs.loc['ENO 1:2']['silnlp_line_number'])
    return vrefs

def df_print(df):
    print(f"The columns are {[col for col in df]}\n")
    print(df)
    return None
    
        
def main(args):

    silnlp_assets_folder = Path("D:/GitHub/davidbaines/trabina/silnlp/assets")
    silnlp_vref_file = silnlp_assets_folder / "vref.txt"
    vrefs = get_vrefs(silnlp_vref_file)
    
    pattern = 'major'

    data_folder = Path(r"D:/GitHub/davidbaines/trabina/data")
    bible_folder = Path(args.bible_folder)
    output_folder = Path(args.output_folder)
    
    terms_json_file = data_folder / f"{pattern}_terms.json"
    major = read_terms_from_json(terms_json_file)
    
    isos = {'en':'en','eng':'en', 'fr':'fr', 'fra':'fr','es':'es','id':'id'}
    valid_isos = set(isos.values())
    
    # Keep only Proper Nouns
    major = major[major.domain == 'PN']
    
    # Drop unnecessary columns
    major.drop(columns = ['sense','category','AR','DC'], inplace=True)
    
    # There are many results that don't look like names. They seem to be associated with verses in the deuterocannon.
    #Omit those for now.
    #df[df.score < 50].index
    major.drop(major[major.silnlp_line_number > 31170].index, inplace=True)
    print("This is the major terms df")
    df_print(major)
    exit()
    
    major_en = major.drop(major[major.en == ''].index)
    major_en = major_en.drop(columns=[iso for iso in valid_isos if iso != 'en'])
    
    major_fr = major.drop(major[major.fr == ''].index)
    major_fr = major_fr.drop(columns=[iso for iso in valid_isos if iso != 'fr'])
    
    major_es = major.drop(major[major.es == ''].index)
    major_es = major_es.drop(columns=[iso for iso in valid_isos if not iso == 'es'])
    
    major_id = major.drop(major[major['id'] == ''].index)
    major_id = major_id.drop(columns=[iso for iso in valid_isos if not iso == 'id'])
    
    major_iso = {'en':major_en, 'fr': major_fr, 'es':major_es, 'id':major_id}

    possible_bibles = bible_folder.glob("*.txt")
    bible_versions = {bf:bf.name[:bf.name.find('-')] for bf in possible_bibles if bf.name[:bf.name.find('-')] in isos}
    
    #print(bible_versions)

    for bible_version,iso in tqdm(bible_versions.items()):
          
        iso = isos[iso]
        
        # Choose the dataframe that has glosses for all terms in this language.
        major = major_iso[iso]
        
        output_tsv = output_folder / f"matched_{bible_version.stem}_{pattern}_names.tsv"
        #bible_url = r"https://raw.githubusercontent.com/BibleNLP/ebible-corpus/main/corpus/eng-eng-web.txt"
                      
        # Read in the Bible
        bible = get_bible_from_file(bible_version)    
        
        #Add in the verse line numbers and refs. 
        #We will join using the silnlp_line_numbers.
        # The refs will be good to check with the vrefs from the major terms list.
        bible['ref'] = vrefs.index
        bible['silnlp_line_number'] = vrefs.silnlp_line_number.values
        
        # Now drop empty verses. Must add the verse refs before this step!
        bible.drop(bible[bible.verse == ''].index, inplace=True)
        # The index of the bible and the silnlp_line_numbers should be the same throughout.
        
        #print("This is the bible df")
        #df_print(bible)    
        
        #print("This is the major terms df")
        #df_print(major)
        
        # Add the verse to the terms data
        major_bible = pd.merge(major, bible, how='inner', left_on = 'silnlp_line_number', right_on = 'silnlp_line_number')
        
        major_bible['refs_match'] = major_bible.vrefs == major_bible.ref
        
        #print("This is the major_bible df")
        #df_print(major_bible)
        
        all_refs_match = len(major_bible[major_bible.refs_match == True]) == len(major_bible)
        if not all_refs_match:
            print(f"These references don't match: {major_bible[major_bible.refs_match == False]}")
            exit()
        
        # For each English gloss, does it appear in the verse?
        # Add a column that indicates whether the gloss is found in the verse.
        
        found_col = f"{iso}_in_{bible_version}"
        major_bible[found_col] = major_bible.fillna('').apply(lambda row: row[iso].lower() in row.verse.lower(), axis=1)
        
        # From https://www.statology.org/pandas-groupby-count-with-condition/
        # groupby team and count number of 'pos' equal to 'Gu'
        # df_count = df.groupby('team')['pos'].apply(lambda x: (x=='Gu').sum()).reset_index(name='count')

        bible_wordcount_found = major_bible.groupby(iso)[found_col].apply(lambda x: (x).sum()).reset_index(name='Found')
        bible_wordcount_not_found = major_bible.groupby(iso)[found_col].apply(lambda x: (x == False).sum()).reset_index(name='Not_found')
        bible_wordcount = pd.merge(bible_wordcount_found,bible_wordcount_not_found)
        bible_wordcount['Found_ratio'] = bible_wordcount.apply(lambda x: int(x[1]) / (int(x[1]) + int(x[2])), axis=1)
        bible_wordcount.to_csv(output_tsv, sep = '\t')
    print(f"Saved results to {output_folder}")
        

if __name__ == "__main__":
    parser = ArgumentParser()
    #parser.add_argument('--bible_version', help="Bible version to use", required=True)
    parser.add_argument('--bible_folder', help="Where to find Bible versions", required=True)
    parser.add_argument('--output_folder', type=Path, help="Where to save the output", default="D:/GitHub/davidbaines/trabina/data/matches")
    #parser.add_argument('--repo', help="Bible repo to use", default='ebible')
    parser.add_argument('--ratio_threshold', type=float, help="Threshold for ratio found/total to be significant", default=0.5)
    parser.add_argument('--min_found',       type=int, help="Threshold for minimum found to be considered a match", default=2)
    args = parser.parse_args()
    
    main(args)
