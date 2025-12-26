from fastapi import FastAPI, HTTPException
import json
import os

file_path = os.path.join(os.getcwd(), "db.json")
full_db = {}


def file_check():
    return os.path.exists(file_path)


def is_empty():
    if not file_check():
        return True

    if os.path.getsize(file_path) == 0:
        return True

    try:
        with open(file_path, "r") as db:
            data = json.load(db)
            return not bool(data)
    except json.JSONDecodeError:
        return True


def load_db():
    global full_db

    if file_check() and not is_empty():
        with open(file_path, "r") as db:
            full_db = json.load(db)
    else:
        full_db = {"students": {}}
        with open(file_path, "w") as db:
            json.dump(full_db, db, indent=4)

    print("DB loaded:", full_db)


load_db()

app = FastAPI()


@app.get("/alldb")
def get_alldb():
    return full_db


@app.get("/alldb/{id}")
def get_student(id: str):
    student = full_db.get("students", id).get(id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="ID not found"
        )
    else:
        return student
