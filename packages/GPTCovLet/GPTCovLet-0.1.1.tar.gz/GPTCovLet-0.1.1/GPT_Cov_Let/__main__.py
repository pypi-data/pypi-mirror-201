from . import scrapeToGPT

if __name__ == "__main__":
    url = "https://www.linkedin.com/jobs/view/dev10-entry-level-software-developer-nationwide-at-dev10-3497504875/?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"
    scrapeToGPT.urlScrape(url)
