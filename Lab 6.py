# I used a adjacency matrix graph
class GraphAM:
    def __init__(self, vertices, weighted=False, directed=False):
        self.am = []
        for i in range(vertices):
            self.am.append([0] * vertices)
        self.directed = directed
        self.weighted = weighted
        self.representation = 'AM'

    def is_valid_vertex(self, u):
        return 0 <= u < len(self.am)

    def insert_vertex(self):
        for lst in self.am:
            lst.append(0)
        new_row = [0] * (len(self.am) + 1)
        self.am.append(new_row)
        return len(self.am) - 1

    def insert_edge(self, src, dest, weight=1):
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return
        self.am[src][dest] = weight
        if not self.directed:
            self.am[dest][src] = weight

    def delete_edge(self, src, dest):
        self.insert_edge(src, dest, 0)

    def num_vertices(self):
        return len(self.am)

    def num_edges(self):
        count = 0
        for lst in self.am:
            for edge_weight in lst:
                if edge_weight != 0:
                    count += 1
        return count

    def edge_weight(self, src, dest):
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return 0
        return self.am[src][dest]

    def num_of_self_edges(self):
        count = 0
        for i in range(len(self.am)):
            if self.am[i][i] != 0:
                count += 1
        return count

    def contains_cycle(self):
        dsf = DisjointSetForest(self.num_vertices())
        for i in range(len(self.am)):
            for j in range(len(self.am)):
                if self.am[i][j] != 0:
                    if dsf.find(i) == dsf.find(j):
                        return True
                    dsf.union(i, j)
        return False

    def display(self):
        print('[', end='')
        for i in range(len(self.am)):
            print('[', end='')
            for j in range(len(self.am[i])):
                edge = self.am[i][j]
                if edge != 0:
                    print('(' + str(j) + ',' + str(edge) + ')', end='')
            print(']', end=' ')
        print(']')

# Creates a dictionary with a tuple of source and destination as key and weight of edge as value
    def get_edges(self):
        dict = {}
        for i in range(len(self.am)):
            for j in range(len(self.am)):
                if self.am[i][j] != 0:
                    dict[(i, j)] = self.am[i][j]
        return dict

# Gets number of indegrees for all vertices
    def in_degrees(self):
        in_degree = []
        for i in range(len(self.am)):
            count = 0
            for j in range(len(self.am)):
                if self.am[j][i] != 0:
                    count += 1
            in_degree.append(count)
        return in_degree

# Gets the vertices that the current vertex is pointing to.
    def get_adj_vertices(self, vertices):
        adj_vertices = []
        for i in range(len(self.am)):
            if self.am[vertices][i] != 0:
                adj_vertices.append(i)
        return adj_vertices


class Queue:
    def __init__(self):
        self.queue = []

    def put(self, item):
        self.queue.append(item)

    def get(self):
        if self.is_empty():
            return
        a = self.queue[0]
        del self.queue[0]
        return a

    def is_empty(self):
        return len(self.queue) == 0

class DisjointSetForest:
    def __init__(self, n):
        self.forest = [-1] * n

    def is_index_valid(self, index):
        return 0 <= index < len(self.forest)

    def find(self, a):
        if not self.is_index_valid(a):
            return -1
        if self.forest[a] < 0:
            return a
        self.forest[a] = self.find(self.forest[a])
        return self.forest[a]

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self.forest[rb] = ra

    def in_same_set(self, a, b):
        if self.find(a) == self.find(b):
            return True
        return False

    def __str__(self):
        return str(self.forest)


def kruskals_algorithm(graph):
    new_graph = GraphAM(graph.num_vertices(), weighted=True, directed=True)
    dict = graph.get_edges()
    list = []
    for i in dict:
        if dict[i] not in list:
            list.append(dict[i])
    list.sort()
    for i in list:
        for j in dict:
            if dict[j] == i:
                new_graph.insert_edge(j[0], j[1], i)
                if new_graph.contains_cycle():
                    new_graph.delete_edge(j[0], j[1])
    return new_graph

def topological_sort(graph):
    in_degrees = graph.in_degrees()
    sort_result = []
    q = Queue()
    for i in range(len(in_degrees)):
        if in_degrees[i] == 0:
            q.put(i)
    while not q.is_empty():
        u = q.get()
        sort_result.append(u)
        for adj_vertex in graph.get_adj_vertices(u):
            in_degrees[adj_vertex] -= 1
            if in_degrees[adj_vertex] == 0:
                q.put(adj_vertex)
    if len(sort_result) != graph.num_vertices():
        return None
    return sort_result

def main():
    graph = GraphAM(6, weighted=True, directed=True)
    graph.insert_edge(0, 1, 5)
    graph.insert_edge(0, 2, 9)
    graph.insert_edge(1, 2, 1)
    graph.insert_edge(3, 4, 12)
    graph.insert_edge(2, 3, 8)
    graph.insert_edge(1, 5, 1)
    graph.insert_edge(4, 5, 18)
    graph.display()
    print(topological_sort(graph))
    ########################## Topological Sort #########################
    graph.insert_edge(5, 3, 69)
    graph.display()
    kruskals_algorithm(graph).display()
    ########################## Kruskals Algorithm #######################

main()

