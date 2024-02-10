import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
import sys
from utils.response import Response


# This is a storage class in order to store important information
class webScraperStorage:
    totalURLCount = 0
    longestPage = 0
    longestNumWords = 0
    newList = []
    checkSumList = []

def scraper(url, resp):
    links = extract_next_links(url, resp)
    # Removing the fragment section by splitting by # and getting the part before it
    links_list = [link.split('#')[0] for link in links if is_valid(link)]
    return links_list

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

    cleaned_texts = [resp.raw_response.content] # get the content of the page
    newList = []
    for text in cleaned_texts: # filter all html tags, also newline, carriage return, tab and \xa0 (unicode) chars. 
       soup = BeautifulSoup(text, 'html.parser')
       newList.append(soup.get_text(separator='\n').strip().replace('\n', '').replace('\r', '').replace('\t', '').replace('\xa0', ''))

    combined_text = '\n'.join(newList) #make the list as a single list to be able to use re.findall, or tokenize function from PartA
    english_words = re.findall(r"[a-zA-Z0-9]+", combined_text) #filter all non-alphanumeric chars

    all_words_length = len(english_words)

    # Checking how many words there are
    if (all_words_length > 100000):
        return urlList
    
    if all_words_length > webScraperStorage.longestPage:
        webScraperStorage.longestPage = resp.raw_response.url
        webScraperStorage.longestNumWords = all_words_length
    
    checkSumTotal = 0
    # Using checksum in order to check for exact duplicates of pages
    for word in english_words:
        for letter in word:
            checkSumTotal += ord(letter)

    if checkSumTotal in webScraperStorage.checkSumList:
        return urlList
    else:
        webScraperStorage.checkSumList.append(checkSumTotal)

    # This is the set of stop words that we check
    stop_words_set = {"a", "about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being",
        "below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during",
        "each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's",
        "hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself",
        "let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours", "ourselves","out",
        "over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them",
        "themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very",
        "was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why",
        "why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"}
    
    # Looping through all of the words and deleting stop words
    english_words = [word for word in english_words if word not in stop_words_set]
    # for key, i in enumerate(english_words):
    #     if i in stop_words_set:
    #         del english_words[key]

    # Checking if the ratio of the number of valid words over the total number of words is over the 30 percent threshold
    valid_words_length = len(english_words)

    if (all_words_length == 0):
        return urlList

    if (valid_words_length/all_words_length < 0.15):
        return urlList


    soup = BeautifulSoup(resp.raw_response.content, "html.parser", parse_only=SoupStrainer('a')) # create beautiful soup object and filter to get only a tags
    # print(currentPage.content)
    count = 0
    for elem in soup:
        if elem.has_attr("href") and elem["href"] not in urlList: # if element has link
            link = elem["href"]
            count += 1
            urlList.append(link)
    # print(count)
    print()
    print()
    print(resp.raw_response.url)
    print()
    print()
    if resp.raw_response.url in newList:
        raise ValueError('A very specific bad thing happened.')
    webScraperStorage.newList.append(resp.raw_response.url)
    webScraperStorage.totalURLCount += 1
    return urlList

def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
         # Checking to see if the current page is in the domain
        icsSearch = re.search("\.ics\.uci\.edu/", url)
        csSearch = re.search("\.cs\.uci\.edu/", url)
        informaticsSearch = re.search("\.informatics\.uci\.edu/", url)
        statsSearch = re.search("\.stat\.uci\.edu/", url)

        # Checking for a calendar url
        if len(re.findall(r"[/]*\d{1,4}[/-]{1}0*\d{0,2}[/-]{1}0*\d{1,2}[/]*", url)) != 0:
            return False

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
    icsSearch = re.search("\.ics\.uci\.edu/", "https://ngs.ics.uci.edu/to-brazil-thinking-computer-vision-in-developing-countries")
    csSearch = re.search("\.cs\.uci\.edu/", "https://ngs.ics.uci.edu/to-brazil-thinking-computer-vision-in-developing-countries")
    informaticsSearch = re.search("\.informatics\.uci\.edu/", "https://ngs.ics.uci.edu/to-brazil-thinking-computer-vision-in-developing-countries")
    statsSearch = re.search("\.stat\.uci\.edu/", "https://ngs.ics.uci.edu/to-brazil-thinking-computer-vision-in-developing-countries")
    

    if (icsSearch or csSearch or informaticsSearch or statsSearch):
            print("False")
            sys.exit(0)

    print("true")

    # test = {"url": "https://www.ics.uci.edu", # create dict to create Response object
    #         "status": 0,
    #         "error": None
    #         }
    # testResponse = Response(test) # dummy Response object so extract_next_links can be called
    # print(scraper("https://www.ics.uci.edu", testResponse))


    