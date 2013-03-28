def clust_distance(c1, c2, seqs):
    max_distance = 1.0
    for i in range(len(c1)):
        for j in range(len(c2)):
            d = seq_distance(seqs[c1[i]], seqs[c2[j]])
            if d < max_distance:
                max_distance = d
    return max_distance

