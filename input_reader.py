
def read_input_file(input_file):
    '''
    Reads the input_file, and returns the content as a string.
    Returns None in case of fail
    '''
    try:
        f = open(input_file, 'r')
        data_string = f.read()
        f.close()
    except:
        data_string = None
    return data_string

def get_nodes_data(data):
    ini_text = "NO" + 9 * " " + "COORD X"
    end_text = "CARACTERISTICAS DAS BARRAS"
    ini_index = data.find(ini_text)
    node_data = data[data.find(ini_text)+len(ini_text):data.find(end_text)]
    ini_text = "==\r\n"
    end_text = 3 * "\r\n" + 5 * " " + "=="
    node_data = node_data[node_data.find(ini_text)+len(ini_text):node_data.find(end_text)]
    lines = node_data.split('\r\n')
    nodes = {}
    for line in lines:
        terms = line.split()
        if len(terms) == 6:
            try:
                index = int(terms[0])
                x = float(terms[1])
                y = float(terms[2])
                nodes[index] = (x, y)
            except:
                print 'error!'
    return nodes

def get_elements_data(data):
    ini_text = "CARACTERISTICAS DAS BARRAS"
    end_text = "PROPRIEDADES DAS BARRAS"
    ini_index = data.find(ini_text)
    node_data = data[data.find(ini_text)+len(ini_text):data.find(end_text)]
    ini_text = "==\r\n"
    end_text = 3 * "\r\n" + 5 * " " + "=="
    node_data = node_data[node_data.find(ini_text)+len(ini_text):node_data.find(end_text)]
    lines = node_data.split('\r\n')
    elements = {}
    for line in lines:
        terms = line.split()
        if len(terms) == 8:
            index = int(terms[0])
            ni = int(terms[1])
            nj = int(terms[3])
            sec_type = int(terms[5])
            cosine = float(terms[7])
            elements[index] = {'nodes':(ni, nj),'section':sec_type, 'cosine':cosine}
    return elements

def get_results_data(data):
    # First : Identify load cases
    #import pdb; pdb.set_trace()
    results = {}
    data_parts = data.split('CARREGAMENTO:')
    if data_parts > 1:
        for part in data_parts[1:]:
            lc = part[:part.find('(GRELHA')].strip()
            results[lc] = {}
            results_ = {}
            # Get data in data part
            
            # Displacements
            start = part.find('NO               DESLOC Z')
            end = part.find('ESFORCOS NAS EXTREMIDADES DAS BARRAS')
            #print "Starts at %d and ends at %d"%(start, end)
            lines = part[start:end].split('\r\n')
            displacements = {}
            for line in lines:
                line_data = line.split()
                if len(line_data) == 4:
                    node = int(line_data[0])
                    vdisp = float(line_data[1])
                    displacements[node] = vdisp
            # Internal forces
            start = part.find('BARRA          NO          CORTANTE')
            end = part.find('RESULTANTES NODAIS')
            lines = part[start:end].split('\r\n')
            lines = part[start:end].split('\r\n')
            iforces = {}
            for i in range(len(lines)):
                line = lines[i]
                line_data = line.split()
                if len(line_data) == 5:
                    next_line_data = lines[i+1].split()
                    elem = int(line_data[0])
                    ni = int(line_data[1])
                    nj = int(next_line_data[0])
                    Vi = float(line_data[2])
                    Vj = float(next_line_data[1])
                    Mi = float(line_data[3])
                    Mj = float(next_line_data[2])
                    Ti = float(line_data[4])
                    Tj = float(next_line_data[3])
                    ifs = {'nodes':(ni,nj),'V':(Vi,Vj),'M':(Mi,Mj),'T':(Ti,Tj)}
                    iforces[elem] = ifs
 

            results[lc]['displacements'] = displacements
            results[lc]['internal_forces'] = iforces

    return results


