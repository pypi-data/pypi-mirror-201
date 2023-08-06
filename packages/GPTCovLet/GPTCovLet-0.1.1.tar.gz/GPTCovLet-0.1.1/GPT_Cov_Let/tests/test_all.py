from unittest.mock import patch
import sys, os
import os.path

# __file__
# os.path.join(os.path.dirname(__file__), "staticPageUnitTest.html")
sys.path.append(os.path.abspath("../.."))
# print(os.path)
# print(sys.path)
from bs4 import BeautifulSoup

from GPT_Cov_Let import scrapeToGPT


def test_descScrape():
    # by absolute definition the improved unit test would make a get request and get the file but in lieu of making my first ever unit test doable i did it with a static file saved in the directory (so at very least it works offline)

    pseudoHTML = open("GPT_Cov_Let/tests/staticPageUnitTest.html", "r").read()
    pseudoHTML = BeautifulSoup(pseudoHTML, "html.parser")
    # print(scrapeToGPT.descScrape(pseudoHTML))
    assert scrapeToGPT.descScrape(pseudoHTML), "RTTS"

    return


"""
def test_integration():
    url = "https://www.linkedin.com/jobs/view/software-test-engineer-entry-level-at-rtts-3470060740/?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"
    description = scrapeToGPT.urlScrape(url)
    assert scrapeToGPT.completionQuery(description), True

"""

# def completionQuery Test (insert without coverLetter)

url = "https://www.linkedin.com/jobs/view/dev10-entry-level-software-developer-nationwide-at-dev10-3497504875/?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"
# scrapeToGPT.urlScrape(url) #ALSO CANNOT TEST THIS BC REQUIRES GITHUB SECRETS
test_descScrape()  # current scrapes company name
# test_integration() #CANNOT TEST THIS BC REQUIRES GITHUB SECRETS
