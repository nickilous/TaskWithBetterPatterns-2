
from Identifiable import Identifiable
from typing import List

class Graph:
  @classmethod
  def create_from_nodes(cls, nodes: List[Identifiable]):
      return Graph(len(nodes), len(nodes), nodes)

  @classmethod
  def fromRaw(cls, nodes: List, weights: List) -> 'Graph':
    graph = Graph.create_from_nodes(nodes)
    row = 0
    col = 0
    for source in nodes:
        col = 0
        for weight in weights[row]:
            destination = nodes[col]
            try:
                floatWeight = float(weight)
                graph.connect(source, destination, floatWeight)
            except ValueError:
                pass
            col += 1
        #graph.addVertex(source)
        row += 1
    return graph
  
  def __init__(self, row, col, nodes: List[Identifiable] = []):
    # set up an adjacency matrix
    self.adj_mat = [[0] * col for _ in range(row)]
    self.nodes = nodes
    # for i in range(len(self.nodes)):
    #     self.nodes[i].id = i

  # Conncects from node1 to node2
  # Note row is source, column is destination
  # Updated to allow weighted edges (supporting dijkstra's alg)
  def connect_dir(self, node1: Identifiable, node2: Identifiable, weight = 1):
    node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
    self.adj_mat[node1][node2] = weight
  
  # Optional weight argument to support dijkstra's alg
  def connect(self, node1: Identifiable, node2: Identifiable, weight = 1):
    self.connect_dir(node1, node2, weight)
    self.connect_dir(node2, node1, weight)

    # Get node row, map non-zero items to their node in the self.nodes array
    # Select any non-zero elements, leaving you with an array of nodes
    # which are connections_to (for a directed graph)
    # Return value: array of tuples (node, weight)
  def connections_from(self, node: Identifiable):
    node = self.get_index_from_node(node)
    return [(self.nodes[col_num], self.adj_mat[node][col_num]) for col_num in range(len(self.adj_mat[node])) if self.adj_mat[node][col_num] != 0]

  # Map matrix to column of node
  # Map any non-zero elements to the node at that row index
  # Select only non-zero elements
  # Note for a non-directed graph, you can use connections_to OR
  # connections_from
  # Return value: array of tuples (node, weight)
  def connections_to(self, node: Identifiable):
    node = self.get_index_from_node(node)
    column = [row[node] for row in self.adj_mat]
    return [(self.nodes[row_num], column[row_num]) for row_num in range(len(column)) if column[row_num] != 0]
     
  
  def print_adj_mat(self):
    for row in self.adj_mat:
      print(row)
  
  def node(self, index):
    return self.nodes[index]
    
  
  def remove_conn(self, node1: Identifiable, node2: Identifiable):
    self.remove_conn_dir(node1, node2)
    self.remove_conn_dir(node2, node1)
   
  # Remove connection in a directed manner (nod1 to node2)
  # Can accept index number OR node object
  def remove_conn_dir(self, node1: Identifiable, node2: Identifiable):
    node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
    self.adj_mat[node1][node2] = 0   
  
  # Can go from node 1 to node 2?
  def can_traverse_dir(self, node1: Identifiable, node2: Identifiable):
    node1, node2 = self.get_index_from_node(node1), self.get_index_from_node(node2)
    return self.adj_mat[node1][node2] != 0  
  
  def has_conn(self, node1: Identifiable, node2: Identifiable):
    return self.can_traverse_dir(node1, node2) or self.can_traverse_dir(node2, node1)
  
  def add_node(self,node: Identifiable):
    self.nodes.append(node)
    node.index = len(self.nodes) - 1
    for row in self.adj_mat:
      row.append(0)     
    self.adj_mat.append([0] * (len(self.adj_mat) + 1))

  # Get the weight associated with travelling from n1
  # to n2. Can accept index numbers OR node objects
  def get_weight(self, n1: Identifiable, n2: Identifiable):
      node1, node2 = self.get_index_from_node(n1), self.get_index_from_node(n2)
      return self.adj_mat[node1][node2]
  
  # Allows either node OR node indices to be passed into 
  def get_index_from_node(self, node: Identifiable):
      if not isinstance(node, Identifiable) and not isinstance(node, int):
        raise ValueError("node must be an integer or Identifiable")
      if isinstance(node, int):
        return node
      else:
        return node.id
    
  def dijkstra(self, startNode: Identifiable, endNode: Identifiable) -> int:
    # Get index of node (or maintain int passed in)
    nodenum = self.get_index_from_node(startNode)
    # Make an array keeping track of distance from node to any node
    # in self.nodes. Initialize to infinity for all nodes but the 
    # starting node, keep track of "path" which relates to distance.
    # Index 0 = distance, index 1 = node hops
    dist = [None] * len(self.nodes)
    for i in range(len(dist)):
      dist[i] = [float("inf")]
      dist[i].append([self.nodes[nodenum]])
        
    dist[nodenum][0] = 0
    # Queue of all nodes in the graph
    # Note the integers in the queue correspond to indices of node
    # locations in the self.nodes array
    queue = [i for i in range(len(self.nodes))]
    # Set of numbers seen so far
    seen = set()
    while len(queue) > 0:
      # Get node in queue that has not yet been seen
      # that has smallest distance to starting node
      min_dist = float("inf")
      min_node = None
      for n in queue: 
        if dist[n][0] < min_dist and n not in seen:
          min_dist = dist[n][0]
          min_node = n
            
      # Add min distance node to seen, remove from queue
      queue.remove(min_node)
      seen.add(min_node)
      if endNode.id in seen:
        result = dist[endNode.id][0]
        return result
      # Get all next hops 
      connections = self.connections_from(min_node)
      # For each connection, update its path and total distance from 
      # starting node if the total distance is less than the current distance
      # in dist array
      for (node, weight) in connections: 
        tot_dist = weight + min_dist
        if tot_dist < dist[node.id][0]:
          dist[node.id][0] = tot_dist
          dist[node.id][1] = list(dist[min_node][1])
          dist[node.id][1].append(node)
    return dist

  def __str__(self) -> str:
    string = ""
    for index in range(len(self.nodes)):
      string += "\n\n Starting Location:\n ---------------------\n"
      string += str(self.nodes[index])
      string += "Distances: \n ----------------------------\n"
      string += str(self.adj_mat[index])
    return string
  
  def __repr__(self) -> str:
      return self.__str__()