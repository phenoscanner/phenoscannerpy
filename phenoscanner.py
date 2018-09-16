import os, re, urllib, json, sys, string
from operator import sub
from optparse import OptionParser

def freader(x):
    ifile=open(x, "r")
    lines=ifile.readlines()
    tab_file=[tuple(line.strip().split("\t")) for line in lines]
    return tab_file

def fwrite(x, filename):
    with open(filename, 'w') as fp:
        fp.writelines('\t'.join(i) + '\n' for i in x)

print("")
print("###############################################################################")
print("## PhenoScanner V2                                                           ##")
print("##                                                                           ##")
print("## Cardiovascular Epidemiology Unit                                          ##")
print("## University of Cambridge                                                   ##")
print("## phenoscanner@gmail.com                                                    ##")
print("##                                                                           ##")
print("## 16/09/18                                                                  ##")
print("###############################################################################")
print("")

parser = OptionParser()
parser.add_option("--snp", default=".", dest="snp", help="query a SNP")
parser.add_option("--gene", default=".", dest="gene", help="query a gene")
parser.add_option("--region", default=".", dest="region", help="query a region")
parser.add_option("--catalogue", default="GWAS", help="catalogue of associations to be queried (options: None, GWAS, eQTL, pQTL, mQTL, methQTL)")
parser.add_option("--pvalue", default=1e-5, help="pvalue threshold")
parser.add_option("--proxies", default="None", help="proxies to be queried (options: None, AFR, AMR, EAS, EUR, SAS)")
parser.add_option("--r2", default=0.8, help="r2 threshold")
parser.add_option("--build", default=37, help="r2 threshold")
parser.add_option("--infile", default=None, dest="infile", help="input file prefix", metavar="FILE")
parser.add_option("--outfile", default=None, dest="outfile", help="output file prefix")
parser.add_option("--wd", default=".", dest="wd", help="working directory")

(options, args) = parser.parse_args()

snp = options.snp
gene = options.gene
region = options.region
catalogue = options.catalogue
pvalue = options.pvalue
proxies = options.proxies
r2 = options.r2
build = options.build
infile = options.infile
outfile = options.outfile
wd = options.wd

os.chdir(wd)

if snp=="True":
    snp=True

if gene=="True":
    gene=True

if region=="True":
    region=True

querysnp = 0
if snp!="." or snp==True:
    querysnp = 1

querygene = 0
if gene!="." or gene==True:
    querygene = 1

queryregion = 0
if region!="." or region==True:
    queryregion = 1

if (querysnp + querygene + queryregion)==0:
    sys.exit('Error: no query has been requested')

if (querysnp + querygene + queryregion)>1:
    sys.exit('Error: cannot have more than two query types')

if (catalogue=="None" or catalogue=="GWAS" or catalogue=="eQTL" or catalogue=="pQTL" or catalogue=="mQTL" or catalogue=="methQTL")==False:
    sys.exit('Error: catalogue has to be one of None, GWAS, eQTL, pQTL, mQTL or methQTL')

if (proxies=="None" or proxies=="AFR" or proxies=="AMR" or proxies=="EAS" or proxies=="EUR" or proxies=="SAS")==False:
    sys.exit('Error: proxies has to one of None, AFR, AMR, EAS, EUR or SAS')

if not(float(pvalue)>0 and float(pvalue)<=1):
    sys.exit('Error: the p-value threshold has to be greater than 0 and less than or equal to 1')

if not(float(r2)>=0.5 and float(r2)<=1):
    sys.exit('Error: the r2 threshold has to be greater than or equal to 0.5 and less than or equal to 1')

if not(int(build)==37 or int(build)==38):
    sys.exit('Error: the genome build has to be either 37 or 38')

if infile==None and (snp==True or gene==True or region==True):
    sys.exit('Error: no input file was specified')

if querysnp==1:
    if snp==True:
        if outfile==None:
            outfile = infile
        qsnps = freader(infile+".txt")
        qsnps = [i[0].strip() for i in qsnps]
        results = None
        snps = None
        if len(qsnps)>100:
            sys.exit('Error: a maximum of 100 SNP queries can be requested at one time')
        else:
            n_queries = len(qsnps) / 10
            if len(qsnps) % 10 > 0:
                n_queries = n_queries + 1
            for i in range(n_queries):
                query = urllib.urlopen("http://www.phenoscanner.medschl.cam.ac.uk/api/?snpquery="+"+".join(qsnps[i*10:(i+1)*10])+"&catalogue="+catalogue+"&p="+str(pvalue)+"&proxies="+proxies+"&r2="+str(r2)+"&build="+str(build))
                out = json.load(query)
                if 'error' in out:
                    print('Error: '+out['error']+" in chunk "+str(i+1))
                else:
                    if results==None:
                        results = out['results']
                    else:
                        results = results + out['results'][1:] 
                    if snps==None:
                        snps = out['snps']
                    else:
                        snps = snps + out['snps'][1:]
                    print(str(i+1)+" -- chunk of 10 SNPs queried")
            if results:
                fwrite(snps, outfile+"_PhenoScanner_SNP_Info.tsv")
                fwrite(results, outfile+"_PhenoScanner_"+catalogue+".tsv")
    else:
        if outfile==None:
            outfile = snp.replace(":", "-")
        query = urllib.urlopen("http://www.phenoscanner.medschl.cam.ac.uk/api/?snpquery="+snp+"&catalogue="+catalogue+"&p="+str(pvalue)+"&proxies="+proxies+"&r2="+str(r2)+"&build="+str(build))
        out = json.load(query)
        if 'error' in out:
            print('Error: '+out['error'])
        else:
            results = out['results']
            snps = out['snps']
            fwrite(snps, outfile+"_PhenoScanner_SNP_Info.tsv")
            fwrite(results, outfile+"_PhenoScanner_"+catalogue+".tsv")
            print(snp+" -- queried")

