from pokerEngine import PokerAppSelector, PokerApp

def main():
    interface = PokerAppSelector()
    if interface == None:
        return
    app = PokerApp(interface)
    app.run()

if __name__ == '__main__':
    main()