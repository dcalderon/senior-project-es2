"""
This program will serve as our control. It'll demarcate the ecotypes randomly to show how
bad of a VI score it'll get.

We take in the id we are using and output a file with random (should check this) demarcations.
"""

from random import *

def runrandom2(id):
    """
    Second random demarcation implementation. Ecotypes broken up according to
    the broken-stick distribution.
    """
    
    sequence_file = open('./sequences/amlfredfasta.fas', 'r')
    out_file = open('./output/Random2_'+id+'.csv','w')
    sequences = []
    
    #Get the outgroup
    outgroup = sequence_file.readline()[1:].strip()
    # First let's read in the sequences into a list. I.e., parse out relevant info
    for line in sequence_file:
        if line[0] == '>':
            sequences += [line[1:].strip()]
    sequence_file.close()
    
    #Decide on npop
    #rand_npop = find_npop(sequences, id)
    rand_npop = answer_npop(id)
    print 'rand_npop: ', rand_npop 
    
    #First create ecotype distribution
    ecotype_distribution = [len(sequences)]
    while len(ecotype_distribution) != rand_npop:
        e_to_split = randint(0, len(ecotype_distribution) - 1)
        num_of_e = ecotype_distribution[e_to_split]
        if num_of_e != 1:
            #print 'num_of_e: ', num_of_e
            del ecotype_distribution[e_to_split]
            #I think should be -1 since we don't want ecotypes of 0
            new_e = randint(1, (num_of_e - 1))
            ecotype_distribution.append(new_e)
            ecotype_distribution.append(num_of_e - new_e)
            #print 'ecotype distribution: ',ecotype_distribution
    
    #find largest ecotype
    largest_ecotype = 1
    for i in ecotype_distribution:
        if i > largest_ecotype:
            largest_ecotype = i
    
    #Then distribute shuffled sequences according to distribution
    shuffle(sequences)
    ecotypes = []
    for i in ecotype_distribution:
        ecotypes.append(sequences[:i])
        sequences = sequences[i:]
    
    #Print out file
    # Start making outputfile
    first_line = 'Ecotype Number'
    for i in range(1, largest_ecotype + 1):
        first_line += ',Sequence '+str(i)
    out_file.write(first_line+"\n")
    
    # Print ecotypes
    line_number = 1
    for eco in ecotypes:
        line = str(line_number)
        for e in eco:
            line += ','+e
        out_file.write(line+"\n")
        line_number+=1
        
    # Final line
    out_file.write('Outgroup'+outgroup)
    out_file.close()
    
def find_npop(sequences, id):
    """
    Function to return chosen npop, so I can change this and change 
    how all the random demarcators find npop.
    """
    return randint(1, len(sequences) + 1)
    
def answer_npop(id):
    """
    Given the id with the solution npop number returns correct npop.
    """
    # final200_50npop_1.9omega_11sigma_0gamma_4 example id
    # we split among underscore then take npop portion and chop npop
    # off then cast to int
    
    #NEED TO ADJUST FOR id that is sent to this! I think it's right
    return int(id.split('_')[1][:-4])

def runrandom(id):
    """
    First random demarcation implementation.
    """
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
    rand_npop = find_npop(sequences, id)
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