

#  Personal Blog — Flask + JSON + Admin Panel

A simple yet powerful **personal blogging platform** built with **Flask**, using JSON files as article storage.
It includes a clean homepage, article reader pages, and a secure admin panel to create, edit, and delete articles.

This project is inspired by the Roadmap.sh project challenge and improved with additional features like slug generation, admin authentication, and an editable CMS-like interface.

---

## 🚀 Features

### ✅ Public Features

* View all articles on the homepage
* Read full articles
* Clean Bootstrap UI
* Automatically generated summaries
* URL slug system (e.g., `/articles/article5`)

### 🔐 Admin Features

* Basic HTTP Authentication
* Admin Dashboard (`/admin`)
* Create new article (`/new`)
* Edit article (`/edit/<slug>`)
* Delete article (`/delete/<slug>`)
* JSON-based storage (simple + fast)

---

## 🗂️ Project Structure

```
/articles            → JSON article files
/templates           → HTML templates
    index.html
    admin.html
    edit.html
    new.html
    article.html

/static              → CSS, images, JS
app.py               → Main application logic
README.md            → Project documentation
```

---



## 📄 JSON Article Format

Each article is stored as a separate `.json` file:

```json
{
  "slug": "article5",
  "title": "Example Title",
  "category": "Motivation",
  "summary": "Short summary...",
  "content": "Full article content...",
  "published_date": "January 4, 2025",
  "author": "Author Name"
}
```


---


## 🧠 **How `app.py` Works (Detailed Explanation)**

The heart of the project is **app.py**, which ties together routing, JSON management, and authentication.
Here’s how each part works:

---

### **1️⃣ Articles Directory Setup**

```python
ARTICLES_DIR = Path(__file__).parent / "articles"
```

All articles are stored as separate JSON files inside the `articles/` folder.

---

### **2️⃣ Reading & Normalizing Articles**

* `read_json()` → Safely loads JSON files
* `normalize_json()` → Ensures every article has consistent fields
* `load_article(slug)` → Loads a single article
* `load_all_articles()` → Loads every JSON file and returns a list of articles

Together, these functions handle reading and cleaning data for display.

---

### **3️⃣ Slug Generation**

```python
def calculate_slug():
```

This finds the highest existing article number, then generates the next one:

`article5.json` → next becomes `article6.json`.

---

### **4️⃣ HTTP Basic Authentication**

Admin routes are protected using a decorator:

```python
@requires_auth
```

The decorator:

* Checks the browser’s Authorization header
* If missing/invalid → sends a `401` with `WWW-Authenticate` header
* Browser shows a login popup
* Valid login allows access to admin pages

This secures the admin panel without needing a login form.

---

### **5️⃣ Routes Overview**

#### ✔ Public Routes

| Route              | Description                   |
| ------------------ | ----------------------------- |
| `/`                | Homepage showing all articles |
| `/articles/<slug>` | Displays a single article     |

#### ✔ Admin Routes (all protected)

| Route            | Function              |
| ---------------- | --------------------- |
| `/admin`         | Admin dashboard       |
| `/new`           | Create a new article  |
| `/edit/<slug>`   | Edit existing article |
| `/delete/<slug>` | Delete article        |

Each route interacts with JSON files using Python filesystem operations.

---

### **6️⃣ Creating, Editing, and Deleting Articles**

* `/new` collects form data → creates a JSON file
* `/edit/<slug>` updates an existing JSON file
* `/delete/<slug>` removes the JSON file

This turns your blog into a mini CMS (Content Management System).

---

### **7️⃣ Running the Server**

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Flask starts in debug mode for development.

---


## 🔐 Default Admin Login

```
username: admin
password: secret
```

---

## ✨ Future Improvements (optional ideas)

* Tag filtering
* Search bar
* Dark mode
* Image uploads for articles
* Rich text editor (Quill/TinyMCE)
* Deploy on Render/Railway

---

## 🙌 Special Thanks

### ⭐ Roadmap.sh

This project is based on the amazing challenge from:
**[https://roadmap.sh/projects/personal-blog](https://roadmap.sh/projects/personal-blog)**












