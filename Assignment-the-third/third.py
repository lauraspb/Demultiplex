#!usr/bin/env python

import argparse
import Bioinfo 
import gzip
parser = argparse.ArgumentParser()

#taking arguments for reads, indexes, barcode file, quality score cutoff
parser.add_argument("-r1", help="Read 1 file name")
parser.add_argument("-r2", help="Read 2 file name")
parser.add_argument("-i1", help="Index 1 file name")
parser.add_argument("-i2", help="Index 2 file name, reverse complemented input")
parser.add_argument("-b", help="barcodes file with expected indices")
parser.add_argument("-q", type=int, help="quality score cutoff for indices.")
args = parser.parse_args()

#opening files saving to variables
r1 = gzip.open(args.r1, 'rt')
r2 = gzip.open(args.r2, 'rt')
i1 = gzip.open(args.i1, 'rt')
i2 = gzip.open(args.i2, 'rt')
iL = open(args.b, 'r')

#Opening the barcodes file and getting the index and index sequences in a list
#also opening up all of the output files for writing
known = {}
filenames1 = {}
filenames2 = {}
for line in iL:
    line = line.strip()
    index = line.split("\t")[3]
    sequence = line.split("\t")[4]

    #ignoring the first line of index file because it is not a sequence
    if Bioinfo.validate_base_seq(sequence):
        known[sequence] = [index]

        #using the index name of the line to name my output files and save them 
        #as variables in a dict
        out_r1 = open(f'out_R1_{index}.fastq', 'w')
        out_r2 = open(f'out_R2_{index}.fastq', 'w')
        filenames1[sequence] = (out_r1, f'out_R1_{index}.fastq')
        filenames2[sequence] = (out_r2, f'out_R2_{index}.fastq')

#opening the rest of the files for writing
sw1 = open('swap_R1.fastq', 'w')
sw2 = open('swap_R2.fastq', 'w')
b1 = open('bad_R1.fastq', 'w')
b2 = open('bad_R2.fastq', 'w')

#High level functions
def addheader(header,i1, i2):
    '''This function takes the header, and two indexes, and returns a new header
    with the appended indexes at the end of it'''
    new = header+'-'+i1+'-'+revcomp(i2)
    return new

def revcomp(index):
    '''This function takes an index from index2 file and returns the reverse 
    complement string'''
    comp = ''
    for nt in index:
        if nt == 'A':
            comp = comp + 'T'
        elif nt == 'T':
            comp = comp + 'A'
        elif nt == 'C':
            comp = comp + 'G'
        elif nt == 'G':
            comp = comp + 'C'
    comp = comp[::-1]
    return comp
    
def qualcheck(qline):
    '''Checks that the average of the qscores in a quality score line (qline) are
    above the cutoff, returns a boolean'''
    tot = 0
    for q in qline:
        tot += Bioinfo.convert_phred(q)
    qscore = tot/len(qline)
    if qscore < args.q:
        return False
    else:
        return True

    
#initializing empty lists that will hold records for each file
r1list, r2list, i1list, i2list = [], [], [], []
di = {}
bco = 0
sco = 0
mco = 0
total = 0
for a, b, c, d in zip(r1, r2, i1, i2):
    a = a.strip()
    b = b.strip()
    c = c.strip()
    d = d.strip()
    #Appending lines of files while the lists are less than 4 elements long, once they
    #are, I am continuing with logic statements.
    if len(r1list) < 4:
        r1list.append(a)
        r2list.append(b)
        i1list.append(c)
        i2list.append(d)
        if len(r1list) == 4:
            i2list[1] = revcomp(i2list[1])

            #bad file writing if found Ns or not in known dictionary of indexes, or if quality score is too low. 
            if 'N' in i1list[1] or 'N' in i2list[1] or i1list[1] not in known or i2list[1] not in known or qualcheck(i1list[3]) == False or qualcheck(i2list[3]) == False:
                r1list[0] = addheader(r1list[0], i1list[1], i2list[1])
                r2list[0] = addheader(r2list[0], i1list[1], i2list[1])
                b1.writelines("%s\n" % l for l in r1list)
                bco+=1
                total+=1
                b2.writelines("%s\n" % l for l in r2list)
    
            #if indexes are the same I will change the header and write that to the appropriate file
            elif i1list[1] == i2list[1]:
                r1list[0] = addheader(r1list[0], i1list[1], i2list[1])
                r2list[0] = addheader(r2list[0], i1list[1], i2list[1])
                for file in filenames1:
                    if i1list[1] in file:
                        filenames1[file][0].writelines("%s\n" % l for l in r1list)
                        if i1list[1] not in di:
                            di[i1list[1]] = 1
                        else:
                            di[i1list[1]] +=1
                for file in filenames2:
                    if i2list[1] in file:
                        filenames2[file][0].writelines("%s\n" % l for l in r2list)
                        mco+=1
                        total+=1
                        
            #if indexes are not the same, header gets changed and lists written to swap files
            elif i1list[1] != i2list[1]:
                r1list[0] = addheader(r1list[0], i1list[1], i2list[1])
                r2list[0] = addheader(r2list[0], i1list[1], i2list[1])
                sw1.writelines("%s\n" % l for l in r1list)
                sw2.writelines("%s\n" % l for l in r2list)  
                sco +=1 
                total +=1             
            r1list, r2list, i1list, i2list = [], [], [], []


tot = bco+sco+mco
with open('report', 'w') as r:
    for k in di:
        r.write(f"{(di[k]/mco)*100} percent reads of {k} index\n")
    r.write(f"{bco} read-pairs found in bad category\n")
    r.write(f"{sco} read-pairs found in swap category\n")
    r.write(f"{mco} read-pairs found in match category\n")






