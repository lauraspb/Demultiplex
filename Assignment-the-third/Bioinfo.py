#!/usr/bin/env python

def validate_base_seq(seq,RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    DNAbases = set('ATGCatcg')
    RNAbases = set('AUGCaucg')
    return set(seq)<=(RNAbases if RNAflag else DNAbases)
# print(validate_base_seq('ACTGTG'))

def convert_phred(letter):
    """Converts a single character into a phred score"""
    return ord(letter) - 33

def qual_score(phred_score):
    phred_scores = []
    for letter in phred_score:
        phred_scores.append(convert_phred(letter))
    return sum(phred_scores)/len(phred_score)

DNA = set('ACTGactg')

if __name__ == "__main__":
    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    assert validate_base_seq("Hi there!") == False, "Validate base seq fails to recognize nonDNA"
    assert validate_base_seq("Hi there!", True) == False, "Validate base seq fails to recognize nonDNA"
    print("Passed DNA and RNA tests")