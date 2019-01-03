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
        internal_forces = results[load_case]['internal_forces']
        for element, result in internal_forces.iteritems():
            element_data = elements[element]
            ni, nj = element_data['nodes']
            sec_num = element_data['section']
            cosine = element_data['cosine']
            sine = sqrt(1.0 - cosine ** 2)
            width = section_data[sec_num]
            Mi, Mj = result['M']
            Ti, Tj = result['T']
            Vi, Vj = result['V']
            # Node i
            mxi = - sine * Mi / width 
            myi = cosine * Mi / width
            mxyi = (sine + cosine) * Ti / width
            vi = Vi / width 

            # Node j
            mxj = - sine * Mj / width 
            myj = cosine * Mj / width
            mxyj = (sine + cosine) * Tj / width
            vj = Vj / width 
            
            # 1st node
            if nf.has_key(ni):
                nf_ = nf[ni]
                nf_['mx'].append(mxi)
                nf_['my'].append(myi)
                nf_['mxy'].append(mxyi)
                nf_['v'].append(vi)
            else:
                nf_ = {}
                nf_['mx'] = [mxi]
                nf_['my'] = [myi]
                nf_['mxy'] = [mxyi]
                nf_['v'] = [vi]
                nf[ni] = nf_

            # 2nd node
            if nf.has_key(nj):
                nf_ = nf[nj]
                nf_['mx'].append(mxj)
                nf_['my'].append(myj)
                nf_['mxy'].append(mxyj)
                nf_['v'].append(vj)
            else:
                nf_ = {}
                nf_['mx'] = [mxj]
                nf_['my'] = [myj]
                nf_['mxy'] = [mxyj]
                nf_['v'] = [vj]
                nf[nj] = nf_

        # Computing mean values
        tol = 1.0e-6
        nfm = {} # Nodal force mean value
        for k,nf_ in nf.items():
            print '-> Node #%d'%k
            nfm_ = {}
            for iftype in ('mx','my','mxy','v'):
                print '  - %s: %s'%(iftype,str(nf_[iftype]))
                count = 0
                val = 0.0
                for v in nf_[iftype]:
                    if abs(v) > tol:
                        count += 1
                        val += v
                if count > 0:
                    nfm_[iftype] = val / float(count)
                else:
                    nfm_[iftype] = 0.0
                print '   -> Mean value: %f'%nfm_[iftype]
            nfm[k] = nfm_
        nodal_forces[load_case] = {"all":nf,"mean":nfm}

    return nodal_forces



