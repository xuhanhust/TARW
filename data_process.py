
def data_load(path, id):
    nodes = []
    edges = []
    target_nodes = []

    pathlist1 = path + str(id) + '.txt'
    file = open(pathlist1)

    for line in file:
        source, target = line.split(' ')
        nodes.append(int(source))
        nodes.append(int(target))
        edges.append((int(source), int(target)))

    pathlist2 = path + 'target\\'+str(id) + '.txt'
    file2 = open(pathlist2)  #target
    for line in file2:
        nodes2 = line
        target_nodes.append(int(nodes2))

    nodes = list(set(nodes))
    target_nodes = list(set(target_nodes))
    data_stastics(nodes, edges, target_nodes)

    return nodes, edges, target_nodes


def data_stastics(nodes, edges, target_nodes):
    num_nodes = len(nodes)
    num_edges = len(edges)
    num_target_nodes = len(target_nodes)

    print('Number of Nodes: {}'.format(num_nodes))
    print('Number of Edges: {}'.format(num_edges))
    print('Number of Target Nodes: {}'.format(num_target_nodes))