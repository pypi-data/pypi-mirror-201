from twitscrape.twitter_scraper import TwitterGeolocationScraper

test_scraper = TwitterGeolocationScraper(filter_replies=True)
test_df = test_scraper.run()
test_df.to_csv('test.csv')

#TODO: Learn how to properly utilise pytest, rather than saving a csv of output.
