import sys
import os
import h5py
import hdfdict
import numpy as np

# save memory
memoryFile = 'pokerAI3.h5'
test1 = h5py.File(memoryFile, 'r')
memory = dict(hdfdict.load(memoryFile))
test1.close()

for key, entry in memory.items():
    i = 0
    for sel in entry:
        if (type(sel) == int) | (type(sel) == np.int32) | (type(sel) == np.int64):
            pass
        else:
            memory[key][i] = list(sel)
        i += 1

print(memory)
# load memory
test1 = h5py.File(memoryFile, 'w')
hdfdict.dump(memory, memoryFile)
test1.close()
