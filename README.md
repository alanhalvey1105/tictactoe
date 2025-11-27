# 🎮 Tic-Tac-Toe API (FastAPI + PostgreSQL)

A simple, modern **Tic-Tac-Toe backend API** built using **FastAPI**, **PostgreSQL**, and **async database operations**.  
Includes clean project structure, automated tests with **pytest**, and easy setup instructions for local development.

---

## 📘 Project Overview

This project provides a backend API for creating and playing Tic-Tac-Toe games.  
It supports:

- Creating a new game
- Joining an existing game
- Making moves
- Tracking game state
- Determining the winner
- Persistent storage using PostgreSQL

The API is lightweight, fast, asynchronous, and fully documented using FastAPI's built-in OpenAPI support.

---

## Features

- **FastAPI** for high-performance async APIs  
- **PostgreSQL** database with JSON storage for the game board  
- **Pytest** integration for API testing  
- **Automatic OpenAPI documentation**      

---

## Tech Stack

| Component | Technology |
|----------|------------|
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM / DB Layer | async PostgreSQL driver |
| Testing | pytest + httpx |
| Documentation | Swagger UI |
| Language | Python 3 |

---

---

## Setup & Installation

Follow these steps to run the project locally on Linux(Ubuntu):

---


### 1.Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

```

### 2.Install Dependencies

```bash
pip install -r requirements.txt

```

### 3.Start PostgreSQL(Local)

```bash
sudo service postgresql start


```
### 4.Copy the file **.env.example** and create a new file named **.env**

```bash
cp .env.example .env


```
### 5.Run FastAPI Server

```bash
uvicorn app.main:app --reload


```

### 6.Start Tic-Tac-Toe game

```bash

http://localhost:8000/static/index.html


```
---

## API Documentation

### Swagger UI

```bash

http://localhost:8000/docs


```
---

## Project Folder Structure

Below is the recommended structure for this FastAPI + PostgreSQL project:

```bash
├── app
│   ├── static/               # Frontend files
│   │   └── index.html        # UI for Tic-Tac-Toe
│   │
│   ├── db.py                 # Database connection + initialization
│   ├── logic.py              # Core Tic-Tac-Toe logic (moves, winners)
│   ├── main.py               # FastAPI application & routes
│   ├── schemas.py            # Pydantic request/response models
│
├── tests/
│   ├── test_api.py           # API endpoint tests
│   ├── test_logic.py         # Unit tests for game logic
│
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Project dependencies
├── .gitignore                # Git ignored files
├── README.md                 # Project documentation
```
---
---

## Run Test

```bash
pytest
```
---
