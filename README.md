# Ideogram Jsonifyer

Creates an ideogram compatible JSON file using GTF and DGE data.

Prerequisites
-python version 3.6 or higher
-pip *or* 
-degenome version 0.1.0 or higher
(the install program does pip3 install degenome)

Use command ```./ideogram_jsonify.py --help``` for full documentation.

Typical use
```./ideogram_jsonify.py gtf_path dge_path```
```python3 ideogram_jsonify.py gtf_path dge_path``` also works if for some reason you don't get the program to work as an executable

Example use:
```./ideogram_jsonify.py ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M23/gencode.vM23.basic.annotation.gtf.gz https://genelab-data.ndc.nasa.gov/genelab/static/media/dataset/GLDS-4_array_differential_expression.csv?version=1```

This will create the necessary json files to do a differential gene analysis of the two datasets. The program automatically determines whether the inputs are urls that need to be downloaded from the internet or local files.

*Note* The program will By default the program will delete the gtf and dge files that are used to try to reduce clutter. Use the flag -k to prevent this from happening.
