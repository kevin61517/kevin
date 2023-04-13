from interface_test import team_manager

if __name__ == '__main__':
    teammate = team_manager
    kevin = team_manager.get_teammate('kevin')
    leia = team_manager.get_teammate('leia')
    print(kevin.name)
    kevin.exec()
    kevin.slots()
    leia.exec()
