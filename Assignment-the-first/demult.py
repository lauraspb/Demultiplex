import argparse

def get_args():
    parser= argparse.ArgumentParser(description="Parses sam file")
    parser.add_argument("-f", help= "filename")
    parser.add_argument("-l", type=int, help="length")
    return parser.parse_args()

args = get_args()

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with "l" values of 0.0.'''
    for i in range(args.l):
        lst.append(value)
    return lst
my_list: list = []
my_list = init_list(my_list)

import Bioinfo
import gzip

def populate_list(file):
    """Takes a fastq file and returns a list of sums of quality scores for each position in the DNA sequence."""
    with gzip.open(file, 'rt') as fh:
        all_qual = init_list([])
        n = 0
        for line in fh:
    #         print(line)
            if n%4==3:
                stripped = line.strip()
    #             print(stripped)
                for i, qual in enumerate(stripped):
                    qscore = Bioinfo.convert_phred(qual)
                    all_qual[i]+=qscore
            n+=1
    return all_qual, n

my_list, num_lines = populate_list(args.f)

print("# Base Pair"+"\t"+"Mean Quality Score")
for i, score in enumerate(my_list):
    my_list[i] = score/(num_lines/4)
    print(str(i)+"\t"+str(my_list[i]))

import matplotlib.pyplot as plt

plt.bar(x=range(args.l), height=my_list)
plt.title('Mean Quality Score of Base Pairs')
plt.ylabel('Mean Quality Score')
plt.xlabel('# Base Pair')
plt.show()
plt.savefig('meanqual_read2.png')