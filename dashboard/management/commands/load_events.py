
import csv
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd
from dashboard.load_wiki_events import WikiPageRevisions
from dashboard.models import Event, WikiRevisionEvent

class Command(BaseCommand):
    help = 'Load events data from events_data.csv file'

    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'events_data.csv'
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                formatted_date = datetime.strftime(
                    pd.to_datetime(row['Event date']), '%Y-%m-%d')
                event = Event.objects.get_or_create(date=formatted_date, name=row['Event name'], description=row['Event description'],
                                                    tags=row['Tags'], link=row['Link to additional info'], revisions_count=1)
                tags = row['Tags']
                start = row['Event date']
                page_title = 'Perovskite solar cell, Solar cell, Semiconductor'
                link = 'https://en.wikipedia.org/wiki/Perovskite_solar_cell'
                plus_month_period = 6
                wikiPageRevisions = WikiPageRevisions(
                    tags, start, plus_month_period, page_title, link)
                df = wikiPageRevisions.get_wiki_revisions_frame()
                for _, row in df.iterrows():
                    formatted_date = row['date']
                    revisions_count = row['revisions_count']                    
                    wikievent = WikiRevisionEvent.objects.get_or_create(event_date=formatted_date,
                                                                        page_description=page_title,
                                                                        event_tags=tags, page_url=link, revisions_count=revisions_count)
