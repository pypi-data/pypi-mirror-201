import numpy as np
import ctypes
import os

absolute_path = os.path.dirname(__file__)
absolute_path += "lib/library.so"

# # Load the shared library
lib = ctypes.CDLL(absolute_path)

def get_community(nodes, edges):
    # Create a 2D NumPy array
    a = np.array(edges, dtype=np.int32)
    nodeCount = len(nodes)

    # Get the dimensions of the array
    nrows, ncols = a.shape

    # Create a 1D NumPy array to hold the output
    b = np.zeros(nodeCount, dtype=np.int32)

    # Pass the arrays to the C function
    lib.get_community(
        a.ctypes.data_as(ctypes.POINTER(ctypes.c_int)), # edge
        ctypes.c_int(nrows), #edge_count
        ctypes.c_int(nodeCount), #node_count
        b.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    )
    b = [p for p in b]
    return b





