from django.shortcuts import render
from django.http import HttpResponse
import plotly
import plotly.express as px
import plotly.graph_objects as go
import random
import pandas as pd
from birdspotter.dataio.scripts.get_user_datasets import get_dataset_data

# Create your views here.

# Data view
def index(request):
    args = {}

    if request.user.is_authenticated:
        args['isAdmin'] = True
    else:
        args['isAdmin'] = False

    data_table = get_dataset_data(args['isAdmin'])

    bird_data_total = pd.DataFrame({})

    for key in data_table:
        bird_data_total[key] = data_table[key]

 # Nesting bird count graph fig
    grouped = bird_data_total[['species', 'behavior']].copy()
    grouped = grouped.reset_index()

    nesting_data = {}
    nesting_data['nesting'] = grouped[grouped.behavior == 1]
    nesting_data['nesting'] = nesting_data['nesting'].rename(columns={'behavior': 'Nesting'})

    nesting_data['non_nesting'] = grouped[grouped.behavior == 0]
    nesting_data['non_nesting'] = nesting_data['non_nesting'].rename(columns={"behavior": "Non-Nesting"})

    nesting_data['flying'] = grouped[grouped.behavior == 2]
    nesting_data['flying'] = nesting_data['flying'].rename(columns={'behavior': 'Flying'})

    combined = [nesting_data['nesting'], nesting_data['non_nesting'], nesting_data['flying']]
    combined = pd.concat(combined)

    combined['Non-Nesting'] = combined['Non-Nesting'].replace(0, 1)
    combined['Flying'] = combined['Flying'].replace(2, 1)

    combined = combined.groupby(['species']).sum()
    combined = combined.reset_index()
    del combined['index']
    # Total bird count graph fig
    bird_count = bird_data_total['species'].value_counts()

    fig_bird_total = px.pie(combined, values=bird_count, names='species', title='Island Totals')
    args['total_graph'] = plotly.offline.plot(fig_bird_total, auto_open = False, output_type="div")

    # Bar Graph
    fig_bird_nesting = px.bar(combined, x="species", y=['Nesting', 'Non-Nesting', 'Flying'], title="Nesting Behavior")

    args['nesting_graph'] = plotly.offline.plot(fig_bird_nesting, auto_open = False, output_type="div")

    # Table data
    # Table Figure
    fig_table = go.Figure(data=[go.Table(header=dict(values=list(combined.columns)),
                                         cells=dict(values=[combined['species'], combined['Nesting'], combined['Non-Nesting'], combined['Flying']]))])

    args['table'] = plotly.offline.plot(fig_table, auto_open = False, output_type="div")

    # Line Graph Fig

    #args['dist_plot'] = plotly.offline.plot(fig_dist_plot, auto_open = False, output_type="div")

    return render(request, "dataviz.html", args)
