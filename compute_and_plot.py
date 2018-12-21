from math import sqrt

def compute_results(nodes, elements, results, section_data):
#   for node, coords in nodes.iteritems():
#       print "Node # %d, %s"%(node, str(coords))
#   for element, data in elements.iteritems():
#       print "Element # %d, %s"%(element, str(data))
#   for load_case in results.keys():
#       print "\n- Load case: %s\n\n"%load_case
#       displacements = results[load_case]['displacements']
#       internal_forces = results[load_case]['internal_forces']
#       print "\n - Displacements\n\n"
#       for node, result in displacements.iteritems():
#           print "Node # %d: %s"%(node,str(result))
#       print "\n - Internal forces\n\n"
#       for element, result in internal_forces.iteritems():
#           print "Element # %d: %s"%(element,str(result))
#        
    # The displacements are already computed for each node
    # 1st step - compute internal forces in nodes
    nodal_forces = {}
    for load_case in results.keys():
        nf = {}
        for element, result in internal_forces.iteritems():
            element_data = elements[element]
            ni, nj = element_data['nodes']
            sec_num = element_data['section']
            cosine = element_data['cosine']
            sine = sqrt(1.0 - cossine ** 2)
            width = section_data[sec_num]
            Mi, Mj = result['M']
            Ti, Tj = result['T']
            Vi, Vj = result['V']
            # Node i
            mxi = - sine * M / width 
            myi = cosine * M / width
            Mxyi = (sine + cosine) * T / width
            vi = Vi / width 

            # Node j
            mxi = - sine * M / width 
            myi = cosine * M / width
            Mxyi = (sine + cosine) * T / width
            vi = Vi / width 


