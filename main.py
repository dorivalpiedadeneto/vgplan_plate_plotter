# vgplan_plate_plotter main
from basics import *
from input_reader import *

if __name__ == "__main__":
    v, sv, ssv = version()
    print "VGPlan Plate Plotter version %d.%d.%d"%(v,sv,ssv)
    perform()

