f = open('amlRFWsequences-without-DNA.fas','r')
f2 = open('RFW-without-DNA.fas','r')
#out = open('switch.fas','w')

replace = {}

for line in f:
    l = f2.readline()[1:].strip()
    replace[line[1:].strip()] = l
    print line[1:].strip(),' : ',l 
    
print replace
    
f.close()
f2.close()
#out.close()