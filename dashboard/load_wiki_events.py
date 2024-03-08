import pandas as pd
from datetime import datetime
from copy import deepcopy
import requests
import re


class WikiPageRevisions:
        
    #df = pd.DataFrame(revision_list)
    query_url = "https://{0}".format('en.wikipedia.org/w/api.php')

    def __init__(self, tags, start, plus_month_period, titles, link):
        self.tags = tags
        self.start = datetime.strftime(
            pd.to_datetime(start), '%Y-%m-%dT%H:%M:%SZ')
        self.stop = datetime.strftime(
            pd.to_datetime(start) + pd.DateOffset(months=plus_month_period), '%Y-%m-%dT%H:%M:%SZ')
        self.titles_multiple_pages = titles
        self.page_link = link
        self.query_params = {}
        self.query_url = WikiPageRevisions.query_url
        self.query_params['action'] = 'query'
        self.query_params['prop'] = 'revisions'
        self.query_params['rvprop'] = 'timestamp|content'
        self.query_params['rvlimit'] = 5
        self.query_params['rvdir'] = 'newer'
        self.query_params['format'] = 'json'
        self.query_params['redirects'] = 1
        self.query_params['formatversion'] = 2
        self.query_params['titles'] = titles.split(',')[0]
        self.query_params['rvstart'] = self.start
        self.query_params['rvend'] = self.stop

    def tags_list(self):
        tags_list = self.tags.split(',')
        tags_list = [tag.strip() for tag in tags_list]
        return tags_list
    
    def titles_list(self):
        titles_list = self.titles_multiple_pages.split(',')
        titles_list = [title.strip() for title in titles_list]
        return titles_list
    
    def get_revisions(self, json_response):

        if not 'error' in json_response and len(json_response)> 0 and type(json_response['query']['pages']) == list:
            if 'revisions' in json_response['query']['pages'][0]:
                return json_response['query']['pages'][0]['revisions']
            else:
                return list()
        elif 'error' in json_response:
            raise Exception(json_response['error'])
        else:
            raise ValueError("There are no revisions in the JSON")

    def tags_found(self, content):
        for tag in self.tags:
            if not re.search(tag, content, re.IGNORECASE):
                return False
        return True

    def get_filtered_revisions(self, revision_list):
        for revision in revision_list:
            if 'content' in revision:
                found = self.tags_found(revision['content'])
                if not found:
                    revision_list.remove(revision)
            else:
                revision_list.remove(revision)
        return revision_list

    def get_wiki_revisions_frame(self):


        revision_list = list()
        df = pd.DataFrame(revision_list)

        # Make the query perovskite, efficiency
        titles = self.titles_list()
        for title in titles:
            self.query_params['titles'] = title
            json_response = requests.get(url=self.query_url, params=self.query_params).json()
            revision_list += self.get_revisions(json_response)
            if len(revision_list) == 0:
                # return df
                continue
            revision_list = self.get_filtered_revisions(revision_list)
            # Loop for the rest of the revisions
            while True:

                # Newer versions of the API return paginated results this way
                if 'continue' in json_response:
                    query_continue_params = deepcopy(self.query_params)
                    query_continue_params['rvcontinue'] = json_response['continue']['rvcontinue']
                    json_response = requests.get(
                        url=self.query_url, params=query_continue_params).json()
                    revision_list += self.get_revisions(json_response)
                    revision_list = self.get_filtered_revisions(revision_list)
                # If there are no more revisions, stop
                else:
                    break

        df = pd.DataFrame(revision_list)


        df['timestamp'] = pd.to_datetime(df['timestamp'])
        monthly_counts = df.groupby(df['timestamp'].dt.to_period('M')).size().reset_index()
        monthly_counts.rename(columns={0: 'revisions_count'}, inplace=True)
        monthly_counts['date'] = monthly_counts['timestamp'].dt.strftime(
            '%Y-%m-%d')
        subset_desired_columns = monthly_counts.loc[:, ['date',  'revisions_count']]
        return subset_desired_columns


# tags1 = 'research, perovskite, efficiency'
# tags2 = 'solar energy, milestone'
# tags = 'solar energy, policy, cost'
# start = 'April 14, 2009'
# plus_month_period = 6
# page_title = 'Perovskite solar cell,Solar cell,Semicondactor'
# link = 'https://pubs.acs.org/doi/10.1021/ja809598r'
# wikiPageRevisions = WikiPageRevisions(tags, start, plus_month_period, page_title, link)
# df = wikiPageRevisions.get_wiki_revisions_frame()
# # Set index=False to exclude row numbers
# print(df)
# #df.to_csv('perovskite_solar_cell.csv', index=False)

