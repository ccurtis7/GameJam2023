import sys
import os
import numpy as np
strategyDir = os.path.join(os.getcwd(), 'strategy')
sys.path.insert(0, strategyDir)
from pokerEngine import PokerApp
from pokerBotEngine import PokerAI, PokerAppSelector
import h5py
import hdfdict

def saveMemory(memory, file):
    memoryFile = open(file, 'w')
    for key, entry in memory.items():
        print('{}:{}'.format(key, entry), file=memoryFile)
    memoryFile.close()

def loadMemory(file):
    memoryFile = open(file, 'r')
    memory = {}
    for line in memoryFile.readlines():
        entry = line.replace('\n', '').split(':')
        memory[entry[0]] = eval(entry[1])
    memoryFile.close()
    return memory

def main():
    interface = PokerAppSelector()
    if interface == None:
        return
    elif interface.name == 'bot':
        # load memory
        memoryFile = os.path.join(strategyDir, 'pokerAI3a.txt')
        memory = loadMemory(memoryFile)

        app = PokerAI(interface, memory)
        memory = app.run()
        #print(memory)
        # save memory
        saveMemory(memory, memoryFile)

        #print(memory)
    else:
        app = PokerApp(interface)
        app.run()

if __name__ == '__main__':
    main()
