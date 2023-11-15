import random
import matplotlib.pyplot as plt

class CityGrid:
    '''
            Карта символов: [](Пустая) - Свободная клетка
                            # - Блок
                            $ - Блок покрытый
                            T - Башня
                            @ - Зона покрытая
                            | - Граница карты

    '''
    def __init__(self, x, y, proc_blocks):
        #Инициализируем переменные с которыми будем работать большую часть времени
        self.N = x
        self.M = y
        self.cityMatrix = []

        #Запланяем карту клетками
        for i in range(y):
            row = []
            for j in range(x):
                #Генерируем клетку и расставляем блоки с учетом вероятности
                if random.random() > proc_blocks:
                    row.append(" ")
                else:
                    row.append("#")
            self.cityMatrix.append(row)

    def placeTower(self, x, y):
        #Проверяем установили ли значение радиуса. Если нет, то возвращаем ошибку
        if self.coverage== None:
            print("Невозможно установить башню т.к не задан радиус")
            return

        #Ставим башню по координатам и реализуем радиус ее действия. Так же расставляем символы для лучшей отрисвки карты
        self.cityMatrix[y][x] = "T"
        for i in range(max(0, y - self.coverage), min(self.M, y + self.coverage + 1)):
            for j in range(max(0, x - self.coverage), min(self.N, x + self.coverage + 1)):
                if self.cityMatrix[i][j] != "T":
                    if self.cityMatrix[i][j] == "#":  # Если сигнал покрывает блок
                        self.cityMatrix[i][j] = "$"
                    else:
                        self.cityMatrix[i][j] = "@"

    #Функция чтобы задать радиус действия башен
    def setCoverage(self,coverage):
        self.coverage = coverage

    def towerPlacement(self):
        '''
        Алгаритм распределения будет работать следующим образом.
        Сначала мы определяем какая высоата и ширина у квадрата который покрывает связью территорию,
        Далее, определяем сколько в среднем нужно будет поставить вышек
        '''

        for i in range(0, self.M, 2 * self.coverage + 1):
            for j in range(0, self.N, 2 * self.coverage + 1):
                #Создаем начальную точку расположения башни, где предположительно нету блока
                pointY = i + self.coverage
                pointX = j + self.coverage

                if 0 <= pointY < self.M and 0 <= pointX < self.N and self.cityMatrix[pointY][pointX] != "#": #Если блока нету - ставим башню
                    self.placeTower(pointX, pointY)
                else:
                    # Ищем ближайшие доступные точки для установки башни вокруг центральной точки
                    # Перебираем близлежащие точки от изначальной позиции и проверяем есть ли возможность установить башню
                    for dy in range(-1 * self.coverage, self.coverage+1):
                        for dx in range(-1 * self.coverage, self.coverage+1):
                            newY = pointY + dy
                            newX = pointX + dx
                            if 0 <= newY < self.M and 0 <= newX < self.N and self.cityMatrix[newY][newX] != "#":
                                self.placeTower(newX, newY)
                                break
                        else:
                            continue
                        break

    def visualize(self):
        #Визуализация карты города
        fig, ax = plt.subplots()
        for i in range(self.M):
            for j in range(self.N):
                if self.cityMatrix[i][j] == "#":  # Заблокированные блоки
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='black'))
                elif self.cityMatrix[i][j] == "$": # Покрытые блоки
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='darkcyan'))
                elif self.cityMatrix[i][j] == "T":  # Башни
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='red'))
                elif self.cityMatrix[i][j] == "@":  # Зоны покрытия
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='cyan'))
                else:  # Пустые блоки
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='white', fill=False, linestyle='dotted'))

        ax.set_ylim(0, self.M)
        ax.set_xlim(0, self.N)
        plt.gca().set_aspect('equal', adjustable='box')

        plt.show()


city = CityGrid( 20,20,0.3)
city.setCoverage(2)
city.towerPlacement()
city.visualize()