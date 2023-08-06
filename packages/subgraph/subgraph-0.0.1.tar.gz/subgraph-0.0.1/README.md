# Subgraph

## Basic usage:
```python
from subgraph.simplegraph import Subgraph, Subnode, SubgraphNode

subgraph = Subgraph()
node1 = Subnode("simple1", num_outputs=1)
node2 = Subnode("simple2", num_inputs=1)
subgraph.add_node(node1)
subgraph.add_node(node2)
subgraph.link_nodes(node1, 0, node2, 0)

json_str = subgraph.to_json()
restored_subgraph = Subgraph.from_json(json_str)
```