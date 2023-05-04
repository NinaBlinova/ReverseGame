# реверси
import random
import sys

# для получения функции exit(), которая возвращает целое число, указывающее статус выхода.

width = 8
height = 8

def drawBoard(board):
    # вывести игровое поле, ничего не возвращать
    print('   1 2 3 4 5 6 7 8')
    print('  ┎─┰─┰─┰─┰─┰─┰─┰─┒')
    for y in range(height):
        print(f' {(y + 1)}┃', end='')  # выводит метку для оси у левой части поля и содержит аргумент - ключевое слово
        # end='', чтобы вместо новой строки не ыводить ничего
        # (по умолчанию идет перевод на новую строку, а тут это не нужно)
        for x in range(width):
            if x > 0:
                print('\'', end='')
            print(board[x][y], end='')
        print(f'┃{(y + 1)}')
    print('  ┖─┸─┸─┸─┸─┸─┸─┸─┚')
    print('   1 2 3 4 5 6 7 8')





# начальный вид поля игры reverse
def createBoard():
    # создать структуру данных нового чистого игрового поля
    board = []
    for i in range(width):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board



def askEnemy():
    enemy = ''
    while not (enemy == '1' or enemy == '2'):
        print('Вы играете против компьютера(1) или человека(2)? ')
        enemy = input().lower()
    return enemy


def getFirstMove(enemy):
    # случайно выбрать, кто ходил первым
    if enemy == '1':
        if random.randint(0, 1) == 0:
            return 'Компьютер'
        return 'Человек'
    if enemy == '2':
        if random.randint(0, 1) == 0:
            return 'Второй игрок'
        return 'Первый игрок'




def play(plaerTile, computerTile, enemy):
    showHints = False
    turn = getFirstMove(enemy)
    print(f'{turn} ходит первым.')

    # очистить игровое поле и поставить игровые фиши
    board = createBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'



print('Приветствуем в игре "Риверси"!')
print('Правила игры:')
print('В игре используется поле размером 8х8 клеток и фишки - Х и О (это все буквы английского алфавита);')
print(
    'Когда игрок помещает фишку на поле, все фишки противника, которые находятся между новой фишкой '
    'и остальними фишками игрока, переворачиваются;')
print('Выигрывает тот игрок, у которого на поле осталось больше всегоо фишек.')

enemy = askEnemy()
