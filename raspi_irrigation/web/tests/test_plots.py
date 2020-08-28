from raspi_irrigation.web import plots

def test_synthetic_plot():
    fig = plots.current_data_figure(test=True)
