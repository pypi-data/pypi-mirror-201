import json
import uuid

class Subnode:
    def __init__(self, node_type, num_inputs=0, num_outputs=0, node_id=None):
        self.node_type = node_type
        self.node_id = node_id
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.inputs = [None] * num_inputs
        self.outputs = [None] * num_outputs
        self.subgraph = None

    def __repr__(self):
        return f"Subnode(node_id={self.node_id}, node_type={self.node_type}, num_inputs={self.num_inputs}, num_outputs={self.num_outputs})"

    def connect_input(self, index, node):
        if 0 <= index < self.num_inputs:
            self.inputs[index] = node

    def connect_output(self, index, node):
        if 0 <= index < self.num_outputs:
            self.outputs[index] = node

    def get_input_nodes(self):
        return [input_node for input_node in self.inputs if input_node is not None]

    def get_output_nodes(self):
        return [output_node for output_node in self.outputs if output_node is not None]

    def serialize(self):
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "num_inputs": self.num_inputs,
            "num_outputs": self.num_outputs,
            "inputs": [node.node_id if node else None for node in self.inputs],
            "outputs": [node.node_id if node else None for node in self.outputs],
        }

    @classmethod
    def deserialize(cls, data):
        node = cls(data["node_type"], data["num_inputs"], data["num_outputs"], data["node_id"])
        return node

_registered_node_types = {}

def register_node_type(node_type, node_class):
    _registered_node_types[node_type] = node_class

class SubgraphNode(Subnode):
    def __init__(self, num_inputs=0, num_outputs=0, subgraph=None, node_id=None):
        super().__init__("subgraph", num_inputs=num_inputs, num_outputs=num_outputs, node_id=node_id)
        self.nested_subgraph = subgraph if subgraph else Subgraph()

    def serialize(self):
        data = super().serialize()
        data["subgraph"] = self.nested_subgraph.to_json()
        return data

    @classmethod
    def deserialize(cls, data):
        subgraph = Subgraph.from_json(data["subgraph"])
        node = cls(data["node_id"], data["num_inputs"], data["num_outputs"], subgraph)
        return node

register_node_type("subgraph", SubgraphNode)

class Subgraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node.subgraph is not None:
            if node.subgraph == self:
                raise ValueError(f"Node {node} is already in this subgraph")
            node.subgraph.remove_node(node)

        if node.node_id is None:
            node.node_id = str(uuid.uuid4())

        if node.node_id in self.nodes:
            raise ValueError(f"Node with ID {node} already exists in the subgraph")

        self.nodes[node.node_id] = node
        node.subgraph = self

    def remove_node(self, node):
        # make sure the node is in this subgraph (otherwise raise an exception)
        if node.subgraph != self or node.node_id not in self.nodes:
            raise ValueError(f"Tried to remove node {node} which is not in this subgraph")
        for input_idx, input_node in enumerate(node.get_input_nodes()):
            self.unlink_nodes(input_node, input_node.outputs.index(node), node, input_idx)
        for output_idx, output_node in enumerate(node.get_output_nodes()):
            self.unlink_nodes(node, output_idx, output_node, output_node.inputs.index(node))
        del self.nodes[node.node_id]
        node.subgraph = None
        node.node_id = None
    
    def remove_node_by_id(self, node_id):
        if node_id in self.nodes:
            node = self.nodes[node_id]
            self.remove_node(node)
    
    def link_nodes(self, node1, output_idx, node2, input_idx):
        if node1.node_id in self.nodes and node2.node_id in self.nodes:
            node1.connect_output(output_idx, node2)
            node2.connect_input(input_idx, node1)

    def unlink_nodes(self, node1, output_idx, node2, input_idx):
        if node1.node_id in self.nodes and node2.node_id in self.nodes:
            node1.connect_output(output_idx, None)
            node2.connect_input(input_idx, None)

    def to_json(self):
        nodes_list = [node.serialize() for node in self.nodes.values()]
        return json.dumps({"nodes": nodes_list})

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        subgraph = cls()
        node_id_to_node = {}
        for node_data in data["nodes"]:
            node_type = _registered_node_types.get(node_data["node_type"], Subnode)
            node = node_type.deserialize(node_data)
            subgraph.add_node(node)
            node_id_to_node[node.node_id] = node

        for node_data in data["nodes"]:
            node = node_id_to_node[node_data["node_id"]]
            for input_idx, input_node_id in enumerate(node_data["inputs"]):
                if input_node_id is not None:
                    input_node = node_id_to_node[input_node_id]
                    node.connect_input(input_idx, input_node)

            for output_idx, output_node_id in enumerate(node_data["outputs"]):
                if output_node_id is not None:
                    output_node = node_id_to_node[output_node_id]
                    node.connect_output(output_idx, output_node)

        return subgraph