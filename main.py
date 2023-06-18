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
    df['TG'] = df['   TG'].mask(df['   TG'] == -999.9, np.nan)
    temperature = df['TG'].loc[df['    DATE'] == date].squeeze()
    return {"Date": date,
            "Station": station,
            "Temperature": str(temperature)}


@app.route("/api/v1/<station>")
def station_info(station):
    df = pd.read_csv(f'data-small/TG_STAID{str(station).zfill(6)}.txt',
                     parse_dates=['    DATE'],
                     skiprows=20)
    df['   TG'] = df['   TG'] / 10
    df['TG'] = df['   TG'].mask(df['   TG'] == -999.9, np.nan)
    return df.to_dict(orient='records')


@app.route("/api/v1/yearly/<station>/<year>")
def annual(station, year):
    df = pd.read_csv(f'data-small/TG_STAID{str(station).zfill(6)}.txt',
                     parse_dates=['    DATE'],
                     skiprows=20)
    df['   TG'] = df['   TG'] / 10
    df['TG'] = df['   TG'].mask(df['   TG'] == -999.9, np.nan)
    df['    DATE'] = df['    DATE'].astype(str)
    df = df.loc[df['    DATE'].str.startswith(str(year))]
    return df.to_dict(orient='records')


if __name__ == '__main__':
    app.run(debug=True)

# df = df.loc[str(df["    DATE"]).startswith('1860')]
