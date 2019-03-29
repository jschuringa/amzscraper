from flask import Flask, request, abort
from urllib.parse import urlparse
from lib.parser import parseReviewsFromUrl
app = Flask(__name__)

# Handles 'web' validation and returns the report json
@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    url = request.form['url']
    parsedUrl = urlparse(url)
    if parsedUrl.netloc != "www.lendingtree.com" or not parsedUrl.path.startswith("/reviews/") :
        abort(400, "Must be a lendingtree review page")
    try:
        results = parseReviewsFromUrl(url)
        return results.toJSON()
    except Exception as e:
        abort(500, f"Unexpected error while parsing reviews: {e}")