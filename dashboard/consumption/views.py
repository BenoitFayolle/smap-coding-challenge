# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from .models import user, consumption_point
from plotly.offline import plot
import plotly.graph_objs as go
# Create your views here.


def summary(request):
    data2Plot = user.objects.all()
    user_id = []
    ave_cons = []
    tot_cons = []
    for key in data2Plot:
         user_id.append(key.user_id)
         ave_cons.append(key.mean_consumption)
         tot_cons.append(key.total_consumption)
         
     #generate html for plotly bargraphs
    ave_cons_html=plot(go.Figure(data=[go.Bar(x=user_id,y=ave_cons)], 
                                       layout=go.Layout(margin=go.Margin(l=50,r=50,b=20,t=20,pad=4))),
                        output_type='div')

    tot_cons_html=plot(go.Figure(data=[go.Bar(x=user_id,y=tot_cons,name="total consumption of all users (Wh)")],
                                       layout=go.Layout(margin=go.Margin(l=50,r=50,b=20,t=20,pad=4))),
                        output_type='div')
    
    #add user objects for the table
    context={'ave_cons_html': ave_cons_html,
             'tot_cons_html': tot_cons_html,
             'user_table': user.objects.all()}
    return render(request, 'consumption/summary.html', context)


def detail(request,id_request):
     get_object_or_404(user,pk=id_request)
     data2Plot = consumption_point.objects.filter(user_fk=id_request)
     x_datetime = []
     y_consumption = []
     for key in data2Plot:
         x_datetime.append(key.datetime)
         y_consumption.append(key.consumption)
     html=plot(go.Figure(data=[go.Scatter(x=x_datetime,y=y_consumption)],layout=go.Layout(yaxis=dict(title="Consumption (Wh)"))),
               output_type='div')
     context={'html': html,
              'user': user.objects.all().filter(user_id=id_request)}
     return render(request, 'consumption/detail.html', context)