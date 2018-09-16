# phenoscanner.py
phenoscanner.py allows users to query the PhenoScanner database of genotype-phenotype associations from a unix terminal.

# Installation
* Download the phenoscanner.py file.  
* Download the test files.

# Help
python phenoscanner.py --help

# Command line query
A single SNP, gene or region can be queried 

# Input files
Input files have to be tab-delimited text files (without a header) with one SNP, gene or genomic region per line (max 100 SNPs, 10 genes or 10 regions) depending on the query. These files are loaded into the program using the infile option (file prefix only, i.e. no .txt) and by setting the relevant query type to True (see examples below). 

# Examples
\# SNP  
python phenoscanner.py --snp=rs10840293  
python phenoscanner.py --snp=True --infile=test_snp  

\# Gene  
python phenoscanner.py --gene=SWAP70  
python phenoscanner.py --gene=True --infile=test_gene  

\#Region  
python phenoscanner.py --region=chr11:9500000-10500000  
python phenoscanner.py --region=True --infile=test_region 
