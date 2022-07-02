import os
import sys

import requests
import dash
from dash import dcc, html
from dash.dependencies import Input, Output  # , State
from app.utils.functions import deal_response

# from dash.exceptions import PreventUpdate


sys.path.append(os.getcwd())

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="Transformer App", id="first"),
        dcc.Interval(id="timer"),
        html.Div(id="dummy"),
        dcc.Graph(
            id="graph",
            figure={
                "data": [
                    {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "1"},
                    {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "2"},
                ],
                "layout": {"title": "Dash Data Visualization"},
            },
        ),
    ]
)


@app.callback(output=Output("graph", "figure"), inputs=[Input("timer", "n_intervals")])
def update_graph(n_clicks=0):

    response = requests.get("http://127.0.0.1:5000/")
    response = response.json()
    title = "Deu Erro!"

    data = deal_response(response["data"])

    if response["status"] == 1:
        data_response: dict = response["data"]
        x = []
        y = []
        n = len(data_response["PerdasT"])

        for i in range(n):
            i = str(i)
            massa = data_response["Mativa"][i]
            perda = data_response["PerdasT"][i]
            x.append(perda)
            y.append(massa)

        title = "Vem da API"

    data = [
        {"x": x, "y": y, "type": "scatter", "name": "SF", "mode": "markers"},
        {"x": x, "y": y, "type": "scatter", "name": "SF2", "mode": "markers"},
    ]

    return {"data": data, "layout": {"title": title}}


if __name__ == "__main__":
    app.run_server(debug=True)
