import io
import os
import json

import responder

from word_network import WordNetwork


env = os.environ
DEBUG = env['DEBUG'] in ['1', 'True', 'true']
FORMAT = env['FORMAT']
DPI = int(env['DPI'])

cur_dir = os.path.dirname(__file__)
with open(os.path.join(cur_dir, 'word_network.json')) as fp:
    CONFIG = json.load(fp)


api = responder.API(debug=DEBUG)


@api.route("/")
async def generate(req, resp):
    body = await req.text
    json_body = json.loads(body)

    word_network = WordNetwork(
        node_color=CONFIG.get('node_color'),
        directed=CONFIG.get('directed')
    )
    bytes_io = word_network.generate(
        json_body
    ).draw_graph(
        map_node_edge=True,
        max_node_size=CONFIG['max_node_size'],
        figsize=tuple(CONFIG['figsize']),
        edge_vmin=CONFIG['edge_vmin'],
        width=CONFIG['width'],
        font_family=CONFIG['font_family'],
        font_color=CONFIG['font_color'],
        font_size=CONFIG['font_size'],
        font_weight=CONFIG['font_weight'],
        dpi=DPI,
        format_=FORMAT
    ).bytes_io

    resp.content = bytes_io.getvalue()


if __name__ == "__main__":
    api.run()