from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Стрелять можно только в пределах доски!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Стрелять повторно в одну клетку нельзя!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, length, prow, direction):
        self.ln = length
        self.prow = prow
        self.direction = direction
        self.health = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ln):
            current_x = self.prow.x
            current_y = self.prow.y
            if self.direction == 0:
                current_x += i
            elif self.direction == 1:
                current_y += i
            ship_dots.append(Dot(current_x, current_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size
        self.count = 0
        self.area = [["0"] * size for i in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        board = ""
        board += "| 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.area):
            board += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            board = board.replace("■", "0")
        return board

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                current = Dot(d.x + dx, d.y + dy)
                if not (self.out(current)) and current not in self.busy:
                    if verb:
                        self.area[current.x][current.y] = "."
                    self.busy.append(current)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.area[d.x][d.y] = "■"
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()
        self.busy.append(dot)
        for ship in self.ships:
            if ship.shooten(dot):
                ship.health -= 1
                self.area[dot.x][dot.y] = "X"
                if ship.health == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        self.area[dot.x][dot.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, self_board, enemy_board):
        self.self_board = self_board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print("Введите 2 координаты!")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        user = self.random_board()
        ai = self.random_board()
        ai.hid = True
        self.ai = AI(ai, user)
        self.user = User(user, ai)

    def try_board(self):
        board = Board(size=self.size)
        attempts = 0
        lens = [3, 2, 2, 1, 1, 1, 1]
        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("Приветствуем вас в игре морской бой!")
        print("формат ввода : x y")
        print("x - номер строки")
        print("y - номер столбца")

    def print_boards(self):
        print("-" * 20)
        print("Доска пользователя:")
        print(self.user.self_board)
        print("-" * 20)
        print("Доска компьютера:")
        print(self.ai.self_board)
        print("-" * 20)

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2:
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.self_board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Пользователь выиграл!")
                break
            if self.user.self_board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()