class TreeNode:
  def __init__(self, value):
    self.value = value
    self.children = []

  def add_child(self, node):
    self.children.append(node)

  def add_children(self, nodes):
    for node in nodes:
      self.children.append(node)

  def output(self, pos, markerStr="+- ", levelMarkers=[]):
    emptyStr = " "*len(markerStr)
    connectionStr = "|" + emptyStr[:-1]
    level = len(levelMarkers)
    mapper = lambda draw: connectionStr if draw else emptyStr
    markers = "".join(map(mapper, levelMarkers[:-1]))
    markers += markerStr if level > 0 else ""
    
    if isinstance(pos, (tuple, list)):
      out = ''
      for val in pos:
        out += f'{str(val)}: {str(self.value[val]) if val in self.value else self.value["type"]} | '
    else:
      out = f'{str(val)}: {str(self.value[pos]) if pos in self.value else self.value["type"]}'
    print(f"{markers}{out}")
    for i, child in enumerate(self.children):
        isLast = i == len(self.children) - 1
        child.output(pos, markerStr, [*levelMarkers, not isLast])



def get_values_at_depth(root, depth, types):
  # The root node is at depth 0
  current_depth = 0
  # We'll use a queue to keep track of nodes at each level
  queue = [(root, current_depth)]

  while queue:
    current_node, current_node_depth = queue.pop(0)

    # If the current node is at the desired depth, return its value
    if current_node_depth == depth:
      # Get the values of all remaining nodes at this depth
      values = [current_node.value]
      while queue and queue[0][1] == depth:
        if types == None or queue[0][0].value[0] in types:
          values.append(queue.pop(0)[0].value)
        else:
          queue.pop(0)
      return values

    # If the current node is not at the desired depth, add its children to the queue
    for child in current_node.children:
      if types == None or child.value[0] in types:
        queue.append((child, current_node_depth + 1))

  # If no nodes were found at the desired depth, return an empty list
  return []


# for my tree structure of rays
# a node is a segment
# it stores, the ray itself, the the start colour, intersect colour, start intensity, intersect intensity
if __name__ == '__main__':
  # Create a tree
  root = TreeNode(['A', None])  # Dummy root node

  # Add nodes with different types of values
  root_child1 = TreeNode(['A', 1])
  root_child2 = TreeNode(['B', 2])
  root_child3 = TreeNode(['A', 3])
  root_child4 = TreeNode(['C', 4])
  root_child5 = TreeNode(['A', 5])

  root.add_child(root_child1)
  root.add_child(root_child2)
  root.add_child(root_child3)
  root.add_child(root_child4)
  root.add_child(root_child5)

  # Add children to root child nodes
  root_child1_child1 = TreeNode(['D', 6])
  root_child1_child2 = TreeNode(['A', 7])
  
  root_child3_child1 = TreeNode(['A', 8])
  root_child3_child2 = TreeNode(['B', 9])
  root_child4_child1 = TreeNode(['A', 10])
  root_child4_child2 = TreeNode(['B', 11])

  root_child1.add_child(root_child1_child1)
  root_child1.add_child(root_child1_child2)
  root_child3.add_child(root_child3_child1)
  root_child3.add_child(root_child3_child2)
  root_child4.add_child(root_child4_child1)
  root_child4.add_child(root_child4_child2)

  print(root.output())