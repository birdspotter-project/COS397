from django.shortcuts import render
#from django.http import HttpResponse
import plotly
import plotly.express as px
import plotly.graph_objects as go
import random
import pandas as pd

# Create your views here.
# Data view
def index(request):
    args = {}

    # Total bird count data
    birds = ["Gull", "Razorbill", "Common Eider", "Sandpiper"
             , "Cormorants", "Great Cormorant"]
    data_total = {'Specie': [birds[i] for i in range(len(birds))],
                  'Pop': [round(random.gauss(100, 50)) for _ in range(len(birds))]}
    bird_data_total = pd.DataFrame(data_total)
    #bird_data_total.loc[bird_data_total['Pop'] < 2.0, 'Specie'] = 'Other Birds' # Represents 'other birds' based on relative data size

    # Total bird count graph fig
    fig_bird_total = px.pie(bird_data_total, values='Pop', names='Specie', title='Island Totals')
    args['total_graph'] = plotly.offline.plot(fig_bird_total, auto_open = False, output_type="div")

    # Nesting bird data
    birds = ["Gull", "Razorbill", "Common Eider", "Sandpiper"
             , "Cormorants", "Great Cormorant"]
    data_nesting = {'Specie': [birds[i] for i in range(len(birds))],
                    'Nesting': [round(random.gauss(100, 50)) for _ in range(len(birds))]}
    #bird_nesting_data = pd.DataFrame(data_nesting)

    # Nesting bird count graph fig
    #fig_bird_nesting = px.pie(bird_nesting_data, values='Nesting', names='Specie', title='Specie Behavior')
    long_df = pd.read_csv('https://raw.githubusercontent.com/devinchristianson/COS397/data_view/birdspotter/sample_data.csv')
    fig_bird_nesting = px.bar(long_df, x="Specie", y=["Nesting", "Non-Nesting"], title="Nesting Behavior")

    args['nesting_graph'] = plotly.offline.plot(fig_bird_nesting, auto_open = False, output_type="div")

    # Table Figure
    df_table = pd.read_csv('https://raw.githubusercontent.com/devinchristianson/COS397/data_view/birdspotter/sample_data_table.csv')
    fig_table = go.Figure(data=[go.Table(header=dict(values=['Decade', 'Avg'],
                                                     fill_color='AliceBlue'),
                                         cells=dict(values=[df_table.Decade, df_table.Avg],
                                                    fill_color='Bisque'))
    ])
    args['table'] = plotly.offline.plot(fig_table, auto_open = False, output_type="div")

    # Line Graph Fig
    line_df = pd.read_csv('https://raw.githubusercontent.com/devinchristianson/COS397/data_view/birdspotter/line_sample_data.csv')
    fig_line = px.line(line_df, x="Year", y="Pop", color='Specie')

    args['line_graph'] = plotly.offline.plot(fig_line, auto_open = False, output_type="div")

    return render(request, "dataviz.html", args)
