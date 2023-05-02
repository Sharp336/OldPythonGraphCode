import networkx as nx

print('No') if len(list(nx.simple_cycles(nx.DiGraph([i.split(',') for i in input('Введите пары: выше,ниже выше,ниже\nДля окончания enter\n\n').split(' ')])))) != 0 else print('Yes')
