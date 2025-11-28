def is_graph_connected(P):
    n = P.shape[0]
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        node = stack.pop()
        for i in range(n):
            if P[node][i] > 0 and not visited[i]:
                stack.append(i)
                visited[i] = True
    return all(visited)
def validate_entry(entry_value):
    # Проверка, что введенное значение - действительно число (целое или вещественное)
    try:
        if entry_value == '-' or entry_value == '' or entry_value == '.' or entry_value == '-.':
            return True
        float(entry_value)
        return True
    except ValueError:
        return False
