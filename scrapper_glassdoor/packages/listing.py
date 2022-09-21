# Import necessary libraries
# standard libraries
from time import time
# custom functions
try:
    from packages.common import requestAndParse
except ModuleNotFoundError:
    from common import requestAndParse
    
# extracts desired data from listing banner
def extract_listingBanner(listing_soup, url):
    listing_bannerGroup_valid = False

    try:
        listing_bannerGroup = listing_soup.find("div", class_="css-ur1szg e11nt52q0")

        listing_bannerGroup_valid = True
    except:
        print("[ERROR] Error occurred in function extract_listingBanner")
        companyName = "NA"
        company_starRating = "NA"
        company_offeredRole = "NA"
        company_roleLocation = "NA"
        salary = "NA"
    
    if listing_bannerGroup_valid:
        try:
            company_starRating = listing_bannerGroup.find("span", class_="css-1pmc6te e11nt52q4").getText()
        except:
            company_starRating = "NA"

        if company_starRating != "NA":
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText().replace(company_starRating,'')
            except:
                companyName = "NA"
            # company_starRating.replace("★", "")
            company_starRating = company_starRating[:-1]
        else:
            try:
                companyName = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText()
            except:
                companyName = "NA"

        try:
            company_offeredRole = listing_bannerGroup.find("div", class_="css-17x2pwl e11nt52q6").getText()
        except:
            company_offeredRole = "NA"

        try:
            company_roleLocation = listing_bannerGroup.find("div", class_="css-1v5elnn e11nt52q2").getText()
        except:
            company_roleLocation = "NA"

        try:
            salary = listing_bannerGroup.find("span", class_ = "small css-10zcshf e1v3ed7e1").getText()
        except:
            salary = "NA"

    return companyName, company_starRating, company_offeredRole, company_roleLocation, salary

# extracts desired data from listing description
def extract_listingDesc(listing_soup):
    extract_listingDesc_tmpList = []
    listing_jobDesc_raw = None

    try:
        listing_jobDesc_raw = listing_soup.find("div", id="JobDescriptionContainer")
        if type(listing_jobDesc_raw) != type(None):
            JobDescriptionContainer_found = True
        else:
            JobDescriptionContainer_found = False
            listing_jobDesc = "NA"
    except Exception as e:
        print("[ERROR] {} in extract_listingDesc".format(e))
        JobDescriptionContainer_found = False
        listing_jobDesc = "NA"

    if JobDescriptionContainer_found:
        #jobDesc_items = listing_jobDesc_raw.findAll('li')
        #for jobDesc_item in jobDesc_items:
            #extract_listingDesc_tmpList.append(jobDesc_item.text)
        
        jobDesc_items_br = listing_jobDesc_raw.findAll('div')
        for jobDesc_item in jobDesc_items_br:
            extract_listingDesc_tmpList.append(jobDesc_item.text) 
        
        listing_jobDesc = " ".join(extract_listingDesc_tmpList)

        if len(listing_jobDesc) <= 10:
            listing_jobDesc = listing_jobDesc_raw.getText()

    return listing_jobDesc

# extract data from listing
def extract_listing(url):
    request_success = False
    try:
        listing_soup, requested_url = requestAndParse(url)
        request_success = True
    except Exception as e:
        print("[ERROR] Error occurred in extract_listing, requested url: {} is unavailable.".format(url))
        return ("NA", "NA", "NA", "NA", "NA", "NA")

    if request_success:
        companyName, company_starRating, company_offeredRole, company_roleLocation, salary = extract_listingBanner(listing_soup, url)
        listing_jobDesc = extract_listingDesc(listing_soup)

        return (companyName, company_starRating, company_offeredRole, company_roleLocation, listing_jobDesc, salary, requested_url)

if __name__ == "__main__":
    
    url = "https://www.glassdoor.es/job-listing/junior-data-analyst-metiora-JV_IC2664239_KO0,19_KE20,27.htm?jl=1008039079887&pos=107&ao=1136043&s=58&guid=000001824e740ab49619e7165965940d&src=GD_JOB_AD&t=SR&vt=w&cs=1_ca48d4e5&cb=1659173604430&jobListingId=1008039079887&jrtk=3-0-1g97782n82gpn001-1g97782nngsr9800-3b0ce067d9f66178-&ctt=1659174594449"
    start_time = time()
    returned_tuple = extract_listing(url)
    time_taken = time() - start_time
    print(returned_tuple)
    print("[INFO] returned in {} seconds".format(time_taken))