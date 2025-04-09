import dash
from dash import html, dcc, Output, Input
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import pandas as pd

# Beispiel-Daten
data = pd.DataFrame([
    {"name": "Rückhaltebecken Neusäß", "lat": 48.388, "lon": 10.808, "kategorie": "Technischer Hochwasserschutz", "beschreibung": "Modernes Rückhaltebecken entlang des Kobelgrabens."},
    {"name": "Auwald Siebentisch", "lat": 48.340, "lon": 10.930, "kategorie": "Natürlicher Wasserrückhalt", "beschreibung": "Der Auwald speichert bei Starkregen große Mengen Wasser."},
    {"name": "Gründach am Rathausplatz", "lat": 48.366, "lon": 10.898, "kategorie": "Stadtplanung & Versickerung", "beschreibung": "Begrünte Dächer zur Entlastung der Kanalisation."},
    {"name": "Projekt 'Flurretter'", "lat": 48.351, "lon": 10.881, "kategorie": "Landwirtschaftliche Maßnahmen", "beschreibung": "Erosionsschutz durch Hecken und Mulchsaat."},
    {"name": "Schulprojekt Lechforscher", "lat": 48.374, "lon": 10.910, "kategorie": "Bildung & Beteiligung", "beschreibung": "Schüler untersuchen Hochwasserfolgen am Lech."},
])

farben = {
    "Technischer Hochwasserschutz": "blue",
    "Natürlicher Wasserrückhalt": "green",
    "Stadtplanung & Versickerung": "orange",
    "Landwirtschaftliche Maßnahmen": "brown",
    "Bildung & Beteiligung": "purple"
}

kategorien = data["kategorie"].unique()

def generate_markers(selected_categories):
    markers = []
    for _, row in data.iterrows():
        if row["kategorie"] in selected_categories:
            marker = dl.Marker(
                position=[row["lat"], row["lon"]],
                children=[
                    dl.Tooltip(row["name"]),
                    dl.Popup([
                        html.B(row["name"]),
                        html.Br(),
                        row["beschreibung"]
                    ])
                ],
                icon=dl.Icon(color=farben.get(row["kategorie"], "gray"), icon="info-sign")
            )
            markers.append(marker)
    return markers

# Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H2("Nachhaltiger Hochwasserschutz in der Region Augsburg", className="my-3"),
    dbc.Row([
        dbc.Col([
            html.Label("Kategorien auswählen:"),
            dcc.Checklist(
                id="kategorien-checklist",
                options=[{"label": k, "value": k} for k in kategorien],
                value=list(kategorien),
                inputStyle={"margin-right": "10px", "margin-left": "5px"}
            )
        ], width=3),
        dbc.Col([
            dl.Map(
                id="map",
                center=[48.37, 10.90],
                zoom=11,
                children=[
                    dl.TileLayer(),
                    dl.LayerGroup(id="marker-layer")
                ],
                style={'width': '100%', 'height': '600px'}
            )
        ], width=9)
    ])
], fluid=True)

@app.callback(
    Output("marker-layer", "children"),
    Input("kategorien-checklist", "value")
)
def update_markers(selected_categories):
    return generate_markers(selected_categories)

if __name__ == "__main__":
    app.run_server(debug=True)
