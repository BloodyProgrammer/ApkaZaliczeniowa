from locust import HttpUser, task, between
import random


class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def number(self):
        number  = 2115
        self.client.get(f"/number/{number}")
        number  = -2115
        self.client.get(f"/number/{number}")
        number = 9223372036854775807
        self.client.get(f"/number/{number}")
        number = 9223372036854775808
        self.client.get(f"/number/{number}")
        self.client.get("/number/pies")

    # @task
    # def picture_invert(self):
    #     url = '/picture/invert'
    #     with open('C:/Users/Dell/Desktop/FaceID/train/unknown.1(1).jpg', 'rb') as image:
    #         files = {'file': ('img.jpg', image, 'image/jpeg', {'Content-Type': 'multipart/form-data'})}
    #         self.client.request('POST', url, files=files)

    # @task
    # def auth(self):
    #    self.client.get("/auth", auth=("admin", "12345"))
