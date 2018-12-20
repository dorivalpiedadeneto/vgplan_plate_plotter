
def compute_results(nodes, elements, results, section_data):
    for node, coords in nodes.iteritems():
        print "Node # %d, %s"%(node, str(coords))
    for element, data in elements.iteritems():
        print "Element # %d, %s"%(element, str(data))
    for load_case in results.keys():
        print "\n- Load case: %s\n\n"%load_case
        displacements = results[load_case]['displacements']
        internal_forces = results[load_case]['internal_forces']
        print "\n - Displacements\n\n"
        for node, result in displacements.iteritems():
            print "Node # %d: %s"%(node,str(result))
        print "\n - Internal forces\n\n"
        for element, result in internal_forces.iteritems():
            print "Element # %d: %s"%(element,str(result))
         

