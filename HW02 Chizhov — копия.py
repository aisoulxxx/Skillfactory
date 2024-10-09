import random

class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hit_points = len(coordinates)

    def is_sunk(self):
        return self.hit_points == 0

    def hit(self, coordinate):
        if coordinate in self.coordinates:
            self.hit_points -= 1
            self.coordinates.remove(coordinate)
            return True
        else:
            return False

class Board:
    def __init__(self, ships):
        self.size = 6
        self.grid = [['О' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = ships
        self.shots_fired = set()

        self.place_ships()

    def place_ships(self):
        for ship in self.ships:
            for (x, y) in ship.coordinates:
                self.grid[x][y] = '■'

    def shoot(self, x, y):
        if (x, y) in self.shots_fired:
            raise ValueError("Already shot at this coordinate.")

        self.shots_fired.add((x, y))

        for ship in self.ships:
            if ship.hit((x, y)):
                self.grid[x][y] = 'X'
                return True

        self.grid[x][y] = 'T'
        return False

    def display(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i, row in enumerate(self.grid):
            print(f"{i + 1} | {' | '.join(row)} |")

    def is_game_over(self):
        return all(ship.is_sunk() for ship in self.ships)


def main():
    # Примеры кораблей
    player_ships = [
        Ship([(0, 0), (0, 1), (0, 2)]),  # Корабль на 3 клетки
        Ship([(1, 3), (1, 4)]),  # Корабль на 2 клетки
        Ship([(4, 4)]),  # Корабль на 1 клетку
        Ship([(5, 0)]),  # Корабль на 1 клетку
        Ship([(2, 2)]),  # Корабль на 1 клетку
        Ship([(3, 0)]),  # Корабль на 1 клетку
    ]

    computer_ships = [
        Ship([(0, 0), (0, 1), (0, 2)]),
        Ship([(1, 3), (1, 4)]),
        Ship([(4, 4)]),
        Ship([(5, 0)]),
        Ship([(2, 2)]),
        Ship([(3, 0)]),
    ]

    player_board = Board(player_ships)
    computer_board = Board(computer_ships)

    while True:
        # Отображение доски игрока
        print("Ваша доска:")
        player_board.display()

        # Получение координат от игрока
        try:
            x, y = map(int, input("Введите координаты (x y): ").split())
            x -= 1
            y -= 1

            if x < 0 or x >= 6 or y < 0 or y >= 6:
                raise ValueError("Координаты вне диапазона.")

            hit = computer_board.shoot(x, y)
            if hit:
                print("Попадание!")
            else:
                print("Промах!")

            if computer_board.is_game_over():
                print("Поздравляем! Вы победили!")
                break

            # Ход компьютера
            x, y = random.randint(0, 5), random.randint(0, 5)
            print(f"Компьютер стреляет в ({x + 1}, {y + 1})")
            hit = player_board.shoot(x, y)
            if hit:
                print("Компьютер попал!")
            else:
                print("Компьютер промахнулся!")

            if player_board.is_game_over():
                print("Компьютер победил!")
                break

        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
