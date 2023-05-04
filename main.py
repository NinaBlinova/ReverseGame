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


def isValidMove(board, tile, xstart, ystart):
    # Вернуть False, если ход игрока в клетку с координатами xstart, ystart - недопустимыъ
    # если это допустимый ход, то вернуть список клеток, который присвоил бы игрок, если сделал бы туда свой ход
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    if tile == 'X':
        counterTile = 'O'
    else:
        counterTile = 'X'
    tilesToFlip = []
    # проверка каждого из восьми направлений. Чтобы ход был допустимым, игрок должен перевернуть хотя бы одну из
    # фишек противника
    for xstep in [-1, 0, 1]:
        for ystep in [-1, 0, 1]:
            x, y = xstart, ystart
            x += xstep  # первый шаг в направлении х
            y += ystep  # первый шаг в направлении у
            while isOnBoard(x, y) and board[x][y] == counterTile:
                # продолжаем двигаться в направлении х и у
                x += xstep
                y += ystep
                if isOnBoard(x, y) and board[x][y] == tile:
                    # есть фишки, которые можно перевернуть. Двигаться в обратном направлении до достижеия исходной
                    # клетки, отмечая все фишки на этом пути
                    while True:
                        x -= xstep
                        y -= ystep
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])
    if len(tilesToFlip) == 0:  # если ни одна из фишек не первернулась, это недопустимый ход
        return False
    return tilesToFlip


# начальный вид поля игры reverse
def createBoard():
    # создать структуру данных нового чистого игрового поля
    board = []
    for i in range(width):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board


def isOnBoard(x, y):
    # Вернуть True, если координаты есть на игровом поле
    return x >= 0 and x <= width - 1 and y >= 0 and y <= height - 1


def createBoardWithValidMoves(board, tile):
    # вернуть новое поле с точками, обозначающими допустимые ходы, которые может сделать игрок first
    clone = cloneBoard(board)

    for x, y in findValidMoves(clone, tile):
        clone[x][y] = tile.lower()
    return clone


def takeBoardWithValidMovesSecond(board, tile):
    # вернуть новое поле с точками, обозначающими допустимые ходы, которые может сделать игрок second
    clone = cloneBoard(board)

    for x, y in findValidMoves(clone, tile):
        clone[x][y] = tile.lower()
    return clone


def findValidMoves(board, tile):
    # вернуть список списков с координатими х и у допустимых ходов для данного игрока на данном игровом поле
    movies = []
    for x in range(width):
        for y in range(height):
            if isValidMove(board, tile, x, y) != False:
                movies.append([x, y])
    return movies


def calculateScore(board):
    # определить кол-во очков, подсчитав фишки. Вернуть словарь с лючами 'X' и 'O'
    xscore = 0
    oscore = 0
    for x in range(width):
        for y in range(height):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def askTile():
    # позволяет игроку ввести выбранную фишку
    # возвращает список с фишкой игрокав качестве первого элемента и фишкой компьютера в качесте второй
    tile = ''

    while not (tile == 'X' or tile == 'O'):
        print('Вы играете за Х или О?')
        tile = input().upper()
    # Первый элемент в списке - фишка игрока, второй элемент - фишка компьюткра
    if tile == 'X':
        return ['X', 'O']
    return ['O', 'X']




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


def applyMove(board, tile, xstart, ystart):
    # поместить фишку на игровое поле в позицию xstart, ystart и перевернуть какую-либо фишку противника

    # вернуть False, если это недопустимый ход, вернуть True, еси допустимый

    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def cloneBoard(board):
    # сделать копию списка board и вернуть ее
    clone = createBoard()

    for x in range(width):
        for y in range(height):
            clone[x][y] = board[x][y]
    return clone


def isCorner(x, y):
    # Вернуть True, если указанная позиция находится в одном из четырех углов
    return (x == 0 or x == width - 1) and (y == 0 or y == height - 1)


