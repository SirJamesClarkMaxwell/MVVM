
# 🧪 Python MVP ImGui Template

A modern, minimal Python MVP (Model-View-Presenter) application template using
[imgui_bundle](https://github.com/pthom/imgui_bundle) for GUI rendering.

---

## 🚀 Features

- ✨ Clean MVP architecture
- 📊 Example: interactive calculator panel
- 🔍 Data modeling with [`dataclass`](https://www.attrs.org/)
- 🧵 Background processing with thread pool
- 📁 File dialog and CSV support
- 🧱 ImGui docking and multi-panel layout
- 📂 Project loading via project specification file  
- ⚙️ Context manager  
- 💾 Saving and loading UI layout  

---

## 🧰 Requirements

- Python ≥ 3.9
- Recommended: use a virtual environment (uv)
---
After you clone the repository and go to it, you should write:
```bash
uv venv
uv venv exec
```

Install dependencies:

```bash
pip install -r requirements.txt
```
---

## ▶️ Running the App

```bash
python main.py
```

Make sure you're in the project root directory, and the virtual environment (if any) is activated.

---

## 📦 Project Structure

```
.
├── app.py                   # App manager & setup
├── main.py                  # App entry point
├── data/                    # Holds global data
├── models/                  # Business logic
├── presenters/              # binds panel and logic
├── views/
├── utils/
│   ├── file_dialog.py       # File dialog controller
│   ├── logger.py            # Logging wrapper
│   └── thread_pool.py       # Async task management
```

---

## 🧪 Calculator Panel

An example panel that supports:
- Float inputs (`a`, `b`)
- Operator selection (`+`, `-`, `*`, `/`, `^`)
- Live computation via ViewModel
- CSV loading capability

---

## 🛠️ Extending the Template

To add a new module:

1. Create a data model in `data/`
2. Implement business logic in `models/`
3. Write a ViewModel in `viewmodels/`
4. Create a Panel view in `views/`
5. Register it inside `App.setup_panels()`

---

## 🧠 Design Philosophy

- Separation of concerns (MVP)
- Easy to extend with new panels
- Async-safe design
- Clean and modular Python

---

## 👨‍💻 Author

Built by [SirJamesClarkMaxwell](https://github.com/SirJamesClarkMaxwell)

