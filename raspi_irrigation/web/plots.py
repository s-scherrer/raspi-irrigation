import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import data

def current_data_figure(window=86400, interval=None, test=False):
    """
    Creates a figure showing current data over time.

    Parameters
    ----------
    window : float
        Time window length before last measurement of which data should be
        shown, in seconds.
    interval: float or None, optional
        Sampling interval of data. If ``None``, the interval of data sampling
        is used, otherwise the data is resampled to the given interval (in
        seconds).
    test : bool, optional
        Whether to only create a test plot using synthetic data. Defaults to
        ``False``.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object containing the plot.
    """
    if test:
        # generate synthetic test data
        if interval is None:
            interval = 3600
        td = datetime.date.today()
        today = datetime.datetime(td.year, td.month, td.day)
        delta = datetime.timedelta(seconds=window)
        index = pd.date_range(start=today, end=today + delta, freq=f"{interval}S")
        t = index.values.astype('datetime64[s]').astype(float)
        t -= t[0]
        n = len(t)
        T = 15 - 5 * np.cos(2*np.pi*t/86400) + 1 * np.random.randn(n)
        rh = 50 + 25 * np.cos(2*np.pi*t/86400) + 5 * np.random.randn(n)
        df = pd.DataFrame(
            {"Temperature in °C": T, "Rel. humidity": rh},
            index=index
        )
    else:
        raise NotImplementedError

    # plot data
    plt.style.use('seaborn')
    fig, axes = plt.subplots(2, 1, sharex=True)
    for i, var in enumerate(df):
        df[var].plot(ax=axes[i], grid=True, legend=True)
        axes[i].set_ylabel(var)
    axes[-1].set_xlabel('Time')
    return fig
