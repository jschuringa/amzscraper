import unittest
from lib import parser
from bs4 import BeautifulSoup

class TestParserMethods(unittest.TestCase):

    def test_getRequiredItem_isNone(self):
        self.assertRaises(Exception, lambda:parser.getRequiredField("test", None), "No field found with the name 'test'. Cannot parse review, 'test' is a required field.")

    def test_getRequiredItem_Succeeds(self):
        htmlString = "<p class='reviewTitle'>test</p>"
        source = BeautifulSoup(htmlString, "html5lib")
        element = source.find("p", {"class": "reviewTitle"})
        result = parser.getRequiredField("title", element)
        self.assertEqual("test", result)

    def test_getRequiredItem_contentIsEmpty(self):
        htmlString = "<p class='reviewTitle'></p>"
        source = BeautifulSoup(htmlString, "html5lib")
        element = source.find("p", {"class": "reviewTitle"})
        self.assertRaises(Exception, lambda:parser.getRequiredField("title", element), "No contents found in field 'title'.")

    def test_buildReportItem_succeeds(self):
        htmlString = "<p class='reviewTitle'>test</p>"
        source = BeautifulSoup(htmlString, "html5lib")
        review = parser.ParsedReview()
        fields = [parser.ParsedField("title", "p", "reviewTitle")]
        review = parser.buildReportItem(review, fields, source)
        self.assertEqual("test", review.title)

    def test_buildReportItem_fieldDoesntExist(self):
        htmlString = "<p class='reviewTitle'>test</p>"
        source = BeautifulSoup(htmlString, "html5lib")
        review = parser.ParsedReview()
        fields = [parser.ParsedField("title", "p", "asdf")]
        self.assertRaises(Exception, lambda:parser.buildReportItem(review, fields, source))

    def test_buildReportItem_handlesMalformedTag(self):
        htmlString = "<p class='reviewTitle'>test</p"
        source = BeautifulSoup(htmlString, "html5lib")
        review = parser.ParsedReview()
        fields = [parser.ParsedField("title", "p", "reviewTitle")]
        review = parser.buildReportItem(review, fields, source)
        self.assertEqual("test", review.title)

    def test_parseReviewsFromUrl_integration(self):
        url = "https://www.lendingtree.com/reviews/personal/lendingclub/33829657?sort=cmV2aWV3c3VibWl0dGVkX2FzYw==&pid=1"
        report = parser.parseReviewsFromUrl(url)
        self.assertEqual(10, len(report.reviews))
        self.assertTrue(report.reviews[0].recommended)
        self.assertEqual(1, report.reviews[0].stars)

if __name__ == '__main__':
    unittest.main()