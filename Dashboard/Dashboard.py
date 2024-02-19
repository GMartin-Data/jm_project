
import dash
from dash import html
from dash import dcc
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
import numpy as np
import folium
import os
from PIL import Image
from elasticsearch import Elasticsearch
# Connexion à Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Construire la requête pour obtenir la taille totale de l'index
total_docs = es.count(index='adzuna_jobs')["count"]

# Construire une nouvelle requête en spécifiant la taille totale
results = es.search(index='adzuna_jobs', body={"query": {"match_all": {}}}, size=total_docs)
pil_image = Image.open("/Dashboard/2018095159_strategie-de-recherche-d-emploi.png")


# Création de la liste des documents
documents = []
for hit in results['hits']['hits']:
    documents.append(hit['_source'])


# dataframe
df = pd.DataFrame(documents)
locations = [{'label': loc, 'value': loc} for loc in df['location']]
titles = [{'label': loc, 'value': loc} for loc in df['title'].unique()]
ids = [{'label': df[df['id']==loc]['title'].iloc[0], 'value': loc} for loc in df['id']]
app = dash.Dash(__name__)



# Fonction pour générer la mise en page de l'application Dash
def generate_layout():
    return html.Div([
         html.Div([
        
        # le titre avec H4 
        html.Img(src=pil_image, style={'width': '1500px', 'height': '600px'}),
        html.Div([
        html.H4("Choisissez le métier"),
        dcc.Dropdown(
            id='title',
            options= titles,
            value= '',
             )],style={
                    'margin-bottom' : '70px',
                    'width':'50%',
                    'border': '2px solid #eee',
                    'border-radius': '10px',
                    'padding': '30px 30px 30px 120px',
                    'box-shadow': '2px 2px 3px #ccc',
                    'display': 'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto'
                 })
              ]),
        
        html.Div([
         dcc.Tabs(id = 'tabs', value = "tab-1", children=[
             # Onglet info générales
             #
             dcc.Tab(label='infos Générales', children=[
                 html.Div([
                     # Onglet info Emploi
                     html.H3("Emploi")
                 ], style={'margin': '30px','background':'rgb(0,139,139)', 'color':'white', 'textAlign':'center','padding':'8px 5px 8px 0px'}),
                 
                 html.Div([
                     # table de données
                     html.Div(id='output')
                     
                 ]),
                 html.Div(id = "map", style={
                     'display':'inline-block','verticalAlign':'top','width':'50%', 
                                            'padding':'15px 0px 15px 10px'
                 }),
             ]),
             # Onglet Compétences
             dcc.Tab(label='Compétences'),
             # Onglet salaire
             dcc.Tab(label='Salaire')
         ])
     ])
        
       
    ])

# Fonction de rappel pour mettre à jour le tableau de données
@app.callback(
    Output('output', 'children'),
    [Input('title', 'value')], 
    
)
def update_data_table(titre_choisie):
    
    df_col_name = df[[ 'contract','company','title','location', "salary_max", "salary_min", "latitude","longitude", "created"]]
    df_cond = df_col_name[df_col_name['title'] == titre_choisie]
    
    to_df = pd.DataFrame(df_cond)
    df_to_dict = to_df.to_dict("records")
    table_elements = []
    
    for i, data in enumerate(df_to_dict):
        
        table = dash_table.DataTable(
            id=f'id = table_infos-{i}',
            columns=[{'id': col, 'name': col} for col in data.keys()],
            data=[data],
            
            style_table={'margin': '20px',
                         },
            style_cell = {'font-family': 'Montserrat'},
            style_data={
                        'color': 'black',
                        'backgroundColor': 'white',
                        'border': '1px solid black',  
                    },
            style_header={ 'border': '1px solid black' ,
                          'backgroundColor': 'rgb(210, 210, 210)'},
    
        )
        
        table_elements.append(table)
    
    
    
    return table_elements

# Définir la mise en page de l'application Dash
app.layout = generate_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
