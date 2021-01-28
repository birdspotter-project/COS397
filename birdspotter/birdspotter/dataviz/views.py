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
	birds = ["Gull", "Razorbill", "Common Eider", "Sandpiper"
			, "Cormorants", "Great Cormorant"]
	data = {'Specie': [birds[i] for i in range(len(birds))],
			'Pop': [round(random.gauss(100, 50)) for _ in range(len(birds))]}
	df = pd.DataFrame(data)
	#df.loc[df['Pop'] < 2.0, 'Specie'] = 'Other Birds' # Represent only large countries
	fig = px.pie(df, values='Pop', names='Specie', title='Island Totals')
	args['graph_div'] = plotly.offline.plot(fig, auto_open = False, output_type="div")
	return render(request, "dataviz.html", args)
