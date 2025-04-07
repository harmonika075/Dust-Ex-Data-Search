
from flask import Flask, render_template, request
from data.dust_data import dust_data

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query", "").lower()
    page = int(request.args.get("page", 1))
    page_size = 20

    if query:
        matches = [entry for entry in dust_data if query in entry["material"].lower()]
        valid_matches = [
            entry for entry in matches if any(p != "no data" for p in entry["explosion_properties"])
        ]

        valid_matches.sort(key=lambda x: (
            x["material"].lower() != query,
            -sum(p != "no data" for p in x["explosion_properties"]),
            x["median_size"] == "–"
        ))

        start = (page - 1) * page_size
        end = start + page_size
        results_to_show = valid_matches[:end]
        show_more = len(valid_matches) > end

        return render_template("index.html",
                               results=valid_matches,
                               results_to_show=results_to_show,
                               show_more=show_more,
                               query=query,
                               page=page)
    else:
        return render_template("index.html", results=[], results_to_show=[], show_more=False, query="", page=1)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
