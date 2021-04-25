from django.shortcuts import render, redirect
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from birdspotter.dataio.scripts.get_user_datasets import get_dataset_data
from django.contrib import messages

# Data view
def index(request, uuid):
    args = {}
    
    if request.user.is_authenticated:
        
        data_table, dataset_name, _ = get_dataset_data(request.user.is_authenticated, uuid)
        args['dataset_name'] = dataset_name
        if data_table is None:
            messages.error(request, "The selected dataset does not have an associated shapefile")
            return redirect('/')
        bird_data_total = pd.DataFrame({})
    
        for key in data_table:
            bird_data_total[key] = data_table[key]
    
        # Nesting bird count graph fig
        grouped = bird_data_total[['species', 'behavior']].copy()
        grouped = grouped.reset_index()
    
        # Isolate each behavior by value. i.e. any row w/ behavior 1 = nesting
        nesting_data = {}
        nesting_data['nesting'] = grouped[grouped.behavior == 1]
        nesting_data['nesting'] = nesting_data['nesting'].rename(columns={'behavior': 'Nesting'})
    
        nesting_data['non_nesting'] = grouped[grouped.behavior == 0]
        nesting_data['non_nesting'] = nesting_data['non_nesting'].rename(columns={'behavior': 'Non-Nesting'})
    
        nesting_data['flying'] = grouped[grouped.behavior == 2]
        nesting_data['flying'] = nesting_data['flying'].rename(columns={'behavior': 'Flying'})
    
        # Combine the isolated data
        combined = [nesting_data['nesting'], nesting_data['non_nesting'], nesting_data['flying']]
        combined = pd.concat(combined)
    
        # Change default values to 1
        combined['Non-Nesting'] = combined['Non-Nesting'].replace(0, 1)
        combined['Flying'] = combined['Flying'].replace(2, 1)
    
        combined = combined.groupby(['species']).sum()
        combined = combined.reset_index()
        del combined['index']
        # Total bird count graph fig
        bird_count = bird_data_total['species'].value_counts()
    
        # Species total pie chart
        fig_bird_total = px.pie(combined, values=bird_count, names='species', title='Island Totals')
        args['total_graph'] = plotly.offline.plot(fig_bird_total, auto_open = False, output_type='div')
    
        # Species behavior Bar graph
        fig_bird_nesting = px.bar(combined, x="species", y=['Nesting', 'Non-Nesting', 'Flying'], title='Nesting Behavior')
    
        args['nesting_graph'] = plotly.offline.plot(fig_bird_nesting, auto_open = False, output_type='div')
    
    
        args['table'] = plotly.offline.plot(go.Figure(data=[go.Table(header=dict(values=list(combined.columns)),
                                             cells=dict(values=[combined['species'], combined['Nesting'], combined['Non-Nesting'], 
                                            combined['Flying']]))]), auto_open = False, output_type='div')
    
        # Certainty Table Fig
        fig_certainty = go.Figure(data=[go.Table(header=dict(values=['species', 'certain_p1']),
                                                 cells=dict(values=[bird_data_total.species, bird_data_total.certain_p1]))])
    
        args['certainty_table'] = plotly.offline.plot(fig_certainty, auto_open = False, output_type='div')
    
        return render(request, 'dataviz.html', args)
    
    return redirect('/')
