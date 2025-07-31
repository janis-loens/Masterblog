# Masterblog

A simple blog application built with Flask that allows users to:

- View existing blog posts
- Add new blog posts
- Edit and update existing posts
- Delete posts

All blog data is stored locally in a `storage.json` file.

---

## 🚀 Features

- Create, edit, and delete blog posts
- Posts are stored in a JSON file for simplicity
- Clean and responsive interface using HTML & CSS
- Cross-platform path handling using `pathlib`
- Minimal dependencies for quick deployment

---

## 📁 Project Structure

```
Masterblog/
├── app.py                # Main Flask app
├── storage/
│   └── storage.json      # JSON file holding blog posts
├── templates/
│   ├── index.html        # Homepage showing all posts
│   ├── add.html          # Form to add a new post
│   └── update.html       # Form to update an existing post
├── static/
│   └── style.css         # Stylesheet for the blog
├── LICENSE               # Optional license file
├── README.md             # README file
└── requirements.txt      # Requirements for deployment
```

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/janis-loens/Masterblog.git
cd Masterblog
```

2. **Set up a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000/`.

---

## 📝 Usage

- Click **"Add blog post"** to create a new post.
- Use the **Edit** button to update content.
- Use the **Delete** button to remove a post.
- All posts are saved to `storage/storage.json`.

---

## 📌 Requirements

- Python 3.7+
- Flask

---

## 📖 License

This project is licensed under the terms of the [MIT License](LICENSE).
