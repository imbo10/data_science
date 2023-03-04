# app.py

import pandas as pd
import base64
from dash import Dash, dcc, html, Input, Output


data = (
    pd.read_csv("avocado.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

regions = data["region"].sort_values().unique()
avocado_types = data["type"].sort_values().unique()

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

image_filename = './assets/favicon.ico' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

### A
app.layout = html.Div(
    children = [
        ### B
        html.Div(
            children = [
               ### html.Img(
                 ###   src = "data:image/ico;base64,{}".format(encoded_image.decode()),
                 ###  className = "header-emoji",
                ###),
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children = "Avocado Analytics",
                    className = " header-title",
                ),
                html.P(
                    children = (
                        "Analyze the behavior of avocado prices and the number"
                        "of avocados sold in the US between 2015 and 2018"
                    ),
                    className = "header-description",
                ),
            ],
            className = "header",
        ), ### End Div B

        ### Div C
        html.Div(
            children = [
                html.Div(
                    children = [
                        html.Div(children = "Region", className="menu-title"),
                        dcc.Dropdown(
                            id = "region-filter",
                            options = [
                                {"label": region, "value": region}
                                for region in regions
                            ],
                            value = "Albany",
                            clearable = False,
                            className = "dropdown"
                        ),
                    ],
                ),
                html.Div(
                    children = [
                        html.Div(children = "Type", className="menu-title"),
                        dcc.Dropdown(
                            id = "type-filter",
                            options = [
                                {"label": avocado_type.title(), "value": avocado_type}
                                for avocado_type in avocado_types
                            ],
                            value = "organic",
                            clearable = False,
                            className = "dropdown"
                        ),
                    ],
                ),
                html.Div(
                    children = [
                        html.Div(children = "Date Range", className = "menu-title"),
                        dcc.DatePickerRange(
                            id = "date-range",
                            min_date_allowed = data["Date"].min().date(),
                            max_date_allowed = data["Date"].max().date(),
                            start_date = data["Date"].min().date(),
                            end_date = data["Date"].max().date(),
                        ),
                    ],
                ),
            ],
            className = "menu"
        ), ### End Div C

        ### Div D
        html.Div(
            children = [

                ### Div E
                html.Div(
                    children = dcc.Graph(
                        id = "price-chart",
                        config = {"displayModeBar": False},
                        
                    ),
                    className = "card",
                ), ### End Div E

                ### Div F
                html.Div(
                    children = dcc.Graph(
                        id = "volume-chart",
                        config = {"displayModeBar": False},
                        
                    ),
                    className = "card",
                ), ### End Div F
            ],
            className = "wrapper",
        ), ### End Div D
    ]
) ### End Div A

@app.callback(
    Output("price-chart", "figure"),
    Output("volume-chart", "figure"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)

def update_charts(region, avocado_type, start_date, end_date):
    filtered_data = data.query(
        "region == @region and type == @avocado_type"
        " and Date >= @start_date and Date <= @end_date"
    )

    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "types": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>"
            },
        ],
        "layout": {
            "title": {"text": "Average Price of Avocado", "x": 0.05, "xanchor": "left",},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True, "tickprefix": "$"},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)