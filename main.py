# реверси
import random
import sys


# для получения функции exit(), которая возвращает целое число, указывающее статус выхода.

def drawBoard(board):
    horizontalLineOne = '   '
    UpperBorder = '  '
    horizontalLineTwo = '   '
    LowerBorder = '  '

    for i in range(size):
        if i != size - 1:
            horizontalLineOne += str(i + 1) + ' '
        else:
            horizontalLineOne += str(i + 1)
    print(horizontalLineOne)

    for i in range(size):
        if i == 0:
            UpperBorder += '┎─'
        elif i > 0 and i < size + 1:
            UpperBorder += '┰─'
    print(UpperBorder + '┒')

    for y in range(size):
        if y < 9:
            print(f' {(y + 1)}┃',
                  end='')  # выводит метку для оси у левой части поля и содержит аргумент - ключевое слово
        # end='', чтобы вместо новой строки не ыводить ничего
        # (по умолчанию идет перевод на новую строку, а тут это не нужно)
        else:
            print(f'{(y + 1)}┃', end='')
        for x in range(size):
            if x > 0:
                print('\'', end='')
            print(board[x][y], end='')
        print(f'┃{(y + 1)}')

    for i in range(size):
        if i == 0:
            LowerBorder += '┖─'
        elif i > 0 and i < size + 1:
            LowerBorder += '┸─'
    print(LowerBorder + '┚')

    for i in range(size):
        if i != size - 1:
            horizontalLineTwo += str(i + 1) + ' '
        else:
            horizontalLineTwo += str(i + 1)
    print(horizontalLineTwo)


def isOnBoard(x, y):
    # Вернуть True, если координаты есть на игровом поле
    return x >= 0 and x <= size - 1 and y >= 0 and y <= size - 1


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
    for i in range(size):
        board.append([' '] * size)
    return board


def findValidMoves(board, tile):
    # вернуть список списков с координатими х и у допустимых ходов для данного игрока на данном игровом поле
    movies = []
    for x in range(size):
        for y in range(size):
            if isValidMove(board, tile, x, y) != False:
                movies.append([x, y])
    return movies


# следующие две функции возвращают структуру данных игрового поля, которая содержит маленькую букву фишки во всех клетках
# ходы в которые допустимы
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


def calculateScore(board):
    # определить кол-во очков, подсчитав фишки. Вернуть словарь с лючами 'X' и 'O'
    xscore = 0
    oscore = 0
    for x in range(size):
        for y in range(size):
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
        tile = input('Вы играете за Х или О? ').upper()
    # Первый элемент в списке - фишка игрока, второй элемент - фишка компьюткра
    if tile == 'X':
        return ['X', 'O']
    return ['O', 'X']


def askEnemy():
    enemy = ''
    while not (enemy == '1' or enemy == '2'):
        enemy = input('Вы играете против компьютера(1) или человека(2)? ').lower()
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


# функция создает структуру данных пустого поля, но затем копирует все позиции в параметре board
# с помощью вложенного цикла
# ИИ использует данную функцию, чтобы была возможность вносить изменения в копию игрового поля,
# не изменяя исходное игровое поле
def cloneBoard(board):
    # сделать копию списка board и вернуть ее
    clone = createBoard()

    for x in range(size):
        for y in range(size):
            clone[x][y] = board[x][y]
    return clone


# нужна для программирования ИИ
def isCorner(x, y):
    # Вернуть True, если указанная позиция находится в одном из четырех углов
    return (x == 0 or x == size - 1) and (y == 0 or y == size - 1)


