import time
from bs4 import BeautifulSoup
import multiprocessing as mp
from threading import Thread
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer

START_TIME = default_timer()

def fetch(session, href):
    thisJob = jobListing()

    base_url = "https://www.indeed.com"
    with session.get(base_url + href) as response:
        print("Going to job")
        print(base_url+href)
        data = response.text

        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.2f}s".format(elapsed)
        #print("{0:<30} {1:>20}".format(href, time_completed_at))
        info = BeautifulSoup(response.content, "html.parser")
        jobTitle = info.find("h1", class_="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title")
        job_desc = info.find(id="jobDescriptionText")
        thisJob.jobDesc = (job_desc)
        # print(job_desc)
        try:
            thisJob.jobTitle = jobTitle.text
            # print(jobTitle.text)
        except:
            # print("-No Title-")
            thisJob.jobTitle = "-No Title-"

        listings.append(thisJob)
        return data

async def get_job_data(hrefs):

    #print("{0:<30} {1:>20}".format("File", "Completed at"))
    with ThreadPoolExecutor(max_workers=20) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, href) # Allows us to pass in multiple arguments to `fetch`
                )
                for href in hrefs
            ]
            for response in await asyncio.gather(*tasks):
                pass



cpuCount = (mp.cpu_count())

baseURL = 'https://www.indeed.com'
url = ('https://www.indeed.com/jobs?q=information+technology&start=')


#"https://www.indeed.com/jobs?q=information+technology&start=0"

listings  = []

#print(currentPageUrl)

#page = requests.get(url)


class jobListing:
    jobTitle = ""
    jobDesc = ""
    output = jobTitle + ": " + jobDesc

    def __str__(self):

        return self.output




def refineDesc(desc = BeautifulSoup()):

    for a in desc.find_all('p'):
        print(a)
        if "Responsibilities" in a:
            print("found one")
            element = a
        else:
            element = "not there"

    #print(element)
    return element


def getResultsFromPage(pageNumber):
    currentPageUrl = url + pageNumber.__str__()

    try:
        page = requests.get(currentPageUrl)
    except:
        return
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="mosaic-provider-jobcards")

    # print(results.prettify())

    hrefs = []

    for a in results.find_all('a', href=True):

        if "clk?" in a['href']:
            # print("Found the URL:", a['href'])
            hrefs.append(a['href'])

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_job_data(hrefs))
    loop.run_until_complete(future)

        #t.start()
    # print(hrefs)



pageNum = 0

while True:

    print("started page")
    getResultsFromPage(pageNum)

    pageNum = pageNum +1
    if pageNum == 1:
        break


#mp.Process.join()
print(len(listings))
for jobListing in listings:
    print(jobListing.jobTitle)
    try:
        jobRequirements = refineDesc(jobListing.jobDesc)
        print(jobRequirements)
    except:
        print("no reqiremtns statment")




    print("\n")


