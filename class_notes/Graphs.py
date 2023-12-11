class Node(object):
    def __init__(self,name):
        '''Assumes name is a string'''
        self.name = name 
    def get_name(self):
        return self.name 
    def __str__(self):
        return self.name 

class Edge(object):
    def __init__(self, src, dest):
        '''Assumes src and dest are nodes'''
        self.src = src 
        self.dest = dest
    def get_source(self):
        return self.src 
    def get_destination(self):
        return self.dest 
    def __str__(self):
        return self.src.get_name() + '->' + self.dest.get_name()

class WeightedEdge(Edge):
    def __init__(self,src, dest, weight=1):
        '''Assumes src and dest are nodes, weight a float'''
        self.src = src 
        self.dest = dest 
        self.weight = weight
    def get_weight(self):
        return self.weight 
    def __str__(self):
        return self.src.get_name() + '->(' + str(self.weight) + ')'\
            + self.dest.get_name()
            
class Digraph(object):
    # nodes is alist of the nodes in the graph
    # edges is a dict mapping each node to a list of its children 
    def __init__(self):
        self.nodes = []
        self.edges = {}
        
    def add_node(self,node):
        if node in self.nodes:
            raise ValueError('Duplicate Node')
        else:
            self.nodes.append(node)
            self.edges[node] = []
    def add_edge(self,edge):
        src = edge.get_source()
        dest = edge.get_destination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def children_of(self,node):
        return self.edges[node]
    def has_node(self,node):
        return node in self.nodes 
    def __str__(self):
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.get_name() + '->'\
                    + dest.get_name() + '\n'
        return result[:-1]
    
class Graph(Digraph):
    def add_edge(self,edge):
        Digraph.add_edge(self,edge)
        rev = Edge(edge.get_destination(), edge.get_source())
        Digraph.add_edge(self,rev)
        
        
def print_path(path):
    '''Assumes path is a list of Nodes'''
    result = '' 
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result 

def DFS(graph, start, end, path, shortest):
    '''
    Assumes graph is a Digraph; start and end are nodes;
        path and shortest are lists of nodes 
        Returns a shortest path from start to end in graph
    '''
    path = path + [start]
    print('Current DFS path:',print_path(path))
    if start == end:
        return path 
    for node in graph.children_of(start):
        if node not in path: #avoid cycles
            if shortest == None or len(path) < len(shortest):
                new_path = DFS(graph, node, end, path, shortest)
                if new_path != None:
                    shortest = new_path 
    return shortest

def search(graph, start,end):
    '''
    Assumes graph is a Digraph; start and end are nodes
    Returns the shortest path from start to end in graph
    '''
    return DFS(graph, start, end, [], None)

def testSP():
    nodes = []
    for name in range(6): #create 6 nodes
        nodes.append(Node(str(name)))
    g = Digraph()
    for n in nodes:
        g.add_node(n)
    g.add_edge(Edge(nodes[0],nodes[1]))
    g.add_edge(Edge(nodes[1],nodes[2]))
    g.add_edge(Edge(nodes[2],nodes[3]))
    g.add_edge(Edge(nodes[2],nodes[4]))
    g.add_edge(Edge(nodes[3],nodes[4]))
    g.add_edge(Edge(nodes[3],nodes[5]))
    g.add_edge(Edge(nodes[0],nodes[2]))
    g.add_edge(Edge(nodes[1],nodes[0]))
    g.add_edge(Edge(nodes[3],nodes[1]))
    g.add_edge(Edge(nodes[4],nodes[0]))
    sp = search(g,nodes[0],nodes[5])
    print('Shortest path found by DFS:', print_path(sp))
    sp = BFS(g, nodes[0],nodes[5])
    print('Shortest path found by BFS:',print_path(sp))

def BFS(graph, start, end):
    '''
    Assumes graph is a Digraph; start and end are nodes;
    Returns a shortest path from start to end in graph
    '''
    init_path = [start]
    path_queue = [init_path]
    while len(path_queue) != 0:
        # Get and remove oldest element in PathQueue
        tmp_path = path_queue.pop(0)
        print('Current BFS path:', print_path(tmp_path))
        last_node = tmp_path[-1]
        if last_node == end:
            return tmp_path
        for next_node in graph.children_of(last_node):
            if next_node not in tmp_path:
                new_path = tmp_path + [next_node]
                path_queue.append(new_path)
    return None