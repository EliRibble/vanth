import flask

blueprint = flask.Blueprint('index', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html', path='/')
