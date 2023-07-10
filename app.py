import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf
from dash import Dash, dcc, html
from dash import Dash, dash_table
from dash.dependencies import Input, Output, State
from dash.dash_table import DataTable, FormatTemplate
import pandas as pd
import dash_bootstrap_components as dbc
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.layout = html.Div([
            html.H1('DaZ 0.2: A interactive dashboard for data analysis'),
            html.H2('Using this tool we can do the following:'),
            html.H5('1.Filter column.'),
            html.H5('2.Delete an entire column and also rename the column.'),
            html.H5('3.Sort columns in ascending, descending order.'),
            html.H5('4.Delete specific rows.'),
            html.H5('5.Export after cleaning the data.'),
            html.Hr(),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop your excel file or ", html.A("Select Files")]),
            
            style={
                "width": "20%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
    
        html.Div(id="output-data-upload"),
    ]
)
def parse_data(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")),index_col=False)
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),index_col=False)
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return df
@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents"), Input("upload-data", "filename")],
)

def update_table(contents, filename):
    table = html.Div()
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        table = html.Div(
            [
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{"name": i, "id": i,'deletable': True,
                        'renamable': True} for i in df.columns],
                    
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                    export_format="xlsx",
                    style_header={
                        'backgroundColor': 'rgb(40, 30, 30)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(60, 50, 50)',
                        'color': 'white'
                    },
            ),                
                html.Hr(),
                html.Div("Raw Content"),
                html.Pre(
                    contents[0:200] + "...",
                    style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
                ),
            ]
        )
    return table
if __name__ == "__main__":
    app.run_server(debug=False)