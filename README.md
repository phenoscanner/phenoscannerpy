# phenoscanner.py
phenoscanner.py allows users to query the PhenoScanner database of genotype-phenotype associations from a unix terminal.

# Installation
* Download the phenoscanner.py file.  
* Download the test files.

# Help
python phenoscanner.py --help

# Examples
\# SNP  
python phenoscanner.py --snp=rs10840293  
python phenoscanner.py --snp=True --infile=test_snp  

\# Gene  
python phenoscanner.py --gene=SWAP70  
python phenoscanner.py --gene=True --infile=test_gene  

\#Region  
python phenoscanner.py --location=chr11:9500000-10500000  
python phenoscanner.py --location=True --infile=test_region 
