#!/usr/bin/env python3

import shutil
import urllib.request as request
import os
import re
import argparse
from contextlib import closing
from urllib.parse import urlparse

from degenome import gtf_to_gen_pos, dge_to_ideogram

def get_arguments():
    parser = argparse.ArgumentParser(description='Create ideogram jsons from gtf and dge data')
    #parser.add_argument("-l", "--url", action="store_true")
    #parser.add_argument("-f", "--file", action="store_true")
    parser.add_argument("-k", "--keep", action="store_true", help="Determines whether the user wants to keep the intermediate files after the process completes")
    parser.add_argument("-g", "--organism", default="life", help="Determines the name of the gen_post.tsv file. Meaningless when -k is not used")
    parser.add_argument("-o", "--output", default="", help="Output directory of ideogram JSON files")
    parser.add_argument("gtf_path", help="Filepath or url to the gtf info to be processed")
    parser.add_argument("dge_path", help="Filepath or url to the dge matrix info to be processed")

    args = parser.parse_args()
    return args



def check_url(check):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, check) is not None:
        return True
    else:
        return False


def gtf_path(url):
    print("Downloading gtf info from internet")
    parsed_url = urlparse(url)
    gtf_path = os.path.basename(parsed_url.path)
    with closing(request.urlopen(url)) as r:
        with open(gtf_path, 'wb') as f:
            shutil.copyfileobj(r, f)
    return gtf_path

def dge_matrix(url):
    print("Downloading dge info from internet")
    parsed_url = urlparse(url)
    dge_matrix = os.path.basename(parsed_url.path)
    request.urlretrieve(url, dge_matrix)
    return dge_matrix

def ideogram_json(gtf_path, dge_matrix, organism, cleanup=True, output_dir=""):
    print("Converting gtf to gen_post.tsv file")
    print("This may take a while ...")
    gtf_to_gen_pos.etl(gtf_path=gtf_path, organism=organism)
    gen_pos = organism.replace(" ","_")+'.gen_pos.tsv'
    print("Translating dge data to ideogram")
    dge_to_ideogram.etl(gen_pos_path=gen_pos, dge_path=dge_matrix, output_dir=output_dir)

    if cleanup:
        os.remove(gtf_path)
        os.remove(dge_matrix)
        os.remove(gen_pos)
        print("Cleaning Up")

def main():
    args = get_arguments()

    print("Checking gtf to see if URL request is needed")
    if check_url(args.gtf_path):
        gtf = gtf_path(args.gtf_path)
    else:
        gtf = args.gtf_path
    print("Check complete")

    print("Checking dge to see if URL request is needed")
    if check_url(args.dge_path):
        dge = dge_matrix(args.dge_path)
    else:
        dge = args.dge_path
    print("Check complete")

    if args.keep:
        cleanup = False
    else:
        cleanup = True
    ideogram_json(gtf, dge, args.organism, cleanup, args.output)
    print("Finished")
    
if __name__ == "__main__":
    main()
    



#gtf_path = 'ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M23/gencode.vM23.basic.annotation.gtf.gz'
#dge_path = 'https://genelab-data.ndc.nasa.gov/genelab/static/media/dataset/GLDS-4_array_differential_expression.csv?version=1'

#gtf = gtf_path(gtf_path)
#dge = dge_matrix(dge_path)

#ideogram_json(gtf, dge, "momento mori")

