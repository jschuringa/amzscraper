import requests
import json
from bs4 import BeautifulSoup

class ParsedField():
    def __init__(self, name, tag_type, attr_name, attr="class"):
        self.tag_type = tag_type
        self.attr_name = attr_name
        self.name = name
        self.attr = attr

# I don't think I necessarily need this object anymore, since I'm using setattr
# but is probably useful for testing
class ParsedReview(object):
    title = ""
    content = ""
    author = ""
    stars = 0
    date = ""
    failed = False
    error = ""

    def get_required_field(self, name, element):
            if(element is None):
                raise Exception(f"No field found with the name '{name}'. Cannot parse review, '{name}' is a required field.")
            else:
                if len(element.contents) == 0:
                    raise Exception(f"No contents found in field '{name}'.")
                return element.contents[0]

    def build_report_item(self, fields, source):
        for field in fields:
            setattr(self, field.name, self.get_required_field(field.name, source.find(field.tag_type, {field.attr: field.attr_name})))

class ReviewReport:
    def __init__(self, reviews):
        self.reviews = reviews

    # I saw a few ways to create json for a complex object, this seemed the easiest
    # without additional dependencies
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# reads the html from a (assumed valid) url, and parses the field data from them
# handles errors for each review and sets error/failed field. This isn't necessarily
# useful from an API standpoint, but it felt weird just letting raised exceptions
# fall into the abyss, and it didn't make sense to end parsing just because one 
# field/review failed
def parse_reviews(url, all_pages):
    fields = [
        ParsedField("title", "a", "review-title", "data-hook"),
        ParsedField("date", "span", "review-date", "data-hook"),
        ParsedField("content", "span", "review-body", "data-hook"),
        ParsedField("author", "span", "a-profile-name"),
    ]

    parsed_reviews = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html5lib")
    review_items = soup.findAll("div", {"data-hook": "review"})

    for review in review_items:
        this_review = ParsedReview()
        try:
            this_review = build_report_item(thisReview, fields, review)
            parsed_reviews.append(this_review)
        except Exception as e:
            this_review.failed = True
            this_review.error = e

    return ReviewReport(parsed_reviews)