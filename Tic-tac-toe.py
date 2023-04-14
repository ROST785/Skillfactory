def print_area(area):
    for char in area:
        print(char)
def get_winner(area, turn_char):
    print_area(area)
    print(f"{turn_char} выиграл")
def check_winner(area, turn_char):
    for i in range(3):
        if area[i][0] == turn_char and area[i][1] == turn_char and area[i][2] == turn_char:
            get_winner(area, turn_char)
            return 1
        if area[0][i] == turn_char and area[1][i] == turn_char and area[2][i] == turn_char:
            get_winner(area, turn_char)
            return 1
    if area[0][0] == turn_char and area[1][1] == turn_char and area[2][2] == turn_char:
        get_winner(area, turn_char)
        return 1
    if area[0][2] == turn_char and area[1][1] == turn_char and area[2][0] == turn_char:
        get_winner(area, turn_char)
        return 1
area = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]
for turn in range(1,10):
    if turn % 2:
        turn_char = "X"
    else:
        turn_char = "0"
    print_area(area)
    print(f"Ход номер {turn}")
    print(f"Ходит {turn_char}")
    while True:
        row = int(input(f"Введите номер строки ")) - 1
        column = int(input("Введите номер столбца ")) - 1
        if 0 <= row <= 2 and 0 <= column <= 2:
            if area[row][column] == "*":
                area[row][column] = turn_char
                break
            else:
                print("Эта ячейка занята.")
        else:
            print("Неверный номер строки или столбца")
    if check_winner(area, turn_char) == 1:
        break
    elif turn == 9:
        print_area(area)
        print("Ничья.")