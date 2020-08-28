import datetime
import flask
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from . import plots


def run_webserver():
    """
    Runs the raspberry pi web interface
    """

    app = flask.Flask("raspi-irrigation")

    @app.route("/")
    def index():
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        text = f"Current time: {timestamp}"
        img = (
            '<img src="/figures/current_plot.png" alt="Plot of current data">'
        )
        return img + "<br/>" + text

    @app.route("/figures/current_plot.png")
    def current_plot():
        fig = plots.current_data_figure(test=True)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return flask.Response(output.getvalue(), mimetype="image/png")

    app.run(debug=True, host="0.0.0.0")
