def runrandom():
    #OPEN FASTA FILE AND OUTPUT FILE
    outgroup = sequence_file.readline()[1:].strip()
    for line in sequence_file:
        if line[0] == '>':
            sequences += [line[1:].strip()]
    sequence_file.close()
    rand_npop = randint(1, len(sequences) + 1)
    npop_list = range(1, rand_npop+1)
    ecotypes = {}
    for i in npop_list:
        ecotypes[i] = []
    shuffle(npop_list)
    shuffle(sequences)
    for i in npop_list:
        if len(sequences) != 0:
            for j in range(1, randint(1, len(sequences))):
                ecotypes[i] += [sequences.pop()]
    result_ecotypes = []
    largest_ecotype = 0
    for i in npop_list:
        t = ecotypes[i]
        if len(t) != 0:
            result_ecotypes += [t]
            if len(t) > largest_ecotype:
                largest_ecotype = len(t)
    #OUTPUT RESULTS