def takePlayerMove(board, playerTile):
    # позволить игроку ввести свой ход
    # вернуть ход в виде [x, y] (или вернуть строки "подсказка" или "выход"
    validDigits = ['1', '2', '3', '4', '5', '6', '7', '8']
    while True:
        print('укажите ход, текст для завершения игры - exit или для вывода подсказки - help.')
        move = input().lower()
        if move == 'exit' or move == 'help':
            return move
        elif len(move) == 2 and move[0] in validDigits and move[1] in validDigits:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('Это недопустимый ход. Введите номер столбца от 1 до 8 и номер ряда от 1 до 8.')
            print('К примеру, значение 81 перемещает в верхний правый угол.')
    return [x, y]


def calculateComputerMove(board, computerTile):
    # учитывая данное игровое поле и данную фишку компьютера, определить,
    # куда делать ход,  вернуть этот ход в виде списка [x, y]
    possibleMoves = findValidMoves(board, computerTile)
    random.shuffle(possibleMoves)  # сделать случайным порядок ходов
    # всегда делать ход в угол, если это возможно
    for x, y in possibleMoves:
        if isCorner(x, y):
            return [x, y]
    # найти ход с наибольшим возможным количеством очков
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = cloneBoard(board)
        applyMove(boardCopy, computerTile, x, y)
        score = calculateScore(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def printScore(board, playerTile, computerTile):
    score = calculateScore(board)
    print(f'Ваш счет: {score[playerTile]}. Счет компьютера: {score[computerTile]}.')




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
    while True:
        if enemy == '1':
            playerValidMoves = findValidMoves(board, playerTile)
            computerValidMoves = findValidMoves(board, computerTile)
            if playerValidMoves == [] and computerValidMoves == []:
                return board  # ходов нет ни у кого, так что окончить игру
            elif turn == 'Человек':  # ход человека
                if playerValidMoves != []:
                    if showHints:
                        validMovesBoard = createBoardWithValidMoves(board, playerTile)
                        drawBoard(validMovesBoard)
                    else:
                        drawBoard(board)
                    printScore(board, plaerTile, computerTile)
                    move = takePlayerMove(board, playerTile)
                    if move == 'exit':
                        print('Бдагодарим за игру!')
                        sys.exit()  # завершить работу программы
                    elif move == 'help':
                        showHints = not showHints
                        continue
                    else:
                        applyMove(board, plaerTile, move[0], move[1])
                turn = 'Компьютер'
            elif turn == 'Компьютер':  # ход Компьютерa
                if computerValidMoves != []:
                    drawBoard(board)
                    printScore(board, plaerTile, computerTile)

                    input('нажмите клавишу Enter для просмотра хода компьютера')
                    move = calculateComputerMove(board, computerTile)
                    applyMove(board, computerTile, move[0], move[1])
                turn = 'Человек'




print('Приветствуем в игре "Риверси"!')
print('Правила игры:')
print('В игре используется поле размером 8х8 клеток и фишки - Х и О (это все буквы английского алфавита);')
print(
    'Когда игрок помещает фишку на поле, все фишки противника, которые находятся между новой фишкой '
    'и остальними фишками игрока, переворачиваются;')
print('Выигрывает тот игрок, у которого на поле осталось больше всегоо фишек.')

enemy = askEnemy()

if enemy == '1':
    playerTile, computerTile = askTile()

    while True:
        finalBoard = play(playerTile, computerTile, enemy)

        # Отобразить итоговый счет
        drawBoard(finalBoard)
        scores = calculateScore(finalBoard)
        print(f'X набрал {scores["X"]}. О набрал {scores["O"]}.')
        if scores[playerTile] > scores[computerTile]:
            print(
                f'Вы победили компьютер, обогнав его на {scores[playerTile] - scores[computerTile]} очков! Позравляю!')
        elif scores[playerTile] < scores[computerTile]:
            print(
                f'Вы проиграли, компьютер обогнал вас на {scores[computerTile] - scores[playerTile]} очков!')
        else:
            print('Ничья!')

        print('Хотите сыграть еще? (yes или no)')
        if not input().lower().startswith('y'):
            break


