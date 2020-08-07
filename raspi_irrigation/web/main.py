import flask
import datetime

def run_webserver():
    """
    Runs the raspberry pi web interface
    """

    app = flask.Flask("raspi-irrigation")

    @app.route('/')
    def index():
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        return f"Hello. The current time is {timestamp}"

    app.run(debug=True, host='0.0.0.0')
