from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import json


app = Flask(__name__)

#Get storage.json path (cross platform)
root_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
json_path = root_dir / "storage" / "storage.json"

def read_storage_json() -> list[dict]:
    """Open, read and close the storage.json file to retrieve all posts.
    Args:
        None
    Returns:
        list: The a list of dictionaries containing information about the posts.
    """
    with json_path.open("r", encoding="utf-8") as file:
        posts = json.load(file)
    return posts


def write_storage_json(content: list) -> None:
    """Open, write and close the storage.json file to retrieve all posts.
    Args:
        content(list): The content to be written into the json file.
    Returns:
        None
    """
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(content, file, indent=2)


@app.route("/")
def index():
    return render_template("index.html", posts=read_storage_json())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        posts = read_storage_json()
        if posts:
            next_id = max(post["id"] for post in posts) + 1
        else:
            next_id = 1  # start from 1 if no posts yet
        
        new_post = {
            "id": next_id,
            "author": request.form.get("author"),
            "title": request.form.get("post_title"),
            "content": request.form.get("post_content"),
        }

        posts.append(new_post)
        write_storage_json(posts)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    posts = read_storage_json()

    posts = [post for post in posts if post.get("id") != post_id]

    write_storage_json(json_path, posts)

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = read_storage_json()
    post = next((post for post in posts if post["id"] == post_id), None)
    if post is None:
        # Post not found
        return "Post not found", 404
    
    if request.method == "POST":
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("post_title")
        post["content"] = request.form.get("post_content")
        # Update the post in the JSON file
        write_storage_json(posts)
        return redirect(url_for("index"))

    # Else, it's a GET request
    # So display the update.html page
    return render_template("update.html", post=post)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)