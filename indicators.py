def detect_crossover(df, short_ma=11, long_ma=23):
    df['short_ma'] = df['close'].rolling(short_ma).mean()
    df['long_ma'] = df['close'].rolling(long_ma).mean()
    if df['short_ma'].iloc[-2] < df['long_ma'].iloc[-2] and df['short_ma'].iloc[-1] > df['long_ma'].iloc[-1]:
        return 'bullish'
    elif df['short_ma'].iloc[-2] > df['long_ma'].iloc[-2] and df['short_ma'].iloc[-1] < df['long_ma'].iloc[-1]:
        return 'bearish'
    return None
