
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
            try:
                index = int(terms[0])
                ni = int(terms[1])
                nj = int(terms[3])
                elements[index] = (ni, nj)
            except:
                print 'error!'
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
            # Get data in data part 
    return results

        


def perform():
    ifile_name = "input_files/simple_50.txt"
    text = read_input_file(ifile_name)
    if isinstance(text, str):
        print get_nodes_data(text)
        print get_elements_data(text)
        print get_results_data(text)
