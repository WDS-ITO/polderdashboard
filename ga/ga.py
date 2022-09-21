"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import math
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'key.json'
VIEW_ID = '271366520'


def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """Queries the Analytics Reporting API V4.


  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '2022-07-01', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:users'},
                      {'expression': 'ga:avgPageLoadTime'},
                       {'expression': 'ga:bounceRate'}],
          'dimensions': []
        }]
      }
  ).execute()



def get_unique_users(analytics):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '2022-07-01', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:users'}
                      ],
          'dimensions': []
        }]
    }
  ).execute()


  users = ss
  for report in users.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      for value in row.get('metrics', []):
        return value.get('values')[0]

def get_bounce_rate(analytics):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '2022-07-01', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:bounceRate'}
                      ],
          'dimensions': []
        }]
    }
  ).execute()


  rate = ss
  for report in rate.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      for value in row.get('metrics', []):
        return str(round(float(value.get('values')[0]),2))
def get_average_load_time(analytics):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '2022-07-01', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:avgPageLoadTime'}
                      ],
          'dimensions': []
        }]
    }
  ).execute()


  time = ss
  for report in time.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      for value in row.get('metrics', []):
        return value.get('values')[0]

def get_user_source(analytics):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': '2022-07-01', 'endDate': 'today'}],
        'metrics': [{'expression': 'ga:users'}

                    ],
        'dimensions': [{'name':'ga:source'}]
      }]
    }
  ).execute()

  sources = ss

  sources_dict = []

  for report in sources.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      sources_dict.append({'source':row.get('dimensions',[])[0],'amount':row.get('metrics',[])[0].get('values')[0]})

  return sources_dict      


def get_search_data(analytics):
  ss = analytics.reports().batchGet(
  body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '2022-07-01', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:avgsearchDuration'}, #Average Search Duration
                      {'expression': 'ga:avgSearchResultViews'}, #Average amount of times a user clicked on a result
                      {'expression': 'ga:avgSearchDepth'}, #How much subsequent pages were viewed after the search
                      {'expression': 'ga:percentSessionsWithSearch'}, #Percentage of sessions with searches
                      {'expression': 'ga:searchRefinements'} #Did they find what they wanted on their first search

                      ],
          'dimensions': []
        }]
      }
  ).execute()


  search_data = ss

  
  data = search_data['reports'][0]['data']['rows'][0]['metrics'][0]['values']
  search_data_dict = {'Average search Duration': data[0], 'Average search result page Visited': data[1],
                      'Average Search Depth': str(round(float(data[2]),2)), 'Percentage of Sessions with Searches': str(round(float(data[3]),2)),
                      'percentage of new search':str(round(float(data[4]),2)) }



  return search_data_dict
def get_search_terms(analytics):
  ss = analytics.reports().batchGet(
  body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '2022-07-01', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:searchUniques'},


                      ],
          'dimensions': [{'name': 'ga:searchKeyword'}]
        }]
      }
  ).execute()
  sources_dict = []
  search_terms = ss
  for report in search_terms.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      sources_dict.append(
        {'Search_term': row.get('dimensions', [])[0], 'Total_Unique_searches': row.get('metrics', [])[0].get('values')[0]})
  return sources_dict

def get_analytics():
  analytics = initialize_analyticsreporting()
  analytics_dict = {'unique_users':get_unique_users(analytics),
                    'loadtime': get_average_load_time(analytics),
                    'bounce_rate': get_bounce_rate(analytics),
                    'sources':get_user_source(analytics),
                    'search_data':get_search_data(analytics)}

  return analytics_dict

def get_terms():
  analytics = initialize_analyticsreporting()
  terms_dict = {'search_terms': get_search_terms(analytics)}
  
  return terms_dict
  

##getting data based on the date entered by the admin

def get_unique_users_date(analytics,start_date, end_date):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
          'metrics': [{'expression': 'ga:users'}
                      ],
          'dimensions': []
        }]
    }
  ).execute()


  users = ss
  for report in users.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      for value in row.get('metrics', []):
        return value.get('values')[0]

def get_bounce_rate_date(analytics,start_date,end_date):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
          'metrics': [{'expression': 'ga:bounceRate'}
                      ],
          'dimensions': []
        }]
    }
  ).execute()


  rate = ss
  for report in rate.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      for value in row.get('metrics', []):
        return str(round(float(value.get('values')[0]),2))


def get_average_load_time_date(analytics,start_date,end_date):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
          'metrics': [{'expression': 'ga:avgPageLoadTime'}
                      ],
          'dimensions': []
        }]
    }
  ).execute()


  time = ss
  load_time = time['reports'][0]['data']['totals'][0]['values'][0]
  return load_time
def get_user_source_date(analytics,start_date,end_date):
  ss = analytics.reports().batchGet(
  body={
      'reportRequests': [
      {
        'viewId': VIEW_ID,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [{'expression': 'ga:users'}

                    ],
        'dimensions': [{'name':'ga:source'}]
      }]
    }
  ).execute()

  sources = ss

  sources_dict = []

  for report in sources.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      sources_dict.append({'source':row.get('dimensions',[])[0],'amount':row.get('metrics',[])[0].get('values')[0]})

  return sources_dict      
def get_search_data_date(analytics,start_date,end_date):
  ss = analytics.reports().batchGet(
  body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
          'metrics': [{'expression': 'ga:avgsearchDuration'}, #Average Search Duration
                      {'expression': 'ga:avgSearchResultViews'}, #Average amount of times a user clicked on a result
                      {'expression': 'ga:avgSearchDepth'}, #How much subsequent pages were viewed after the search
                      {'expression': 'ga:percentSessionsWithSearch'}, #Percentage of sessions with searches
                      {'expression': 'ga:searchRefinements'} #Did they find what they wanted on their first search

                      ],
          'dimensions': []
        }]
      }
  ).execute()


  search_data = ss

  if  search_data['reports'][0]['data']['totals'][0]['values'][0]=='0.0':
    data = search_data['reports'][0]['data']['totals'][0]['values']
  else:
    data = search_data['reports'][0]['data']['rows'][0]['metrics'][0]['values']
  search_data_dict = {'Average search Duration': str(round(float(data[0]),2)), 'Average search result page Visited': data[1],
                        'Average Search Depth': str(round(float(data[2]),2)), 'Percentage of Sessions with Searches': str(round(float(data[3]),2)),
                        'percentage of new search':str(round(float(data[4]),2)) }



  return search_data_dict
def get_search_terms_date(analytics,start_date,end_date):
  ss = analytics.reports().batchGet(
  body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
          'metrics': [{'expression': 'ga:searchUniques'},


                      ],
          'dimensions': [{'name': 'ga:searchKeyword'}]
        }]
      }
  ).execute()
  sources_dict = []
  search_terms = ss
  for report in search_terms.get('reports', []):
    for row in report.get('data', {}).get('rows', []):
      sources_dict.append(
        {'Search_term': row.get('dimensions', [])[0], 'Total_Unique_searches': row.get('metrics', [])[0].get('values')[0]})
  return sources_dict
def get_analytics_date(start_date,end_date):
  analytics = initialize_analyticsreporting()
  analytics_dict = {'unique_users':get_unique_users_date(analytics,start_date,end_date),
                    'bounce_rate': get_bounce_rate_date(analytics,start_date,end_date),
                    'load_time': get_average_load_time_date(analytics,start_date,end_date),
                    'sources': get_user_source_date(analytics,start_date,end_date),
                    'search_data':get_search_data_date(analytics,start_date,end_date),
                    'search_terms': get_search_terms_date(analytics,start_date,end_date)}

  return analytics_dict
