
from hepmc import *
import pydot
import os
import re
from sys import argv

import networkx as nx
import matplotlib.pyplot as plt

def to_graph(evt):
    G = nx.DiGraph()
    in_counter = 0
    out_counter = 0
    for v in evt.vertices():
        G.add_node(v.barcode())
    for p in evt.particles():
        start = p.production_vertex()
        end = p.end_vertex()
        if not start:
            s = 'In: %d' % in_counter
            e = end.barcode()
            in_counter += 1
        elif not end:
            s = start.barcode()
            e = 'Out: %d' % out_counter
            out_counter += 1
        else:
            s = start.barcode()
            e = end.barcode()
        G.add_edge(s, e, barcode=p.barcode(), status=p.status(), pdg=p.pdg_id(), object=p)
    return G

if __name__ == '__main__':
    reader = IO_GenEvent(argv[1], 'r')
    evt = reader.get_next_event()
    G = to_graph(evt)
    from IPython import embed; embed()
