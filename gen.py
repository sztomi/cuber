from cuber import *

for edges in xrange(0, 14, 2):
    print "Bad edges: {}".format(edges)
    for count in xrange(10):
        print gen_known_scramble(edges)
