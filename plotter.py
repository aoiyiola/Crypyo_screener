import mplfinance as mpf
import pandas as pd
from io import BytesIO

def plot_chart(df, symbol, short_ma, long_ma):
    """
    Plots a candlestick chart with moving averages for the given symbol.
    Returns a BytesIO buffer containing the PNG image.
    """
    df = df.copy().tail(100)
    # Ensure timestamp is datetime and set as index
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')

    # Prepare moving averages for mplfinance
    mav = (short_ma, long_ma)

    # Custom style with larger fonts and minimal padding
    my_style = mpf.make_mpf_style(
        base_mpf_style='charles',
        rc={
            'font.size': 16,
            'axes.labelsize': 12,
            'axes.titlesize': 14,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'figure.titlesize': 16,
            'font.family': 'calibri',
        },
        gridstyle='-',
        y_on_right=False,
        figcolor='white',
        facecolor='white',
        edgecolor='black',
    )

    buf = BytesIO()
    mpf.plot(
        df,
        type='candle',
        style=my_style,
        title=f"{symbol} 1H",
        mav=mav,
        ylabel='',
        volume=False,
        savefig=dict(fname=buf, format='png', bbox_inches='tight', pad_inches=0.1)
    )
    buf.seek(0)
    return buf