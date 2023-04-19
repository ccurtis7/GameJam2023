from pokerEngine import PokerAppSelector, PokerApp
import numpy as np

def main():
    interface = PokerAppSelector()
    if interface == None:
        return
    if interface.name != 'AI':
        app = PokerApp(interface)
        app.run()
    else:
        winnings = []
        for i in range(2000):
            app = PokerApp(interface)
            app.run()
            winnings.append(app.money)
        print('Average winnings for {} hands: {}'.format(app.interface.maxhands, np.average(winnings) - 100))

if __name__ == '__main__':
    main()
