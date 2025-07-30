from flask import Flask, render_template
from pathlib import Path
import json


app = Flask(__name__)

#Get storage.json path (cross platform)
root_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
json_path = root_dir / "storage" / "storage.json"


@app.route("/")
def index():
    with json_path.open("r", encoding="utf-8") as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)