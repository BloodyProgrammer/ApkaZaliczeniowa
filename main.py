from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from PIL import Image, ImageOps
from starlette.responses import StreamingResponse
import cv2
import io
import numpy as np
from io import BytesIO, StringIO
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
async def create_upload_file(file: UploadFile = File(...)):

    if not file:
        return {"message": "No upload file sent"}
    else:
        buffer = BytesIO()
        buffer.write(open(file, 'rb').read())
        buffer.seek(0)

        image = Image.open(buffer)
        print(image)
        # with open(file, 'b') as f:
        #     img = Image.open(file)
        #     object = await file.read()
        #     img = Image.open(object)
        #     # im_invert = ImageOps.invert(img)
        #     # nparr = np.fromstring(file, np.uint8)
        #     # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #     # img_not = cv2.bitwise_not(img)
        #     # _, encoded_img = cv2.imencode('.JPG', img_not)
        #
        #     buffer = BytesIO()
        #     img.save(buffer, format="JPEG")
        #     img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        #     img_not = cv2.bitwise_not(img)
        #     _, encoded_img = cv2.imencode('.JPG', img_not)
        #     return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpg")
        #     # return StreamingResponse(io.BytesIO(img.tobytes()), media_type="image/jpg")


# io.BytesIO(inverted_img.tobytes())
security = HTTPBasic()
@app.get("/date")
def date(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"12345"
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