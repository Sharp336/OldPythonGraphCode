from itertools import chain, groupby

class Graph:
    def __init__(self, matrix, isoriented = False, vertex_labels=None):  # иницализация экземпляра класса граф: matrix - матричное представление графа, vertex_labels - список имён вершин
        self.isoriented = isoriented
        self.connections = []  # заглушка под будущую конвертацию матрицы графа в список его рёбер
        self.matrix = matrix  # присваиваем введённую матрицу экземпляру класса
        self.vertexes_amount = len(matrix)  # считаем количество вершин
        self.connections_amount = 0  # заглушка под будущее количество рёбер
        if vertex_labels is None or self.vertexes_amount != len(
                vertex_labels):  # если при инициализации не введены имена вершин или количество имён не соответствует количеству вершин
            vertex_labels = [str(x + 1) for x in range(
                self.vertexes_amount)]  # в качестве имён используем цифры 1, 2, 3 и т.д. по количеству вершин
        self.vertex_labels = vertex_labels  # присваиваем имена вершин экземпляру класса


    def matrix_convert(self):  # метод конвертации матричного представления графа в НЕПОВТОРЯЮЩИЙСЯ список его рёбер
        taken_vertexes = 0  # создаём счётчик индекса, до которого мы уже взяли рёбра вершин
        for a in range(self.vertexes_amount):  # для каждого индекса строки матрицы(для каждой вершины)
            for b in range(self.vertexes_amount) if self.isoriented else range(taken_vertexes, self.vertexes_amount):  # для каждого индекса столбца матрицы(для каждой вершины), начиная от ещё не обхваченных вершин (чей индекс больше счётчика)
                if self.matrix[a][b] > 0:  # если вес ребра больше 0(если оно существует)
                    self.connections.append([a, b, self.matrix[a][b]])  # добавить ребро в формате [индекс строки(вершины), индекс столбца(вершины), вес ребра между ними]
            taken_vertexes += 1  # увеличиваем счётчик на уже обхваченную вершину
        self.connections = sorted(self.connections, key=lambda connection: connection[2])  # сортируем список рёбер по возрастанию 3-его элемента(индекс 2, вес ребра) в каждой записи рёбер
        self.connections_amount = len(self.connections)  # присваиваем заглушке актуальное количество рёбер (длинна списка с ними)

    def poisk_zikla(self):
        if self.isoriented:
            if not self.connections: self.matrix_convert()
            graph, sub_graph = {}, {}

            # k - ключ(вершина), it - итерируемый массив дуг(списков-пар)
            for k, it in groupby(sorted([cn[:2] for cn in self.connections]), key=lambda x: x[0]):
                ''' Заполняем словарь graph значениями по типу вершина: вершины к которым от неё идёт дуга (неповторяющиеся, т.к. значение по ключу - множество)
                "e for _" нужно чтобы даже при одной смежной вершине множество корректно объявилось'''
                graph[k] = {e for _, e in it}

            while True:
                ''' set(graph) - множество из ключей словаря graph, по факту - множество вершин из которых есть "выход".
                chain.from_iterable(graph.values()) - цепь из значений по ключам словаря graph, по факту - множество вершин в которые есть "вход".
                Почему используется цепь ? потому что напрямую преобразовать graph.values() в одномерный массив для поиска пересечения нельзя
                (т.к. внутри нехэшируемые множества), а через вложенные генераторы - костыльно. Ну и наконец intersection - ищем пересечение
                множеств вершин с "входом" и с "выходом", таким образом оставляя только те, которые потенциально могут являться частью цикла'''

                vertex_set = set(graph).intersection(chain.from_iterable(graph.values()))
                sub_graph = {k: vertex_set & vs for k, vs in graph.items() if k in vertex_set and vertex_set & vs}
                if sub_graph == graph: break
                else: graph = sub_graph

            # Если есть подграф то он цикличен
            print("Цикл найден" if graph else "Цикл не найден")

        else: print('Граф неориентированный, поиск цикла невозможен')





    # алгоритм Прима https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9F%D1%80%D0%B8%D0%BC%D0%B0
    def prima(self):
        free_vertexes = list(range(1, len(self.vertex_labels)))  # создаём список индексов вершин без одной(начальной)
        tied = [0]  # создаём список посещённых вершин, по дефолту сразу берём начальную - первую(0 индекс)
        road_length = 0  # создаём счётчик веса всего остовного дерева
        print(f'\n\n\n\n\nНачинаем алгоритм Прима с {self.vertex_labels[0]} вершины\n')

        while free_vertexes:  # пока есть непосещённые вершины
            min_link = None  # самое маленькое ребро на текущем шаге
            overall_min_path = float('inf')  # вес самого маленького ребра на этом шаге

            for current_vertex in tied:  # для индекса каждой ПОСЕЩЁННОЙ вершины
                weights = self.matrix[current_vertex]  # берём вес её рёбер из матрицы
                min_path = float('inf')  # самое маленькое ребро для этой вершины
                free_vertex_min = current_vertex  # вершина к которой идёт от текущей рассматривающейся(посещённой) самое маленькое ребро

                for vertex in range(self.vertexes_amount):  # для индекса каждой из ВСЕХ вершин матрицы
                    vertex_path = weights[vertex]  # берём вер ребра до неё от рассматриваемой посещённой

                    if vertex_path == 0:
                        continue  # если вес 0(ребра нет), переходим к следующей

                    elif vertex in free_vertexes and vertex_path < min_path:  # если вершина ещё не находится в посещённых и путь к ней меньше уже найденного от текущей рассматривающейся(посещённой)
                        free_vertex_min = vertex  # обновляем вершину к которой идёт от текущей рассматривающейся(посещённой) самое маленькое ребро
                        min_path = vertex_path  # обновляем самое маленькое ребро для этой вершины(текущей рассматривающейся - посещённой)

                if free_vertex_min != current_vertex and overall_min_path > min_path:  # если найденная ближайшая вершина не является рассматривающейся и найденное минимальное ребро меньше уже найденного на этом шаге
                    min_link = (current_vertex,
                                free_vertex_min)  # присваиваем минимальное ребро на этом шаге (рассматриваемая вершина, ближайшая к ней)
                    overall_min_path = min_path  # присваиваем минимальный вес ребра на текущем шаге

            print(
                f'Соединяем {self.vertex_labels[min_link[0]]} вершину с {self.vertex_labels[min_link[1]]}, длинна {overall_min_path}')

            road_length += overall_min_path  # добавляем к счётчику веса остовного дерева вес найденного ребра
            free_vertexes.remove(min_link[1])  # удаляем найденную ближайшую вершину из непосещённых
            tied.append(min_link[1])  # и добавляем в посещённые

        print(f'\nДлинна пути: {road_length}')

    # алгоритм Краскала https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9A%D1%80%D0%B0%D1%81%D0%BA%D0%B0%D0%BB%D0%B0
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def kraskal(self):
        print(f'\n\n\n\n\nНачинаем алгоритм Краскала\n')
        self.matrix_convert()  # конвертируем матрицу в список рёбер
        road_length = 0  # создаём счётчик веса всего остовного дерева
        i, taken_vertexes = 0, 0  # создаём счётчик индекса по которому берём ребро из упорядоченного списка и счётчик посещённых вершин
        parent, rank = [], []  # rank - количество взятых рёбер выходящих из вершины по индексу
        for vertex in range(self.vertexes_amount):
            parent.append(vertex)
            rank.append(0)
        while taken_vertexes < self.vertexes_amount - 1:
            u, v, w = self.connections[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                taken_vertexes += 1
                road_length += w
                xroot, yroot = self.find(parent, x), self.find(parent, y)
                if rank[xroot] < rank[yroot]:
                    parent[xroot] = yroot
                elif rank[xroot] > rank[yroot]:
                    parent[yroot] = xroot
                else:
                    parent[yroot] = xroot
                    rank[xroot] += 1

                print(f'Соединяем {self.vertex_labels[u]} вершину с {self.vertex_labels[v]}, длинна {w}')
        print(f'\nДлинна пути: {road_length}')

    def deikstra(self, start):  # принимаем на вход матрицу графа и индекс начальной вершины
        print(f'\n\n\n\n\nНачинаем алгоритм Дейкстры\n')
        visited = []  # создаём список для посещённых вершин
        distances = {
            start: 0}  # создаём словарь расстояний до каждой из вершин с записями по типу (индекс вершины: наименьшее найденное растояние от начальной)
        vertexes = list(range(self.vertexes_amount))  # создаём список индексов непосещённых вершин
        vertexes.remove(start)  # убираем начальную вершину из непосещённых
        visited.append(start)  # и добавляем в посещённые
        for i in vertexes: distances[i] = self.matrix[start][i]  # для каждого индекса(значения из списка) непосещённых вершин добавляем в словарь расстояний начальное(из соответствующей строки матрицы)
        tovisit = start  # индекс вершины у которой на данном шаге нашли самый короткий путь и которая будет отмечена посещённой
        while vertexes:  # пока есть непосещённые вершины
            distance = float('inf')  # дистанция к ближайшей из рассматриваемых непосещённых вершин
            for i in visited:  # для каждого индекса(значения из списка) посещённых вершин
                for v in vertexes:  # для каждого индекса(значения из списка) непосещённых вершин
                    if self.matrix[i][v] > 0 and self.matrix[i][v] + distances[i] < distance:
                        # если ребро от рассматриваемой посещённой до непосещённой вершин существует(больше 0) и
                        # сумма его длинны(matrix[i][v]) с путём до посещённой вершины откуда оно выходит(distances[i])
                        # меньше дистанции к ближайшей из рассматриваемых непосещённых вершин (distance)
                        distance = distances[v] = distances[i] + self.matrix[i][v]  # присваиваем distance и distances[v](самый короткий путь к вершине с индексом v) значение matrix[i][v] + distances[i]
                        tovisit = v  # назначаем вершину с найденным самым коротким путём на этом шаге
            visited.append(tovisit)  # добавляем её в посещённые
            vertexes.remove(tovisit)  # и удаляем из непосещённых

        for i in distances:
            print(f'Путь от {self.vertex_labels[start]} до {self.vertex_labels[i]} равен {distances[i]}')


# неориентированный взвешенный
# matrix1 = [
#     [0, 7, 9, 0, 0, 14],
#     [7, 0, 10, 15, 0, 0],
#     [9, 10, 0, 11, 0, 2],
#     [0, 15, 11, 0, 6, 0],
#     [0, 0, 0, 6, 0, 9],
#     [14, 0, 2, 0, 9, 0],
# ]
#
# g1 = Graph(matrix1)
# g1.prima()
# g1.kraskal()
#
# неориентированный взвешенный
# matrix2 = [
#     [0, 0, 1, 2, 0, 0, 0, 1, 1, 1, 1, 0],
#     [0, 0, 4, 0, 0, 0, 0, 5, 5, 2, 0, 0],
#     [1, 4, 0, 3, 0, 0, 0, 0, 0, 4, 0, 0],
#     [2, 0, 3, 0, 4, 0, 0, 0, 0, 0, 2, 0],
#     [0, 0, 0, 4, 0, 3, 0, 0, 0, 0, 1, 2],
#     [0, 0, 0, 0, 3, 0, 5, 0, 6, 0, 3, 0],
#     [0, 0, 0, 0, 0, 5, 0, 3, 2, 0, 0, 2],
#     [1, 5, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0],
#     [1, 5, 0, 0, 0, 6, 2, 2, 0, 0, 3, 0],
#     [1, 2, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7],
#     [1, 0, 0, 2, 1, 3, 0, 0, 3, 0, 0, 1],
#     [0, 0, 0, 0, 2, 0, 2, 0, 0, 7, 1, 0]
# ]
#
# g2 = Graph(matrix2)
# g2.prima()
# g2.kraskal()
#
# ориентированный взвешенный граф
# matrix3 = [
#     [0, 16, 13, 0, 0, 0],
#     [0, 0, 10, 0, 12, 0],
#     [0, 4, 0, 14, 0, 0],
#     [0, 0, 0, 0, 7, 4],
#     [0, 0, 9, 0, 0, 20],
#     [0, 0, 0, 0, 0, 0],
#     ]
#
# g3 = Graph(matrix3, True)
# g3.poisk_zikla()
# g3.deikstra(0)

# неориентированный взвешенный
# matrix1 = [
#     [0, 1, 0, 0, 4, 8, 0, 0],
#     [0, 0, 2, 0, 0, 6, 6, 0],
#     [0, 0, 0, 1, 0, 0, 2, 0],
#     [0, 0, 0, 0, 0, 0, 1, 4],
#     [0, 0, 0, 0, 0, 5, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0]
# ]
# неориентированный невзвешенный
# matrix2_neor = [
#     [0, 1, 1, 0, 1, 0, 0],
#     [1, 0, 0, 1, 1, 0, 0],
#     [1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 0, 0],
#     [1, 1, 1, 1, 0, 1, 1],
#     [0, 0, 0, 0, 1, 0, 1],
#     [0, 0, 0, 0, 1, 1, 0],
# ]
# ориентированный невзвешенный
# matrix2_orient = [
#     [0, 0, 1, 0, 1, 0, 0],
#     [1, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 0, 1, 0, 0],
# ]
#
# Graph(matrix1).deikstra(0)
# Graph(matrix2_neor).deikstra(0)
# Graph(matrix2_orient).deikstra(0)
