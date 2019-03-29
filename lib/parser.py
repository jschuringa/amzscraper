import requests
import json
from bs4 import BeautifulSoup

class ParsedField():
    def __init__(self, name, tagType, className):
        self.tagType = tagType
        self.className = className
        self.name = name

# I don't think I necessarily need this object anymore, since I'm using setattr
# but is probably useful for testing
class ParsedReview(object):
    title = ""
    text = ""
    author = ""
    stars = 0
    date = ""
    recommended = False
    loanType = ""
    reviewType = ""
    closedWith = False
    failed = False
    error = ""

class ReviewReport:
    def __init__(self, reviews):
        self.reviews = reviews
        if(len(reviews) > 0):
            self.totalReviews = len(reviews)
            self.totalPositive = sum(1 for review in reviews if review.stars >= 3)
            self.totalNegative = sum(1 for review in reviews if review.stars < 3)
            self.avgStars = sum(review.stars for review in reviews) / self.totalReviews

    # I saw a few ways to create json for a complex object, this seemed the easiest
    # without additional dependencies
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# takes in the list of required fields and html source, and sets the required field on the parsed review object
# keeps all the individual tag selection in one place (besides special cases)
def buildReportItem(review, fields, source):
    for field in fields:
        setattr(review, field.name, getRequiredField(field.name, source.find(field.tagType, {"class": field.className})))
    return review

# if the element does not exist or does not have content, raises an error for the required field.
def getRequiredField(name, element):
    if(element is None):
        raise Exception(f"No field found with the name '{name}'. Cannot parse review, '{name}' is a required field.")
    else:
        if len(element.contents) == 0:
            raise Exception(f"No contents found in field '{name}'.")
        return element.contents[0]

# reads the html from a (assumed valid) url, and parses the field data from them
# handles errors for each review and sets error/failed field. This isn't necessarily
# useful from an API standpoint, but it felt weird just letting raised exceptions
# fall into the abyss, and it didn't make sense to end parsing just because one 
# field/review failed
def parseReviewsFromUrl(url):
    fields = [
        ParsedField("title", "p", "reviewTitle"),
        ParsedField("content", "p", "reviewText"),
        ParsedField("author", "p", "consumerName"),
        ParsedField("date", "p", "consumerReviewDate"),
    ]

    parsedReviews = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html5lib")
    reviews = soup.findAll("div", {"class": "mainReviews"})

    for review in reviews:
        thisReview = ParsedReview()
        try:
            thisReview = buildReportItem(thisReview, fields, review)
            starsEl = review.find("div", {"class": "numRec"})
            if starsEl is None:
                raise Exception("No stars field found, stars is a required field to parse a review.")
            else:
                thisReview.stars = int(starsEl.contents[0][1])
            thisReview.recommended = review.find("div", {"class": "lenderRec"}) is not None
            thisReview.closedWith = review.find("p", {"class": "yes"}) is not None
            try:
                listItems = review.findAll("div", {"class": "loanType"})
                if len(listItems) == 2:
                    thisReview.loanType = listItems[0].contents[0]
                    thisReview.reviewType = listItems[1].contents[0]
            except:
                thisReview.failed = True
                thisReview.error = "Failed to parse loan type and review type."
            parsedReviews.append(thisReview)
        except Exception as e:
            thisReview.failed = True
            thisReview.error = e

    report = ReviewReport(parsedReviews)

    return report
