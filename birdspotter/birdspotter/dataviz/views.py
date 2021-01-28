from django.shortcuts import render
from django.http import HttpResponse
import plotly
import plotly.express as px
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
	bird_nesting_data = pd.DataFrame(data_nesting)
	# Nesting bird count graph fig
	fig_bird_nesting = px.pie(bird_nesting_data, values='Nesting', names='Specie', title='Specie Behavior')

	# Dropdown
	button_layer_1_height = 1.08
	fig_bird_nesting.update_layout(
		updatemenus=[
			dict(
				active=1,
				buttons=list([
					dict(label=birds[0],
						 method="update",
						 args=[{"visible": [True, True, False, False]}])
				]),
			)
		])

	args['nesting_graph'] = plotly.offline.plot(fig_bird_nesting, auto_open = False, output_type="div")
	return render(request, "dataviz.html", args)
