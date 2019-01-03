# vgplan_plate_plotter main
from basics import *
from input_reader import *
from compute_and_plot import *

def perform_test():
    ifile_name = "input_files/simple_50.txt"
    text = read_input_file(ifile_name)
    section_data = {1:25,2:50}
    if isinstance(text, str):
        nodes = get_nodes_data(text)
        elements = get_elements_data(text)
        results = get_results_data(text)
        nodal_forces = compute_results(nodes, elements, results, section_data)  
        print nodal_forces

if __name__ == "__main__":
    v, sv, ssv = version()
    print "VGPlan Plate Plotter version %d.%d.%d"%(v,sv,ssv)
    perform_test()    

