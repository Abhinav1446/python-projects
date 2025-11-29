

# 📌 **Task Manager CLI (Python)**

A simple command-line task management application built using Python.
You can **add, delete, update, list, and mark tasks** with statuses like *to-do*, *in-progress*, and *done*.
All tasks are saved in a **JSON file**.

---

## ✨ **Features**

✔ Add tasks

✔ Delete tasks

✔ Update task names

✔ List all tasks

✔ List tasks by status

✔ Mark tasks as in-progress

✔ Mark tasks as done

✔ Automatically stores tasks in `tasklist.json`

✔ Timestamps for created/updated time

---

## 🛠 **Tech Used**

* Python (sys, os, json)
* datetime for timestamps
* JSON file for data storage

---

## 📂 **Project Structure**

```
project/
│
├── tasklist.json        # Auto-created JSON file
├── app.py               # Main application
└── README.md            # Documentation
```

---

## 🚀 **How to Run the Program**

### **1. Open terminal and navigate to the project folder**

```
cd project-folder
```

### **2. Run the script**

Use:

```
python app.py <command> [arguments]
```

---

## 📝 **Available Commands**

### 🔹 **Add a Task**

```
python app.py add "Buy groceries"
```

### 🔹 **Delete a Task**

```
python app.py delete <taskid>
```

### 🔹 **Update a Task**

```
python app.py update <taskid> "New task name"
```

### 🔹 **List All Tasks**

```
python app.py list
```

### 🔹 **List Tasks by Status**

```
python app.py list to-do
python app.py list in-progress
python app.py list done
```

### 🔹 **Mark Task as In-Progress**

```
python app.py mark-in-progress <taskid>
```

### 🔹 **Mark Task as Done**

```
python app.py mark-done <taskid>
```

---

## 📁 **How Tasks Are Stored**

A JSON file (`tasklist.json`) will look like this:

```json
[
    {
        "id": 1,
        "name": "Buy groceries",
        "status": "to-do",
        "created_on": "2025-01-28T15:10:12.123456",
        "updated_on": "2025-01-28T15:10:12.123456"
    }
]
```

---

## 🧠 How It Works (Brief Explanation)

* When the program starts, it loads or creates `tasklist.json`.
* All tasks are stored as dictionaries inside a list in memory.
* After every change (add/delete/update), the file is rewritten.
* Timestamps track when tasks were created and updated.

---

## 🙌 **Future Improvements (optional section)**

You can add this if you plan to upgrade later:

* Pretty table output
* Color-coded statuses
* Task priority
* Due dates
* Search tasks
* Convert to FastAPI or Flask API
* Add unit tests

---




