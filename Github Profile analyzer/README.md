


# GitHub Profile Analyzer (Beginner Python Project)

A simple command-line Python app that uses the **GitHub REST API** to fetch:

- User profile details  
- Recent public events  
- Public repositories  

It then prints a clean summary in the terminal and saves all raw API responses as JSON files.

This project is inspired by the **GitHub User Activity** challenge on Roadmap.sh:  
➡️ https://roadmap.sh/projects/github-user-activity

---

## 📌 Important Note

This project uses **public GitHub API endpoints** and is intended strictly for **learning purposes**.

While testing the application, I used the **public GitHub profile of Kamran Ahmed** (creator of roadmap.sh) only as an example:  
➡️ https://github.com/kamranahmedse

No personal or private data is accessed, stored, or misused.  
Everything fetched is already publicly visible on GitHub and allowed by their API usage policies.

---

## 🚀 Features

- Fetch GitHub user profile details (`/users/{username}`)
- Fetch recent public events (`/users/{username}/events`)
- Fetch public repositories (`/users/{username}/repos`)
- Save all responses to JSON files:
  - `gitdetails.json`
  - `gitactivity.json`
  - `gitrepolist.json`
- Print:
  - Basic profile summary (name, followers, following, bio, Twitter)
  - List of public repositories
  - Stars and languages for each public repo
  - Language usage statistics

---

## 🧰 Requirements

- Python 3.7+
- `requests` library

Install dependencies:

```bash
pip install requests
````

---

## 📁 Project Structure

```
.
├── gitapp.py          # Main Python script
├── gitactivity.json   # Saved events data (created after running)
├── gitdetails.json    # Saved user details (created after running)
├── gitrepolist.json   # Saved repositories (created after running)
└── README.md          # This file
```

---

## ▶️ Usage

Run the app:

```bash
python gitapp.py <github-username>
```

Example:

```bash
python gitapp.py kamranahmedse
```

This will:

1. Fetch GitHub user details, events, and repositories
2. Save all raw data as JSON
3. Print a clean summary like:

```
=== GitHub Profile Summary ===
My name is Kamran Ahmed
I have 35k followers
I am following 10 people
Bio: Creator of roadmap.sh
My Twitter username: kamranahmedse

=== My GitHub Public Repositories ===
- developer-roadmap
- project-guidelines
...

=== Repositories with Stars & Languages ===
- developer-roadmap  ⭐  260k  (TypeScript)
...

=== Language Usage in Repositories ===
- TypeScript: 10 repo(s)
- JavaScript: 5 repo(s)
...
```

*(Numbers shown are just examples.)*

---

## 🔧 Customization Ideas

* Show top 3 starred repositories
* Display total stars across all repos
* Handle rate limits and add token authentication
* Generate charts (matplotlib) for languages or stars
* Build a Flask/FastAPI web UI

---

## ⚠️ Notes

* This project uses **rate-limited public endpoints** (60 requests/hour).
* For extended use, add a GitHub personal access token.
* Only **public** repository/activity data is used.
* No private data is accessed or stored.

---

## 👍 Credits

* Inspired by the **GitHub User Activity** project from Roadmap.sh
* Example profile used: **Kamran Ahmed** (public data only)


