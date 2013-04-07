"""
This program will serve as our control. It'll demarcate the ecotypes randomly to show how
bad of a VI score it'll get.

We take in the id we are using and output a file with random (should check this) demarcations.
"""

from random import *

def runrandom(id):
    sequence_file = open('./sequences/amlfredfasta.fas', 'r')
    out_file = open('./output/Random_'+id+'.csv','w')
    sequences = []
    
    #Get the outgroup
    outgroup = sequence_file.readline()[1:].strip()
    # First let's read in the sequences into a list. I.e., parse out relevant info
    for line in sequence_file:
        if line[0] == '>':
            sequences += [line[1:].strip()]
    sequence_file.close()
    
    # Randomly pick the number of ecotypes.
    rand_npop = randint(1, len(sequences) + 1)
    npop_list = range(1, rand_npop+1)
    
    # Initializes ecotype group dictionary
    ecotypes = {}
    for i in npop_list:
        ecotypes[i] = []
        
    # Shuffles everything in randomly
    shuffle(npop_list)
    shuffle(sequences)
    for i in npop_list:
        if len(sequences) != 0:
            for j in range(1, randint(1, len(sequences))):
                ecotypes[i] += [sequences.pop()]
                
    # Create a list of lists where the index represents the ecotype number
    # also a way to delete empty keys.
    result_ecotypes = []
    largest_ecotype = 0
    for i in npop_list:
        t = ecotypes[i]
        if len(t) != 0:
            result_ecotypes += [t]
            if len(t) > largest_ecotype:
                largest_ecotype = len(t)
    
    # Start making outputfile
    first_line = 'Ecotype Number'
    for i in range(1, largest_ecotype + 1):
        first_line += ',Sequence '+str(i)
    out_file.write(first_line+"\n")
    
    # Print ecotypes
    line_number = 1
    for eco in result_ecotypes:
        line = str(line_number)
        for e in eco:
            line += ','+e
        out_file.write(line+"\n")
        line_number+=1
        
    # Final line
    out_file.write('Outgroup'+outgroup)
    out_file.close()
    
if __name__ == "__main__":
    import sys
    runrandom(sys.argv[1])