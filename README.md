# Universal Format Converter API

A clean, extensible Python Web API built with **FastAPI** for converting files between various formats. It employs a **Factory Method pattern** allowing developers to register new conversion formats without modifying core business logic.

---

## 🚀 Key Features

* **Polymorphic Entrypoint:** Use a single endpoint to convert files by specifying `source_format` and `target_format`.
* **Dedicated Testing Endpoints:** Specific endpoints for ease of testing in Swagger UI.
* **History Tracking:** Logs all conversions (success, failure, and error messages) in a local database.
* **Extensible Design:** Easily introduce new file converters by inheriting from `BaseConverter` and registering them in the factory.
* **Clean Architecture:** Standardized layout decoupling controllers, services, database layers, and factory definitions.

---

## 🛠️ Tech Stack

* **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) & [Uvicorn](https://www.uvicorn.org/)
* **Database & ORM:** SQLite with [SQLAlchemy](https://www.sqlalchemy.org/)
* **Data & Format Processing:**
  * **Excel / CSV:** [Pandas](https://pandas.pydata.org/) & [openpyxl](https://openpyxl.readthedocs.io/)
  * **PDF Parsing:** [pdfplumber](https://github.com/jsvine/pdfplumber)
  * **XML Parsing & Generation:** [xmltodict](https://github.com/martinblech/xmltodict) & [dicttoxml](https://github.com/quandyfactory/dicttoxml)

---

## 📁 Directory Structure

```
format_converter_api/
├── main.py                # App entrypoint & FastAPI initialization
├── requirements.txt       # Dependencies
├── converter.db           # SQLite Database (auto-created on run)
├── uploads/               # Temporary storage for uploaded raw files (auto-created)
├── outputs/               # Temporary storage for converted output files (auto-created)
│
├── controllers/
│   └── converter_controller.py  # API Routers & request handlers
│
├── converters/
│   ├── base_converter.py        # Abstract base class for converters
│   ├── csv_to_json_converter.py
│   ├── excel_to_json_converter.py
│   ├── json_to_excel_converter.py
│   ├── json_to_xml_converter.py
│   ├── pdf_to_txt_converter.py
│   └── xml_to_json_converter.py
│
├── database/
│   └── db.py                    # SQLite connection, Session setup & history schema
│
├── factory/
│   └── converter_factory.py     # Registry / factory resolving converter implementations
│
└── services/
    ├── converter_service.py     # Handles file management & conversion orchestration
    └── history_service.py       # Reads/writes database logs
```

---

## ⚙️ Supported Conversions

| Source Format | Target Format | Extension | Notes |
| :--- | :--- | :--- | :--- |
| **CSV** | **JSON** | `.csv` ➡️ `.json` | Converts tabular records to array of JSON objects. |
| **Excel** | **JSON** | `.xlsx` / `.xls` ➡️ `.json` | Reads sheet data and converts to JSON. |
| **JSON** | **Excel** | `.json` ➡️ `.xlsx` | Writes structured array of objects to Excel format. |
| **JSON** | **XML** | `.json` ➡️ `.xml` | Serializes JSON key/values to XML structure. |
| **XML** | **JSON** | `.xml` ➡️ `.json` | Deserializes XML nodes back into standard JSON. |
| **PDF** | **TXT** | `.pdf` ➡️ `.txt` | Extracts raw text from all PDF pages. |

---

## ⚙️ Setup and Installation

### Prerequisites
* Python 3.8 or higher.

### 1. Set Up Virtual Environment

In your terminal (from the project directory `format_converter_api`):

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Activate on macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Application

Start the local development server:

```bash
uvicorn main:app --reload
```

* **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Alternative API docs (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Reference

### 1. General Convert Endpoint
Routes to the correct converter dynamically based on form parameters.

* **Path:** `POST /api/convert`
* **Content-Type:** `multipart/form-data`
* **Request Body:**
  * `source_format` (string, required): e.g., `"csv"`, `"json"`, `"pdf"`, `"xml"`, `"excel"`
  * `target_format` (string, required): e.g., `"json"`, `"excel"`, `"txt"`, `"xml"`
  * `file` (binary file, required): The file to convert
  * `user_id` (integer, optional): Associated user identifier
* **Response:** Returns the converted file stream as a download.

### 2. Dedicated Endpoints (for easier manual / Swagger testing)
Each accepts `file` and optional `user_id`, returning the converted file as a download response.

* `POST /api/convert/csv-to-json`
* `POST /api/convert/json-to-excel`
* `POST /api/convert/excel-to-json`
* `POST /api/convert/pdf-to-txt`
* `POST /api/convert/xml-to-json`
* `POST /api/convert/json-to-xml`

### 3. Retrieve Conversion Logs
* **Path:** `GET /api/convert/history`
* **Query Parameters:**
  * `limit` (integer, default `100`): Maximum history logs to retrieve
* **Response:** `application/json` (list of history records with timestamps, statuses, and file names).

---

## 🛠️ How to Add a New Converter

Adding a new conversion format does not require modifying any services or controllers. 

1. **Create the Converter class:**
   In [converters/](file:///c:/Users/Intern/format_converter_api/converters), create a new python file subclassing [BaseConverter](file:///c:/Users/Intern/format_converter_api/converters/base_converter.py):
   ```python
   # converters/txt_to_pdf_converter.py
   from converters.base_converter import BaseConverter
   
   class TxtToPdfConverter(BaseConverter):
       source_format = "txt"
       target_format = "pdf"
       
       def convert(self, input_path: str, output_path: str) -> str:
           # Read input_path text and write to output_path PDF
           ...
           return output_path
   ```
2. **Register it in the Factory:**
   Open [factory/converter_factory.py](file:///c:/Users/Intern/format_converter_api/factory/converter_factory.py), import your class and register it:
   ```python
   from converters.txt_to_pdf_converter import TxtToPdfConverter

   # Add it to the self.converters dictionary inside __init__():
   self.converters = {
       ...
       "txt_to_pdf": TxtToPdfConverter(),
   }
   ```
3. **Verify:**
   Restart your FastAPI server. The general endpoint `POST /api/convert` will now automatically support converting `txt` to `pdf`.
