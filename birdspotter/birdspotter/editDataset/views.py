from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse

# Create your views here.

def index(request):
	#should take the selected dataset and allow the owner to edit it.
	args = {}
	return TemplateResponse(request, 'template.html', args)