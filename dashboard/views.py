
from django.shortcuts import render
import pandas as pd
from dashboard.forms import DateForm
from dashboard.models import Event, WikiRevisionEvent
import plotly.graph_objects as go
from colorhash import ColorHash

def chart(request):
    events = Event.objects.all()
    start = request.GET.get('start')
    end = request.GET.get('stop')
       
    if start:
        events = events.filter(date__gte=start)
    if end:
        events = events.filter(date__lte=end)

    wikievents = WikiRevisionEvent.objects.all()
    if start:
        wikievents = wikievents.filter(date__gte=start)
    if end:
        wikievents = wikievents.filter(date__lte=end)

    fig = go.Figure() 
    data=go.Scatter(
        x=[event.date for event in events],
        y=[event.revisions_count for event in events],
        mode='lines+markers',
        showlegend=True,
        text=[event.tags for event in events],
        marker=dict(size=10,
                    color=[ColorHash(event.tags).hex for event in events])                    
    )

    wiki_data = go.Scatter(
        x=[wikievent.event_date for wikievent in wikievents],
        y=[wikievent.revisions_count+5 for wikievent in wikievents],
        mode='lines+markers',
        showlegend=True,
        text=[wikievent.event_tags for wikievent in wikievents],
        marker=dict(size=10,
                    color=[ColorHash(wikievent.event_tags).hex for wikievent in wikievents])
    )

    fig.add_trace(data)
    fig.add_trace(wiki_data)
    if not start:
        start = events.first().date
    if not end:
        end = events.last().date + pd.DateOffset(months=6)
    fig.update_layout(
        xaxis_range=[start, end], title_text='Developments in solar technology')
    fig.update_xaxes(
        dtick="M6",
        tickformat="%b\n%Y",
        ticklabelmode="period"
        )
    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'dashboard/chart.html', context)
