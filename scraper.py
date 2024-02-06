import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
from utils.response import Response


def scraper(url, resp):
    links = extract_next_links(url, resp)
    # Removing the fragment section by splitting by # and getting the part before it
    links_list = [link.split('#')[0] for link in links if is_valid(link)]
    #print(links_list)
    return []


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    urlList = [] # we return this

    # Checking to see if the status code is of a valid type
    if resp.status != 200:
        if resp.status >= 400: # All status codes in the 4xx series are the result of an error, so we skip these urls
            return urlList
        elif resp.status == 204: # Page with no content (a blank page)
            return urlList
        elif resp.status >= 300: # Check for redirection issues
            # FINISH THIS
            print("300")
        
    # print("STATUS")
    # print(type(resp.status))
    # print(resp.status)
    cleaned_texts = [resp.raw_response.content] # get the content of the page
    newList = []
    for text in cleaned_texts: # filter all html tags, also newline, carriage return, tab and \xa0 (unicode) chars. 
       soup = BeautifulSoup(text, 'html.parser')
       newList.append(soup.get_text(separator='\n').strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('\xa0', ''))
 
    combined_text = '\n'.join(newList) #make the list as a single list to be able to use re.findall, or tokenize function from PartA
    english_words = re.findall(r"[a-zA-Z0-9]+", combined_text) #filter all non-alphanumeric chars
    print(english_words) #print to check

    #print(resp.raw_response.content) #4 pages
    soup = BeautifulSoup(resp.raw_response.content, "html.parser", parse_only=SoupStrainer('a')) # create beautiful soup object and filter to get only a tags
    #print(currentPage.content)
    count = 0
    for elem in soup:
        if elem.has_attr("href") and elem["href"] not in urlList: # if element has link
            link = elem["href"]
            count += 1
            urlList.append(link)
   # print(count)
    
    return urlList


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
         # Checking to see if the current page is in the domain
        icsSearch = re.search(".ics.uci.edu/", url)
        csSearch = re.search(".cs.uci.edu/", url)
        informaticsSearch = re.search(".informatics.uci.edu/", url)
        statsSearch = re.search(".stat.uci.edu/", url)

        if (icsSearch is None and csSearch is None and informaticsSearch is None and statsSearch is None):
            return False

        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

if __name__ == "__main__":
    test = {"url": "https://www.ics.uci.edu", # create dict to create Response object
            "status": 0,
            "error": None
            }
    testResponse = Response(test) # dummy Response object so extract_next_links can be called
    print(scraper("https://www.ics.uci.edu", testResponse))
    