if querygene==1:
    if gene==True:
        if outfile==None:
            outfile = infile
        qgenes = freader(infile+".txt")
        qgenes = [i[0].strip() for i in qgenes]
        results = None
        genes = None
        if len(qgenes)>10:
            sys.exit('Error: a maximum of 10 gene queries can be requested at one time')
        else:
            n_queries = len(qgenes)
            for i in range(n_queries):
                query = urllib.urlopen("http://www.phenoscanner.medschl.cam.ac.uk/api/?genequery="+qgenes[i]+"&catalogue="+catalogue+"&p="+str(pvalue)+"&proxies=None&r2=1&build="+str(build))
                out = json.load(query)
                if 'error' in out:
                    print('Error: '+out['error']+" for gene: "+qgenes[i])
                else:
                    if results==None:
                        results = out['results']
                    else:
                        results = results + out['results'][1:]
                    if genes==None:
                        genes = out['genes']
                    else:
                        genes = genes + out['genes'][1:]
                    print(qgenes[i]+" -- queried")
            if results:
                fwrite(genes, outfile+"_PhenoScanner_Gene_Info.tsv")
                fwrite(results, outfile+"_PhenoScanner_"+catalogue+".tsv")
    else:
        if outfile==None:
            outfile = gene
        query = urllib.urlopen("http://www.phenoscanner.medschl.cam.ac.uk/api/?genequery="+gene+"&catalogue="+catalogue+"&p="+str(pvalue)+"&proxies=None&r2=1&build="+str(build))
        out = json.load(query)
        if 'error' in out:
            print('Error: '+out['error'])
        else:
            results = out['results']
            genes = out['genes']
            fwrite(genes, outfile+"_PhenoScanner_Gene_Info.tsv")
            fwrite(results, outfile+"_PhenoScanner_"+catalogue+".tsv")
            print(gene+" -- queried")

if queryregion==1:
    if region==True:
        if outfile==None:
            outfile = infile
        qregions = freader(infile+".txt")
        qregions = [i[0].strip() for i in qregions]
        results = None
        regions = None
        if len(qregions)>10:
            sys.exit('Error: a maximum of 10 region queries can be requested at one time')
        else:
            start = [i.split('-',1)[0] for i in qregions]
            start = [re.sub('.*:', "", i) for i in start]
            end = [i.split('-',1)[1] for i in qregions]
            diff = map(sub, map(int,end), map(int,start))
            if any(i > 1000000 for i in diff) or any(i < 0 for i in diff):
                sys.exit('Error: region query can be maximum of 1MB in size')
            else:
                n_queries = len(qregions)
                for i in range(n_queries):
                    query = urllib.urlopen("http://www.phenoscanner.medschl.cam.ac.uk/api/?regionquery="+qregions[i]+"&catalogue="+catalogue+"&p="+str(pvalue)+"&proxies=None&r2=1&build="+str(build))
                    out = json.load(query)
                    if 'error' in out:
                        print('Error: '+out['error']+" for region: "+qregions[i])
                    else:
                        if results==None:
                            results = out['results']
                        else:
                            results = results + out['results'][1:]
                        if regions==None:
                            regions = out['locations']
                        else:
                            regions = regions + out['locations'][1:]
                        print(str(qregions[i])+" -- queried")
                if results:
                    fwrite(regions, outfile+"_PhenoScanner_Location_Info.tsv")
                    fwrite(results, outfile+"_PhenoScanner_"+catalogue+".tsv")
    else:
        if outfile==None:
            outfile = region.replace(":", "-")
        query = urllib.urlopen("http://www.phenoscanner.medschl.cam.ac.uk/api/?regionquery="+region+"&catalogue="+catalogue+"&p="+str(pvalue)+"&proxies=None&r2=1&build="+str(build))
        out = json.load(query)
        if 'error' in out:
            print('Error: '+out['error'])
        else:
            results = out['results']
            regions = out['locations']
            fwrite(regions, outfile+"_PhenoScanner_Location_Info.tsv")
            fwrite(results, outfile+"_PhenoScanner_"+catalogue+".tsv")
            print(region+" -- queried")

print("")
