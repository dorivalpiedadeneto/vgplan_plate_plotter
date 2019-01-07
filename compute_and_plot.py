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

def generate_mesh(nodes):
    from  matplotlib.tri.triangulation import Triangulation
    from numpy import array
    x = []; y = []
    for nid in sorted(nodes.keys()):
        x_, y_ = nodes[nid]
        x.append(x_)
        y.append(y_)
    t = Triangulation(x, y)
    return array(x), array(y), t.triangles

def plot_mesh(x, y, mesh):
    import matplotlib.pyplot as plt
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.triplot(x, y, mesh, 'ko-', lw=1.0)
    plt.show()

def plot_mean_value_fields(x, y, mesh, results, nodal_forces, ndiv = 6, orientation='horizontal'):
    from numpy import array,linspace
    import matplotlib.pyplot as plt

    # Drawing limits
    xmax = max(x); xmin = min(x)
    ymax= max(y); ymin = min(y)
    dx = xmax - xmin
    dy = ymax - ymin
    xmax += 0.1 * dx; xmin -= 0.1 * dx
    ymax += 0.1 * dy; ymin -= 0.1 * dy


    #print results['P']['displacements'].keys()
    #print nodal_forces['P']['mean'].keys()
    fig_num = 1

    for load_case in results.keys():
        # Plotting displacement
        disp = results[load_case]['displacements']
        disp_val = []
        for node, disp in disp.items():
            #print " - Node # %d: %f"%(node, disp)
            disp_val.append(disp)
        min_val = min(disp_val)
        max_val = max(disp_val)
        if abs(max_val-min_val) < 1.0e-6:
            lvs = [min_val - 0.1, max_val + 0.1]
        else:
            lvs = linspace(min_val, max_val, ndiv).tolist()
        disp_val = array(disp_val)
        # Creating figure
        fig = plt.figure(fig_num)
        ax = fig.add_subplot(111)
        ctr = ax.tricontourf(x,y, mesh, disp_val, cmap = plt.cm.spectral)#, levels = lvs) 
        ax.set_title('Displacement - %s'%load_case)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        fig.colorbar(ctr, orientation=orientation)
        fig_num += 1

    for load_case in nodal_forces.keys():
        # Plotting internal forces
        iforces = nodal_forces[load_case]['mean']
        v_val = []; my_val = []; mx_val = []; mxy_val = []
        for node, iforce in iforces.items():
            v_val.append(iforce['v'])
            mx_val.append(iforce['mx'])
            my_val.append(iforce['my'])
            mxy_val.append(iforce['mxy'])
        v_val = array(v_val)
        mx_val = array(mx_val)
        my_val = array(my_val)
        mxy_val = array(mxy_val)
        # Creating mx figure
        fig = plt.figure(fig_num)
        ax = fig.add_subplot(111)
        ctr = ax.tricontourf(x,y, mesh, mx_val, cmap = plt.cm.spectral)
        ax.set_title('mx - %s'%load_case)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        fig.colorbar(ctr, orientation=orientation)
        fig_num += 1
        # Creating my figure
        fig = plt.figure(fig_num)
        ax = fig.add_subplot(111)
        ctr = ax.tricontourf(x,y, mesh, my_val, cmap = plt.cm.spectral)
        ax.set_title('my - %s'%load_case)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        fig.colorbar(ctr, orientation=orientation)
        fig_num += 1
        # Creating mxy figure
        fig = plt.figure(fig_num)
        ax = fig.add_subplot(111)
        ctr = ax.tricontourf(x,y, mesh, mxy_val, cmap = plt.cm.spectral)
        ax.set_title('mxy - %s'%load_case)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        fig.colorbar(ctr, orientation=orientation)
        fig_num += 1
        # Creating v figure
        fig = plt.figure(fig_num)
        ax = fig.add_subplot(111)
        ctr = ax.tricontourf(x,y, mesh, v_val, cmap = plt.cm.spectral)
        ax.set_title('v - %s'%load_case)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        fig.colorbar(ctr, orientation=orientation)
        fig_num += 1




       


    plt.show()

