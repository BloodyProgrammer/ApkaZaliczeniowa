from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import StreamingResponse
import cv2
import io
import numpy as np
import datetime
import secrets
import os



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/number/{number}")
async def get_number(number: int):

    flag = False

    if number > 1:
        for i in range(2, number):
            if (number % i) == 0:
                flag = True
                break


    if flag:
        text = f"{number}, nie jest liczbą pierwszą"
        return text
    else:
        text = f"{number}, jest liczbą pierwszą"
        return text



@app.post("/picture/invert")
async def create_upload_file(file: bytes = File(...)):

    if not file:
        return {"message": "No upload file sent"}
    else:
            file_byted = np.fromstring(file, np.uint8)
            img = cv2.imdecode(file_byted, cv2.IMREAD_COLOR)
            img_inverted = cv2.bitwise_not(img)
            _, encoded_img = cv2.imencode('.PNG', img_inverted)
            return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")


security = HTTPBasic()
@app.get("/date")
def date(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(os.environ.get("USER"), 'utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(os.environ.get("PASSWORD"), 'utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return datetime.date.today()
