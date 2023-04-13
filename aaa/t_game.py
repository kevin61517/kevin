from game_test.game_manager import game_service

if __name__ == '__main__':
    service = game_service.get_game('a_game')
    print('service=====>', service)
    print('測試遊戲啟動：', service.launch())
