from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import json


app = Flask(__name__)

#Get storage.json path (cross platform)
root_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
json_path = root_dir / "storage" / "storage.json"

def read_storage_json() -> list[dict]:
    """Open, read and close the storage.json file to retrieve all posts.

    Returns:
        list: A list of dictionaries containing information about the posts.
    """
    try:
        # Ensure parent directory exists
        json_path.parent.mkdir(parents=True, exist_ok=True)

        # If file doesn't exist, create it with an empty list
        if not json_path.exists():
            with json_path.open("w", encoding="utf-8") as file:
                json.dump([], file, indent=2)

        # Now read from the file
        with json_path.open("r", encoding="utf-8") as file:
            posts = json.load(file)
            if not isinstance(posts, list):
                raise ValueError("JSON content must be a list of posts.")
            return posts

    except FileNotFoundError:
        print("Error: storage.json not found. Returning an empty list.")
        return []
    except json.JSONDecodeError:
        print("Error: storage.json is empty or malformed. Returning an empty list.")
        return []
    except Exception as e:
        print(f"Error: Unexpected error reading JSON: {e}. Returning an empty list.")
        return []



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
    """Render the homepage displaying all blog posts.
    
    Returns:
        Response: The rendered HTML page with all posts loaded from storage.
    """
    return render_template("index.html", posts=read_storage_json())


@app.route("/add", methods=["GET", "POST"])
def add():
    """Handle creation of a new blog post.

    GET:
        Renders the form to add a new post.

    POST:
        Parses from data, assigns a unique ID, and appends the new post
        to the JSON storage. Redirects to the homepage after successful creation.

    Returns:
        Response: A rendered form page (GET) or a redirect to homepage (POST).
    """
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
    """Delete a blog post by its unique ID.

    Args:
        post_id(int): The unique ID of the post to delete.
    
    Returns:
        Redirect to the homepage after deletion.
    """
    posts = read_storage_json()

    posts = [post for post in posts if post.get("id") != post_id]

    write_storage_json(posts)

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Update an existing blog post by its unique ID.
    Args:
        post_id(int): The unique ID of the post to update.
    Returns:
        Response: A rendered form page for updating the post (GET) or a redirect to homepage (POST).
    """
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
    # Render the update form with the current post data
    return render_template("update.html", post=post)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)