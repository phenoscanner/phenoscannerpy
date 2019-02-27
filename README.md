# phenoscanner.py
phenoscanner.py allows users to query the PhenoScanner database of genotype-phenotype associations from a unix terminal.

## Installation
* Download the [phenoscanner.py](https://raw.githubusercontent.com/phenoscanner/phenoscannerpy/master/phenoscanner.py) file.  
* Download the test files.

## Usage
\# Single query  
A single SNP, gene or region can be queried on the command line using the snp, gene or region flag respectively (see examples below).

\# Multiple queries  
Multiple queries can be performed by using inputting a file containing the SNPs/genes/regions to be queried. Input files have to be tab-delimited text files (without a header) with one SNP, gene or genomic region per line (max 100 SNPs, 10 genes or 10 regions) depending on the query. These files are loaded into the program using the infile option (file prefix only, i.e. no .txt) and by setting the relevant query type to True (see examples below). 

## Examples
\# Help  
python phenoscanner.py --help  

\# SNP  
python phenoscanner.py --snp=rs10840293  
python phenoscanner.py --snp=True --infile=test_snp  

\# Gene  
python phenoscanner.py --gene=SWAP70  
python phenoscanner.py --gene=True --infile=test_gene  

\#Region  
python phenoscanner.py --region=chr11:9500000-10500000  
python phenoscanner.py --region=True --infile=test_region 

## Citation
Staley JR et al. PhenoScanner: a database of human genotype-phenotype associations. Bioinformatics 2016;32(20):3207-3209.
