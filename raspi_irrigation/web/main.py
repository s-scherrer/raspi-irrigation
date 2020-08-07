import flask


def run_webserver():
    """
    Runs the raspberry pi web interface
    """

    app = flask.Flask("raspi-irrigation")

    @app.route('/')
    def index():
        return "Hello"

    app.run(debug=True, host='0.0.0.0')