def takePlayerMove(board, playerTile):
    # позволить игроку ввести свой ход
    # вернуть ход в виде [x, y] (или вернуть строки "подсказка" или "выход"
    validDigits = []
    for i in range(1, size + 1):
        validDigits.append(str(i))
    # Цикл while продолжает выполнение до тех пор, пока игрок не введет допустимый ход.
    # игры ожидает, что игрок введет координаты х и у в виде двух чисел с пробелом
    while True:
        print('укажите ход, текст для завершения игры - exit или для вывода подсказки - help.')
        move = input().lower()
        if move == 'exit' or move == 'help':
            return move
        elif len(move) == 3 and move[0] in validDigits and move[2] in validDigits:
            x = int(move[0]) - 1
            y = int(move[2]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        elif len(move) == 4:
            if move[0] in validDigits and move[1] == ' ' and (move[2] + move[3]) in validDigits:
                x = int(move[0]) - 1
                y = int(move[2] + move[3]) - 1
                if isValidMove(board, playerTile, x, y) == False:
                    continue
                else:
                    break
            elif (move[0] + move[1]) in validDigits and move[2] == ' ' and move[3] in validDigits:
                x = int(move[0] + move[1]) - 1
                y = int(move[3]) - 1
                if isValidMove(board, playerTile, x, y) == False:
                    continue
                else:
                    break
        else:
            print('Это недопустимый ход. Введите номер столбца от 1 до 8 и номер ряда от 1 до 8.')
            print('К примеру, значение 8 1 перемещает в верхний правый угол.')
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


# выводит результаты игры человека и компьютера
def printScore(board, playerTile, computerTile):
    score = calculateScore(board)
    print(f'Ваш счет: {score[playerTile]}. Счет компьютера: {score[computerTile]}.')


# выводит результаты игры человека №1 и человека №2
def printScoreHuman(board, playerFirstTile, playerSecondTile):
    score = calculateScore(board)
    print(f'Счет первого игрока: {score[playerFirstTile]}. Счет второго игрока: {score[playerSecondTile]}.')


def play(plaerTile, computerTile, enemy):
    showHints = False
    turn = getFirstMove(enemy)
    print(f'{turn} ходит первым.')

    # очистить игровое поле и поставить игровые фиши
    board = createBoard()
    board[int(size / 2) - 1][int(size / 2) - 1] = 'X'
    board[int(size / 2) - 1][int(size / 2)] = 'O'
    board[int(size / 2)][int(size / 2) - 1] = 'O'
    board[int(size / 2)][int(size / 2)] = 'X'
    while True:
        if enemy == '1':
            playerValidMoves = findValidMoves(board, playerTile)
            computerValidMoves = findValidMoves(board, computerTile)
            if playerValidMoves == [] and computerValidMoves == []:
                return board  # ходов нет ни у кого, так что окончить игру
            elif turn == 'Человек':  # ход человека
                # Если включен режим подсказок, т.е. showHints принимает значение True,
                # тогда структура данных должна отобразить подсказки на каждой допустимой для хода игрока клетке.
                # Это осуществляется с помощью функции createBoardWithValidMoves().
                # Она возвращает копию поля с подсказками.
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
                # поток выполнения перезапускает блок else и достигает конца блока while, поэтому интерпритатор
                # возвращается к интсрукции while. На этот раз будет очередб компьютера
                turn = 'Компьютер'
            elif turn == 'Компьютер':  # ход Компьютерa
                if computerValidMoves != []:
                    drawBoard(board)
                    printScore(board, plaerTile, computerTile)
                    input('нажмите клавишу Enter для просмотра хода компьютера')
                    move = calculateComputerMove(board, computerTile)
                    applyMove(board, computerTile, move[0], move[1])
                turn = 'Человек'

        elif enemy == '2':
            playerFirstValidMoves = findValidMoves(board, playerFirstTile)
            playerSecondValidMoves = findValidMoves(board, playerSecondTile)
            if playerFirstValidMoves == [] and playerSecondValidMoves == []:
                return board
            elif turn == 'Первый игрок':
                print('Ходит первый игрок')
                if playerFirstValidMoves != []:
                    if showHints:
                        validMovesBoard = createBoardWithValidMoves(board, playerFirstTile)
                        drawBoard(validMovesBoard)
                    else:
                        drawBoard(board)
                    printScoreHuman(board, playerFirstTile, playerSecondTile)
                    move = takePlayerMove(board, playerFirstTile)
                    if move == 'exit':
                        print('Бдагодарим за игру!')
                        sys.exit()
                    elif move == 'help':
                        showHints = not showHints
                        continue
                    else:
                        applyMove(board, plaerTile, move[0], move[1])
                turn = 'Второй игрок'
            elif turn == 'Второй игрок':
                print('Ходит второй игрок')
                if playerSecondValidMoves != []:
                    if showHints:
                        validMovesBoard = takeBoardWithValidMovesSecond(board, playerSecondTile)
                        drawBoard(validMovesBoard)
                    else:
                        drawBoard(board)
                    printScoreHuman(board, playerFirstTile, playerSecondTile)
                    move = takePlayerMove(board, playerSecondTile)
                    if move == 'exit':
                        print('Бдагодарим за игру!')
                        sys.exit()
                    elif move == 'help':
                        showHints = not showHints
                        continue
                    else:
                        applyMove(board, playerSecondTile, move[0], move[1])
                turn = 'Первый игрок'


print('Приветствуем в игре "Риверси"!')
print('Правила игры:')
print('В игре используется поле размером SIZEхSIZE клеток и фишки - Х и О (это все буквы английского алфавита);')
print(
    'Когда игрок помещает фишку на поле, все фишки противника, которые находятся между новой фишкой '
    'и остальними фишками игрока, переворачиваются;')
print('Выигрывает тот игрок, у которого на поле осталось больше всегоо фишек.')

size = int(input('Введите размер поля: '))
if size % 2 != 0:
    size = size + 1
elif size < 3 or size > 10:
    size = 8
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

elif enemy == '2':
    print('Подсказки для 1-го игрока обозначены маленькой буквой его фишки, а для 2-го - маленькой буквой 2-й фишки.')
    if random.randint(0, 1) == 0:
        print('Первый выбирает фишку второй игрок.')
        playerSecondTile, playerFirstTile = askTile()
    else:
        print('Первый выбирает фишку первый игрок.')
        playerFirstTile, playerSecondTile = askTile()
    while True:
        finalBoard = play(playerFirstTile, playerSecondTile, enemy)

        # Отобразить итоговый счет
        drawBoard(finalBoard)
        scores = calculateScore(finalBoard)
        print(f'X набрал {scores["X"]}. О набрал {scores["O"]}.')
        if scores[playerFirstTile] > scores[playerSecondTile]:
            print(
                f'Первый игрок победил второго на {scores[playerFirstTile] - scores[playerSecondTile]} '
                f'очков! Позравляю!')
        elif scores[playerFirstTile] < scores[playerSecondTile]:
            print(f'Второй игрок поьедил первого на {scores[playerSecondTile] - scores[playerFirstTile]} '
                  f'очков! Позравляю!')
        else:
            print('Ничья!')

        print('Хотите сыграть еще? (yes или no)')
        if not input().lower().startswith('y'):
            break
