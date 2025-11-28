import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
def draw_graph(adjacency_matrix):
    # Создаем пустой граф
    G = nx.Graph()
    # Определяем количество вершин из размера матрицы
    num_vertices = len(adjacency_matrix)
    # Добавляем ребра на основе матрицы смежности
    for i in range(num_vertices):
        for j in range(i, num_vertices):
            if adjacency_matrix[i][j] > 0:
                G.add_edge(i, j, weight=adjacency_matrix[i][j])
    # Определяем позицию вершин на графике
    pos = nx.spring_layout(G)
    # Рисуем граф
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # Показываем график
    plt.show()
def create_assembly_graph(adjacency_matrix):
    n = len(adjacency_matrix)
    G = nx.Graph()
    # Начальный цикл для добавления всех начальных узлов в граф
    for i in range(n):
        G.add_node((i,), subset=0)  # Начальный уровень у всех узлов равен 0
    current_level = 0
    nodes = [(i,) for i in range(n)]
    while len(nodes) > 1:
        next_nodes = []
        used = set()
        current_level += 1
        for i in range(len(nodes)):
            if nodes[i] in used:
                continue
            max_weight = -1
            best_j = -1
            for j in range(len(nodes)):
                if i != j and nodes[j] not in used:
                    weight = sum(adjacency_matrix[a][b] for a in nodes[i] for b in nodes[j])
                    if weight > max_weight:
                        max_weight = weight
                        best_j = j
            if best_j != -1:
                new_node = nodes[i] + nodes[best_j]
                next_nodes.append(new_node)
                used.add(nodes[i])
                used.add(nodes[best_j])
                G.add_node(new_node, subset=current_level)
                G.add_edge(nodes[i], new_node, weight=max_weight)
                G.add_edge(nodes[best_j], new_node, weight=max_weight)
            else:
                next_nodes.append(nodes[i])
        nodes = next_nodes
    return G
def plot_graph(G):
    pos = nx.multipartite_layout(G, subset_key="subset")
    weights = nx.get_edge_attributes(G, 'weight')
    # Определяем цветовую карту уровня
    levels = sorted(set(nx.get_node_attributes(G, "subset").values()))
    colors = plt.cm.viridis(np.linspace(0, 1, len(levels)))
    # Назначаем цвета вершинам
    node_colors = [colors[G.nodes[node]["subset"]] for node in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    plt.show()
