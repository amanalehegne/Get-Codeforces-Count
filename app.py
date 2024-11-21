import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_solved_count(handle):
    try:
        url = f"https://codeforces.com/profile/{handle}"
        scraper = cloudscraper.create_scraper()
        res = scraper.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        count_tag = soup.find("div", class_="_UserActivityFrame_counterValue")
        return int(count_tag.get_text(strip=True).split()[0]) if count_tag else 0
    except (cloudscraper.exceptions.CloudflareChallengeError, ValueError) as e:
        print(f"Error for {handle}: {e}")
        return 0

@app.route('/get_solved_count/', methods=['GET'])
def solved_count():
    handle = request.args.get('handle')
    if not handle:
        return jsonify({"error": "Handle is required"}), 400
    count = get_solved_count(handle)
    return jsonify({"handle": handle, "solved_count": count})

@app.route('/fetch_counts/', methods=['POST'])
def fetch_counts():
    data = request.get_json()
    if not data or 'handles' not in data:
        return jsonify({"error": "JSON payload with 'handles' list is required"}), 400
    handles = data.get('handles', [])
    if not isinstance(handles, list):
        return jsonify({"error": "'handles' should be a list"}), 400
    results = {handle: get_solved_count(handle) for handle in handles}
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
