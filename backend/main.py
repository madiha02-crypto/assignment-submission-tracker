from fastapi import FastAPI ,HTTPException

import function
from datetime import datetime
app = FastAPI(
    title="assignment submission  tracker API"
)


@app.get("/assigments/{course}")
def get_all_assigments(course=None,):
    if course == "":
        raise HTTPException(status_code=404, detail="not found")
    if course not in function.Course: 
        raise HTTPException(status_code=409, detail="invalid category")
    return function.filter_course(course=course)