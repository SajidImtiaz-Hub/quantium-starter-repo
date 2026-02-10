import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load the output from Task 2
df = pd.read_csv("formatted_output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# If you have multiple rows per day+region, sum them
daily = df.groupby(["Date", "Region"], as_index=False)["Sales"].sum()

# Line chart (Date on x, Sales on y)
fig = px.line(
    daily,
    x="Date",
    y="Sales",
    color="Region",
    labels={"Date": "Date", "Sales": "Sales", "Region": "Region"},
    title="Pink Morsel Sales by Date after the Pink Morsel price increase",
)

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Pink Morsel Sales Visualiser"),
        dcc.Graph(id="sales-line-chart", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
