import argparse
from bson.json_util import dumps
from flask import Flask, request, Response, current_app
from training.model_manager import ModelManager


def parse_arguments():
    parser = argparse.ArgumentParser(description='Starts a server that queries a pretrained model.')
    parser.add_argument('filename', metavar='filename', help='a model config json file')
    return parser.parse_args()


args = parse_arguments()
model = ModelManager.load(args.filename)
server = Flask(__name__)


@server.route('/', methods=['GET'])
def root():
    return current_app.send_static_file('index.html')


@server.route("/ask", methods=['GET'])
def ask():
    post = request.args.get('post', default=None)
    if post:    
        classification = model.predict([post])
        reaction = model.translate_reaction_id(classification[0])
        return Response(response=dumps(reaction), status=200, mimetype='application/json')
    else:
        return Response(response="Query parameter 'post' is missing.", status=400, mimetype='text/plain')


server.run(host='0.0.0.0')
