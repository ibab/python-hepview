
import sys
import os
import re

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.traversal.depth_first_search import dfs_edges

from hepmc import *

def iterate_events(fpath):
    for evt in event_iterator(fpath):
        yield(to_graph(evt))

def event_iterator(fpath):
    reader = IO_GenEvent(fpath, 'r')
    evt = reader.get_next_event()
    while evt:
        yield evt
        evt = reader.get_next_event()

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
        G.add_edge(s, e, barcode=p.barcode(),
                         status=p.status(),
                         pdg=p.pdg_id(),
                         obj=p)
    # color signal particles
    for p1 in G.edges(data=True):
        par = p1[1]
        pid = p1[2]['obj'].pdg_id()
        if pid in {-5, 5}:
            for p2 in dfs_edges(G, par):
                G[p2[0]][p2[1]]['signal'] = True
    return G

if __name__ == '__main__':
    for evt in iterate_events(sys.argv[1]):
        from IPython import embed; embed()
