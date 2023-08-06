from models.shared.shared_pb2 import Graph
from core.sdk.resource_map import grpc_type_map
import core.sdk.helper as Helper

class GraphHelper:
    '''
    Provides functions to handle graph data
    '''
    
    
    def filter_by_resource(graph: Graph, resource):
        filtered_resource = []

        for root_node in graph.root_nodes:
            mapped = grpc_type_map.get(root_node.node.resource.data.type_url)
            if mapped == resource:
                # parse and add to the list
                filtered_resource.append(Helper.unpack_grpc_resource(root_node.node.resource.data, mapped))

        return filtered_resource
