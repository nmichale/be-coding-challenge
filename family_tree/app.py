import flask
import flask_cors
import connexion

from . import utils
from . import config

ui_bp = flask.Blueprint('ui', __name__)

@ui_bp.route('/swagger_ui')
@ui_bp.route('/swagger_ui/')
def serve_swagger_ui_index():
    return flask.render_template('swagger_ui.html', api_url=flask.request.url_root + 'swagger_ui.json')


@ui_bp.route('/swagger_ui/<path:filename>')
def serve_swagger_ui_static_files(filename):
    return flask.send_from_directory('static', filename)

@ui_bp.route('/swagger_ui.json')
def serve_swagger_ui_json():
    return utils.yaml_to_json(config.wd + '/' + config.SPEC_FN)

@ui_bp.route('/health_check', methods=['GET'])
def health_check():
    return flask.jsonify(True)

cors = flask_cors.CORS()

def create_app():
    app = connexion.FlaskApp(__name__)
    app.app.config['JSON_SORT_KEYS'] = False
    app.app.register_blueprint(ui_bp)
    app.add_api('api.yaml')
    cors.init_app(app.app)
    app.app.register_blueprint(ui_bp)

    return app

