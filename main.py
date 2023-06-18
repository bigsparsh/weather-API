from flask import Flask, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
stations = pd.read_csv('data-small/stations.txt',
                       skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]


@app.route("/")
def home():
    return render_template('index.html', data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def find(station, date):
    df = pd.read_csv(f'data-small/TG_STAID{str(station).zfill(6)}.txt',
                     parse_dates=['    DATE'],
                     skiprows=20)
    df['   TG'] = df['   TG'] / 10
    df['TG'] = df['   TG'].mask(df['   TG'] == -9999, np.nan)
    temperature = df['TG'].loc[df['    DATE'] == date].squeeze()
    return {"Date": date,
            "Station": station,
            "Temperature": str(temperature)}


if __name__ == '__main__':
    app.run(debug=True)
