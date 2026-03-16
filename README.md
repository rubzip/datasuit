# 📊 Pandas-Visual-Flow: No-Code Data Suite

An intuitive, web-based graphical interface for data manipulation, powered by **FastAPI** and **Pandas**. This project bridges the gap between complex Python data wrangling and accessible user experiences.

---

## 🎯 Project Overview
**Pandas-Visual-Flow** is a local-first full-stack application designed for users who need the power of the `pandas` library without writing a single line of code. It allows for seamless data uploading, real-time transformation, and instant visualization of tabular datasets.

### 🚩 The Problem
Modern data tasks are robust but have a high barrier to entry. Non-programmers often struggle with Python syntax, while existing GUI tools are either too simple or overly expensive enterprise solutions.

### ✅ The Solution
A lightweight, local web suite that leverages:
* **FastAPI** for high-performance, asynchronous data processing.
* **Pandas** for industrial-grade data manipulation.
* **Modern Frontend (React/Tailwind)** for a reactive, "live-preview" experience.

---

## 🚀 Core Features & Goals

### 1. Data Ingestion & Export
* **Multi-format Support:** Upload datasets in `.csv` and `.xlsx` formats.
* **Safe Export:** Download your cleaned and manipulated data back to your local machine.

### 2. No-Code Manipulation Tools
* **Smart Filtering:** Apply complex queries (e.g., `Price > 100 & Category == 'Tech'`) via a simple UI.
* **Column Operations:** Rename, drop, or change data types with a click.
* **Data Cleaning:** Instant removal of null values (NaN) and duplicates.
* **Sorting & Selection:** Reorder and slice data dynamically.

### 3. Real-time Feedback
* **Live Preview:** See a 50-row "Instant Preview" of your DataFrame after every transformation.
* **Data Health Dashboard:** Automatic calculation of statistics ($mean$, $std$, $null\_counts$) and schema detection.

### 4. Developer & Technical Goals (The "Under the Hood")
* **Auto-Documentation:** Fully interactive API docs via Swagger (`/docs`).
* **Pydantic Validation:** Strict data validation for all transformation requests.
* **Stateless Processing:** Efficient memory management for handling large files in a local environment.

---

## 🛠️ Tech Stack
* **Backend:** Python 3.10+, FastAPI, Pandas, Uvicorn, Pydantic.
* **Frontend:** React.js (planned), Tailwind CSS, Axios.
* **Development:** Local environment (No deployment/No Auth for MVP focus).

---

## 📈 Roadmap
- [ ] **Phase 1:** Backend Setup & File Upload/Preview Endpoints.
- [ ] **Phase 2:** Implementation of core transformation logic (Filter/Sort/Drop).
- [ ] **Phase 3:** Frontend Development & API Integration.
- [ ] **Phase 4:** Advanced Features (Undo/Redo History & Basic Plotting).
