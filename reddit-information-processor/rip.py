import sys
import praw
import csv
from datetime import date, datetime, timedelta
from pprint import pprint

# Reddit Information Processor (RIP) v1.0, written for the Microsoft Data Science Challenge.

CLIENT_ID     = "CLIENT_ID_HERE"
CLIENT_SECRET = "CLIENT_SECRET_HERE"
USER_AGENT    = "RIPBot v1.0"

reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent = USER_AGENT)
worldnews = reddit.subreddit('worldnews')

if (len(sys.argv) >= 2):
    # First argument is filename. Second is year, third is month.
    SCRAPE_YEAR = False
    
    # Count up the days, count down the months.
    target_year  = int(sys.argv[1])
    target_month = 12
    target_day   = 1
    
    if (len(sys.argv) >= 3):
        target_month = int(sys.argv[2])
    if (len(sys.argv) >= 4):
        target_day = int(sys.argv[3])
    if (len(sys.argv) >= 5):
        SCRAPE_YEAR = bool(sys.argv[4])
        
    start_date = datetime(target_year, target_month, target_day)
    
    # Loop through each month in the year.
    while (start_date.year == target_year):
    
        # Loop through each day in the month.
        while (start_date.month == target_month):
            end_date = start_date + timedelta(hours=23, minutes=59, seconds=59)

            csvfile = open('data/{}.csv'.format(start_date.date()), 'w', newline='', encoding='utf-8')
            csv_writer = csv.writer(csvfile, delimiter=',')
            
            try:
                submissions = worldnews.search(query='timestamp:{}..{}'.format(int(start_date.timestamp()), int(end_date.timestamp())), sort='top', limit=30)
                
                for submission in submissions:
                    # pprint(vars(submission))
                    created_datetime = datetime.fromtimestamp(submission.created)
                    print("[{}] : [{}] {}".format(datetime.fromtimestamp(submission.created), submission.score, submission.title))
                    # result = "{},{},{},{}".format(created_datetime.date(), created_datetime.time(), submission.score, submission.title)
                    # print(result)
                    csv_writer.writerow([created_datetime.date(), created_datetime.time(), submission.id, submission.score, submission.title, submission.domain, submission.url])
                    
                start_date = start_date + timedelta(days=1)
                
            except Exception as e:
                print("--- ERROR OCCURRED! ---")
                print(e)
                #print("--- ERROR OCCURRED! ---")
                print("Retrying...")
            
            csvfile.close()
        
        if not SCRAPE_YEAR:
            break
            
        # -2 months as by the time execution reaches here, the month has been exceeded by 1.
        target_month = (start_date.month - 2) % 12
        if (target_month == 0):
            print("Done.")
            break
        print("New month: {}".format(target_month))
        #target_year = start_date.year   # Reset the year to the passed in value (in case we were in December and incremented ourselves into the new year.)
        start_date = datetime(target_year, target_month, 1)
    
else:
    print("Wrong number of arguments.")