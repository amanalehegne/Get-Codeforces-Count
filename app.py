from flask import Flask, request, jsonify
import bs4
import requests

app = Flask(__name__)

def getTotalProblems(handle):
    try:
        url = "https://codeforces.com/profile/" + handle
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        solved_problems = soup.findAll(
            "div", class_="_UserActivityFrame_counterValue")[0].get_text()

        return int(solved_problems.split(' ')[0])

    except Exception as e:
        print(f"Error occurred: {e}")
        return 0

@app.route('/get_total_problems', methods=['GET'])
def get_total_problems():
    handle = request.args.get('handle')
    if not handle:
        return jsonify({"error": "Handle is required"}), 400

    total_problems = getTotalProblems(handle)
    return jsonify({"handle": handle, "total_problems": total_problems})

if __name__ == '__main__':
    app.run(debug=True)
