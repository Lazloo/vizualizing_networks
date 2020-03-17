import flask
from flask_cors import CORS
from flask import request, jsonify, render_template
from NetworkPackage import network_operations
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc

# Flask Initialization
app = flask.Flask(__name__)
# Cors are important for cross application (during java programming)
CORS(app)
app.config["DEBUG"] = True

obj = network_operations.NetworkClass()
obj.load_network(file_name='data/subgraph.graphml')


# nx.write_graphml(obj.graph, 'data/hero_normed.graphml')
@app.route('/get_data', methods=['GET'])
def get_network():
    weights = nx.get_edge_attributes(obj.graph, 'weight')
    df_edges = pd.DataFrame()
    df_edges['edge_name'] = weights.keys()
    df_edges['weight'] = weights.values()
    edges_to_remove = df_edges.loc[df_edges['weight'] <= 20, 'edge_name'].values
    obj.graph.remove_edges_from(edges_to_remove)

    # degrees = obj.graph.degree(weight='weight')
    # df = pd.DataFrame.from_dict(degrees)
    # subgraph = obj.graph.subgraph(df.loc[df[1] > 1000, 0].values)

    df_size = pd.DataFrame()
    sizes = nx.get_node_attributes(obj.graph, 'size')
    df_size['node_name'] = sizes.keys()
    df_size['size'] = sizes.values()
    subgraph = obj.graph.subgraph(df_size.loc[df_size['size'] > 20, 'node_name'].values)

    print(len(subgraph.nodes))
    print(len(subgraph.edges))
    nx.write_graphml(subgraph, 'data/test.graphml')
    return jsonify(str().join(nx.readwrite.graphml.generate_graphml(subgraph, encoding='utf-8', prettyprint=True)))


# rgb = {i: (r[i], g[i], b[i]) for i, j in r.items()}
app.run(port=10004)

# df_edges = pd.DataFrame()
# df_edges['edge_name'] = weights.keys()
# df_edges['weight'] = weights.values()
# edges_to_remove = df_edges.loc[df_edges['weight'] <= 20, 'edge_name'].values
# obj.graph.remove_edges_from(edges_to_remove)
# df_edges = pd.Series(weights).to_frame()
# sum(df_edges[0] > 1000)

#
# degrees = obj.graph.degree(weight='weight')
#
#
# subgraph = obj.graph.subgraph(df.loc[df[1]>10, 0].values)
# nx.write_graphml(subgraph, 'data/subgraph.graphml')
#
# df = pd.DataFrame.from_dict(degrees)
#
# hist = df.hist(column=1, bins=1000)
# plt.xlim(0,25)
# # plt.yticks([0,10,100,1000,2000,3])
# plt.show()
# app.run(port=10004)

# # obj.graph.
# labels = nx.get_node_attributes(obj.graph, 'label')
# labels_id = {j: i for i,j in labels.items()}
# id_spider = labels_id['SPIDER-MAN/PETER PAR']
# id_hulk = labels_id['HULK/DR. ROBERT BRUC']
# id_iron = labels_id['IRON MAN/TONY STARK']
#
#
#
# degrees = obj.graph.degree(weight='weight')
# print('Spiderman: ' + str(degrees[id_spider]))
# print('Hulk: ' + str(degrees[id_hulk]))
# print('Ironman: ' + str(degrees[id_iron]))
#
#
# try:
#     nx.get_edge_attributes(obj.graph, 'weight')[id_spider, id_hulk]
# except Exception:
#     print('No Link found')
#
#
# try:
#     print('Ironman vs Hulk: ' + str(nx.get_edge_attributes(obj.graph, 'weight')[id_iron, id_hulk]))
# except Exception:
#     print('No Link found')
