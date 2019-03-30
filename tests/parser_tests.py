import unittest
from lib import parser
from bs4 import BeautifulSoup

class TestParserMethods(unittest.TestCase):

    # def test_getRequiredItem_isNone(self):
    #     self.assertRaises(Exception, lambda:parser.getRequiredField("test", None), "No field found with the name 'test'. Cannot parse review, 'test' is a required field.")

    # def test_getRequiredItem_Succeeds(self):
    #     htmlString = "<p class='reviewTitle'>test</p>"
    #     source = BeautifulSoup(htmlString, "html5lib")
    #     element = source.find("p", {"class": "reviewTitle"})
    #     result = parser.getRequiredField("title", element)
    #     self.assertEqual("test", result)

    # def test_getRequiredItem_contentIsEmpty(self):
    #     htmlString = "<p class='reviewTitle'></p>"
    #     source = BeautifulSoup(htmlString, "html5lib")
    #     element = source.find("p", {"class": "reviewTitle"})
    #     self.assertRaises(Exception, lambda:parser.getRequiredField("title", element), "No contents found in field 'title'.")

    # def test_buildReportItem_succeeds(self):
    #     htmlString = "<p class='reviewTitle'>test</p>"
    #     source = BeautifulSoup(htmlString, "html5lib")
    #     review = parser.ParsedReview()
    #     fields = [parser.ParsedField("title", "p", "reviewTitle")]
    #     review = parser.buildReportItem(review, fields, source)
    #     self.assertEqual("test", review.title)

    # def test_buildReportItem_fieldDoesntExist(self):
    #     htmlString = "<p class='reviewTitle'>test</p>"
    #     source = BeautifulSoup(htmlString, "html5lib")
    #     review = parser.ParsedReview()
    #     fields = [parser.ParsedField("title", "p", "asdf")]
    #     self.assertRaises(Exception, lambda:parser.buildReportItem(review, fields, source))

    # def test_buildReportItem_handlesMalformedTag(self):
    #     htmlString = "<p class='reviewTitle'>test</p"
    #     source = BeautifulSoup(htmlString, "html5lib")
    #     review = parser.ParsedReview()
    #     fields = [parser.ParsedField("title", "p", "reviewTitle")]
    #     review = parser.buildReportItem(review, fields, source)
    #     self.assertEqual("test", review.title)

    def test_parseReviewsFromUrl_integration(self):
        url = "https://www.amazon.com/New-Improved-Flask-Mega-Tutorial/product-reviews/1977051871/ref=cm_cr_arp_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
        report = parser.parse_reviews(url)
        self.assertEqual(10, len(report.reviews))
        self.assertTrue(report.reviews[0].recommended)
        self.assertEqual(1, report.reviews[0].stars)

if __name__ == '__main__':
    unittest.main()