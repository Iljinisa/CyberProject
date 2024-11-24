from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def homePageView(request):
    template = loader.get_template('pages/index.html')
    return HttpResponse(template.render())
