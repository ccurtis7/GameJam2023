import sys
import os
import numpy as np
strategyDir = os.path.join(os.getcwd(), 'strategy')
sys.path.insert(0, strategyDir)
from pokerEngine import PokerApp
from pokerBotEngine import PokerAI, PokerAppSelector
import h5py
import hdfdict


def main():
    interface = PokerAppSelector()
    if interface == None:
        return
    elif interface.name == 'bot':
        # load memory
        memoryFile = os.path.join(strategyDir, 'pokerAI3.h5')
        test1 = h5py.File(memoryFile, 'r')
        memory = dict(hdfdict.load(memoryFile))
        test1.close()
        # Doing a memory cleaning
        #memory = {}

        app = PokerAI(interface, memory)
        memory = app.run()
        #print(memory)
        # save memory
        try:
            test1 = h5py.File(memoryFile, 'w')
            hdfdict.dump(memory, memoryFile)
            test1.close()
        except:
            for key, entry in memory.items():
                i = 0
                for sel in entry:
                    if (type(sel) == int) | (type(sel) == np.int32) | (type(sel) == np.int64):
                        pass
                    elif type(sel) == np.ndarray:
                        memory[key][i] = list(sel)
                    else:
                        _ = memory[key].pop(i)
                    i += 1
            try:
                test1.close()
            except:
                pass
            test1 = h5py.File(memoryFile, 'w')
            hdfdict.dump(memory, memoryFile)
            test1.close()

        #print(memory)
    else:
        app = PokerApp(interface)
        app.run()

if __name__ == '__main__':
    main()
