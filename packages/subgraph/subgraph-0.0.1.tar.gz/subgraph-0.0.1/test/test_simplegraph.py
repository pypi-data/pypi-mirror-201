import unittest

from subgraph.simplegraph import Subgraph, Subnode, SubgraphNode

class TestSubgraphLibrary(unittest.TestCase):
    def test_create_subgraph(self):
        subgraph = Subgraph()
        self.assertIsNotNone(subgraph)

    def test_add_remove_node(self):
        subgraph = Subgraph()
        node = Subnode("simple")
        subgraph.add_node(node)
        self.assertIn(node.node_id, subgraph.nodes)
        subgraph.remove_node(node)
        self.assertNotIn(node.node_id, subgraph.nodes)

    def test_remove_node_by_id(self):
        subgraph = Subgraph()
        node = Subnode("simple")
        subgraph.add_node(node)
        subgraph.remove_node_by_id(node.node_id)
        self.assertNotIn(node.node_id, subgraph.nodes)

    def test_link_unlink_nodes(self):
        subgraph = Subgraph()
        node1 = Subnode("simple1", num_outputs=1)
        node2 = Subnode("simple2", num_inputs=1)
        subgraph.add_node(node1)
        subgraph.add_node(node2)

        subgraph.link_nodes(node1, 0, node2, 0)
        self.assertIn(node2, node1.outputs)
        self.assertIn(node1, node2.inputs)

        subgraph.unlink_nodes(node1, 0, node2, 0)
        self.assertNotIn(node2, node1.outputs)
        self.assertNotIn(node1, node2.inputs)

    def test_custom_node_type(self):
        subgraph = Subgraph()
        custom_node = SubgraphNode(num_inputs=1, num_outputs=1)
        subgraph.add_node(custom_node)
        self.assertIn(custom_node.node_id, subgraph.nodes)

    def test_serialization_deserialization(self):
        subgraph = Subgraph()
        node1 = Subnode("simple1", num_outputs=1)
        node2 = Subnode("simple2", num_inputs=1)
        subgraph.add_node(node1)
        subgraph.add_node(node2)
        subgraph.link_nodes(node1, 0, node2, 0)

        json_str = subgraph.to_json()
        restored_subgraph = Subgraph.from_json(json_str)

        self.assertEqual(len(subgraph.nodes), len(restored_subgraph.nodes))
        for node_id in subgraph.nodes:
            self.assertIn(node_id, restored_subgraph.nodes)

        restored_node1 = restored_subgraph.nodes[node1.node_id]
        restored_node2 = restored_subgraph.nodes[node2.node_id]
        self.assertIn(restored_node2, restored_node1.outputs)
        self.assertIn(restored_node1, restored_node2.inputs)

if __name__ == "main":
    unittest.main()