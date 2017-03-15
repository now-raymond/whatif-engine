# ************************************************************************
# ANALYSE DATA BASED ON REDDIT HEADLINES USING CORTONA TEXT ANALYSIS API
# EXTRACT KEYPHRASES AND SENTIMENT VALUES
# ************************************************************************
import urllib2
import urllib
import sys
import base64
import json
import csv
import unicodedata
from unidecode import unidecode
from curve_fit import get_training_data

# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
account_key = 'INSERT ACCOUNT KEY HERE'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}

# Reddit CSV Format
REDDIT_INDEX_DATE = 0
REDDIT_INDEX_TIME = 1
REDDIT_INDEX_ID = 2
REDDIT_INDEX_SCORE = 3
REDDIT_INDEX_TITLE = 4
REDDIT_INDEX_URL = 5

# Detect key phrases.
def text_analytics_keyphrase(text_inputs):
    batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
    req = urllib2.Request(batch_keyphrase_url, text_inputs, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)
    # for keyphrase_analysis in obj['documents']:
    #     print('Key phrases ' + str(keyphrase_analysis['id']) + ': ' + ', '.join(map(str,keyphrase_analysis['keyPhrases'])))
    return obj['documents']

def text_analytics_sentiment(text_inputs):
    # Detect sentiment.
    batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
    req = urllib2.Request(batch_sentiment_url, text_inputs, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)
    # for sentiment_analysis in obj['documents']:
    #     print('Sentiment ' + str(sentiment_analysis['id']) + ' score: ' + str(sentiment_analysis['score']))
    return obj['documents']


# Input: Date, Array of Strings
# Output: CSV File - Date, Keywords, Answer
def analyse_data(asset_file, asset, filename):
    # Read input CSV file
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        input_data = list(reader)

    # Populating output to CSV file
    # Format - date, weightage, percentage_change, keyphrases1, keyphrases2, etc
    output = []
    head_row = ["date", "weightage", "percentage_change"]
    output.append(head_row)

    if (len(input_data) == 0):
        return output

    # print("------------------------------------INPUT DATA-----------------------------------------")
    # print(str(input_data))
    # print("---------------------------------END INPUT DATA-----------------------------------------")

    arr_size = len(input_data)
    data = {}
    doc_arr = []
    data['documents'] = doc_arr
    # Populating input for text analysis
    for i in range(0, arr_size):
        entry = {}
        entry['id'] = i
        unicode_text = unicode(input_data[i][REDDIT_INDEX_TITLE], "ISO-8859-1")
        entry['text'] = str(unidecode(unicode_text))
        doc_arr.append(entry)

    # print("--------------------------TEXT ANALYTICS INPUT DATA--------------------------")
    # print(str(data))
    # print("------------------------END TEXT ANALYTICS INPUT DATA-------------------------")

    arr_keyphrases = text_analytics_keyphrase(str(data))
    arr_sentiments = text_analytics_sentiment(str(data))

    for i in range(0, arr_size):
        entry = []

        # date
        date = input_data[i][REDDIT_INDEX_DATE]
        entry.append(date)

        # weightage
        reddit_score = int(input_data[i][REDDIT_INDEX_SCORE])
        sentiment_score = arr_sentiments[i]['score']
        weightage = reddit_score * (sentiment_score - 0.5)
        # print("Reddit score: " + str(reddit_score) + " Sentiment score: " + str(sentiment_score) + " Weightage: " + str(weightage))
        entry.append(weightage)

        # coordinates
        percentage_change = get_training_data(asset_file, asset, date)
        entry.append(percentage_change)

        # keywords
        keyphrases = arr_keyphrases[i]['keyPhrases']
        # entry_keyphrases = ""
        # first_keyphrase = keyphrases[0]
        # entry_keyphrases += first_keyphrase
        for j in range(0, len(keyphrases)):
            entry.append(str(keyphrases[j]))
            # entry_keyphrases += ',' + keyphrases[j]

        # entry.append(str(entry_keyphrases))


        output.append(entry)

    # print("-----------------------------------CSV OUTPUT DATA--------------------------------------------")
    # print(str(output))
    # print("----------------------------------END CSV OUTPUT DATA------------------------------------------")

    return output
