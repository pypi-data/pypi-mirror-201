from pprint import pprint

import requests

import wikirate4py

api = wikirate4py.API('ThessaloWikiRate',
                      wikirate_api_url="https://staging.wikirate.org",
                      auth=('wikirate', 'wikirat'))

metric = api.add_metric(designer='US Securities and Exchange Commission',
                        name='This is a Multi-category metric 5',
                        question='What is the company\'s ' + 'Advertising Expense',
                        metric_type='Researched',
                        topics=['Annual Reporting', 'Corporate Accountability', 'Financial'],
                        value_type='Multi-Category',
                        value_options=['UK Registry submission', 'Australian Registry submission', 'No'],
                        research_policy='Community Assessed',
                        report_type='Form 10-K',
                        about='This is the about',
                        methodology='<p>Companies should report their financial performance in their annual financial reports, and these are the best places to find this information.</p><p>For companies that file with the SEC, this information can be found within their \"Form 10-K\" filings. You can often find these documents by searching for \"Company 10-k\", or they can be found through the <a href=\"http://www.sec.gov/edgar/searchedgar/companysearch.html\">SEC\'s EDGAR search</a>.</p>')
print(metric)

# # response = requests.request("post", url="https://staging.wikirate.org/update/Source_000172231",
# #                             auth=('wikirate', 'wikirat'),
# #                             headers={"content-type": "application/pdf",
# #                                      'X-API-Key': "ThessaloWikiRate"},
# #                             files={'card[subcards][+File]': open("TestSource.pdf", 'rb')})
# #
# # print(response.status_code)
