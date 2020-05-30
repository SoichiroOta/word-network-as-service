import io
import os
import json

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


cur_dir = os.path.dirname(__file__)
with open(os.path.join(cur_dir, 'word_network.json')) as fp:
    CONFIG = json.load(fp)
if CONFIG.get('style'):
    plt.style.use(CONFIG['style'])


class WordNetwork:
    def __init__(self, node_color=None, directed=False):
        self.bytes_io = io.BytesIO()
        if directed:
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()
        if node_color:
            self.node_color = node_color
        else:
            self.node_color = '#BC002D'
        

    def generate(self, data):
        nodes = data['node']
        for n in nodes:
            if data.get('node_color'):
                node_color = data['node_color']
            elif n.get('color'):
                node_color = n['color']
            else:
                node_color = self.node_color
            self.G.add_node(
                n['word'],
                weight=n['weight'],
                color=node_color)
        edges = data['edge']
        for edge in edges:
            words = edge['word']
            self.G.add_edge(
                words[0],
                words[1],
                weight=edge['weight'])
        return self

    def draw_graph(
        self,
        node_color=None,
        map_node_edge=True,
        max_node_size=1.0,
        figsize=(1, 1),
        edge_vmin=0.0,
        width=1.0,
        font_family='Source Han Sans',
        font_color='black',
        font_size=2,
        font_weight='bold',
        dpi=300,
        format_='PNG',
        **kwargs
    ):
        pos = nx.spring_layout(self.G)
        if map_node_edge:
            node_weights = np.array(
                [d['weight'] for k, d in self.G.nodes(data=True)]
            )
            kwargs['node_size'] = (max_node_size / np.max(
                node_weights
            )) * node_weights 
            kwargs['edge_color'] = [d['weight'] for u, v, d in self.G.edges(
                data=True
            )]
            kwargs['node_color'] = [d['color'] for k, d in self.G.nodes(
                data=True
            )]

        fig = plt.figure(figsize=figsize)
        nx.draw(self.G,
            pos=pos,
            edge_cmap=plt.cm.Greys,
            edge_vmin=edge_vmin,
            width=width,
            with_labels=True,
            font_family=font_family,
            font_color=font_color,
            font_size=font_size,
            font_weight=font_weight,
            **kwargs)
        plt.savefig(
            self.bytes_io,
            dpi=dpi,
            format=format_
        )
        plt.close(fig)
        return self