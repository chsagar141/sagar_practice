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


@app.get("/alldb/{id}/marks")
def get_marks(id: str):
    student = full_db.get("students", {}).get(id)
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Id not found"
        )
    m1 = student.get("mark1", 0)
    m2 = student.get("mark2", 0)
    m3 = student.get("mark3", 0)
    return {
        "m1": m1,
        "m2": m2,
        "m3": m3,
        "full_m123": m1 + m2 + m3
    }


@app.get("/topers")
def top_std(limit: int = 3):
    student = full_db.get("students", {})
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )
    ranked = []

    for sid, student in student.items():
        total = (
            student.get("mark1", 0) +
            student.get("mark2", 0) +
            student.get("mark3", 0)
        )
        ranked.append({
            "id": sid,
            "name": student.get("name"),
            "student_id": student.get("student_id"),
            "total_marks": total
        })
    ranked.sort(key=lambda x: x["total_marks"], reverse=True)
    return ranked[:limit]
