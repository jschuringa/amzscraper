from flask import Flask, request, abort
from urllib.parse import urlparse
from lib.parser import parse_reviews
app = Flask(__name__)

# Handles 'web' validation and returns the report json
@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    url = request.form['url']
    all_pages = request.form['allPages']
    parsed_url = urlparse(url)
    if parsed_url.netloc != "www.amazon.com" or "/product-reviews/" not in parsed_url.path:
        abort(400, "Must be an amazon review page")
    try:
        results = parse_reviews(url, all_pages)
        return results.toJSON()
    except Exception as e:
        abort(500, f"Unexpected error while parsing reviews: {e}")