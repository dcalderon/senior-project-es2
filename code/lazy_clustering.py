"""
This will be a mini package that will do complete-linkage heiarchical clustering without
a divergence matrix. Instead we will give it a distance function that will calculate distances
lazily, thus run on approximately linear space...

WOOH GOT IT WORKING! QUITE SLOW though... Compressions set up as well.
Now I would like to implement this in FORTRAN...
"""
import sys

def seq_distance(s1, s2, seq_size):
    """
    This is the distance function used, somewhat similar to manhatten distance.
    """
    diff = 0.0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            diff+=1.0
    # Might not have this (1 - dist) bit but I think necessary for now.
    return 1.0 - (diff / seq_size)

def clust_distance(c1, c2, seqs, seq_size):
    """
    Given two clusters calculates the distance between the two. TEST!
    """
    max_distance = 1.0
    for i in range(len(c1)):
        for j in range(len(c2)):
            d = seq_distance(seqs[c1[i]], seqs[c2[j]], seq_size)
            if d < max_distance:
                max_distance = d
    return max_distance

def grab_input(fasta):
    """
    This function will grab the input FASTA file and put it into a maneagable data structrue.
    Eventually we'd like to also compress input DNA.
    
    For now returns two corresponding lists of labels and sequences.
    """
    labels = []
    seqs = []
    input = open(fasta, 'r')
    for line in input:
        if line[0] == '>':
            labels.append(line.strip())
        else:
            seqs.append(line.strip())
    
    seq_size = len(seqs[0])
    #Compression
    compressed_seqs = compress_seqs(seqs)
    return labels, compressed_seqs, seq_size
    
    # Before compression
    #return labels, seqs, seq_size

def compress_seqs(seqs):
    """
    Takes in a list of sequences and returns a list of compressed sequences
    """
    #Some initialization
    first_round = True
    pos = []
    compressed_seqs = []
        
    #These loops find all mutation sites
    for column in range(len(seqs[0])):
        pos.append(set())
        for row in range(len(seqs)):
            if first_round:
                compressed_seqs.append('')
            pos[column].add(seqs[row][column])
        first_round = False
    
    #These loops create the compressed sequences 
    for i in range(len(pos)):
        if len(pos[i]) > 1:
            # mutation_site.append(i)
            for j in range(len(compressed_seqs)):
                compressed_seqs[j]+=seqs[j][i]
                
    return compressed_seqs

def get_bins():
    """
    This function will serve to find bin levels wherever they may be...
    For now I'll just give them but may need to look in files later on.
    """
    
    return [0.8, 0.85, 0.9, 0.95, 0.96, 0.97, 0.98, 0.99, 0.995, 1.0]
    #return [.97,]

def matrix(fasta):
    labels, seqs = grab_input(fasta)
    out = open('divmatrix.csv','w')
    for i in range(len(seqs)):
        line = ''
        for j in range(len(seqs)):
            line+=str(seq_distance(seqs[i], seqs[j]))+','
        out.write(line+"\n")
    out.close()

def cluster(fasta):
    """
    Naive complete linkage clustering will occur here. Using distance functions to look
    up distances as we go...
    """
    # Initializing stuff!
    # get's the compressed sequences and the original sequence size
    labels, seqs, seq_size = grab_input(fasta)
    bins = get_bins()
    #return
    #Clusters in here will be ints referring to their seqs list
    output = []
    n_clusters = len(seqs)
    
    #Loop for each identity level find number of bins
    for l in range(len(bins)):
        n_clusters = len(seqs)
        cluster = []
        for i in range(len(seqs)):
            cluster.append([i])
        identity_level = bins[l]
        print identity_level
        # Loop find closest pair of clusters combine, recompute distances
        while True:
            x = -1.0
            xi = 0
            xj = 1
            for i in range(len(cluster)):
                for j in range(i+1, len(cluster)):
                    t = clust_distance(cluster[i], cluster[j], seqs, seq_size)
                    if (t > x):
                        x = t
                        xi = i
                        xj = j
                        
            # If closest pair further apart than identity_level then done
            if (x < identity_level): break
            n_clusters = n_clusters - 1
            # Otherwise, combine the closest pair into xi and eliminate xj
            cluster[xi]+=cluster[xj]
            del cluster[xj]
            
            # TESTING OUTPUT
            # print cluster
            # print "distance of cluster just combined: ", t
            # print "first cluster combined: ", xi
            # print "second cluster combined: ", xj
            # print "number of clusters : ", n_clusters
                                    
        #Output stuff
        output.append((identity_level, n_clusters))
    return output

if __name__ == "__main__":
    print cluster(sys.argv[1])