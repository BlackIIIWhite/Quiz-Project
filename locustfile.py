# from locust import HttpUser, task, between

# class WebsiteUser(HttpUser):
#     wait_time = between(1, 5)

#     @task
#     def load_home_page(self):
#         self.client.get("/")
    
#     def on_start(self):
#         # Disable SSL cert verification
#         self.client.verify = False


#     # @task
#     # def login(self):
#     #     self.client.post("/login/", {
#     #         "email": "agrahariamitindus485@gmail.com",
#     #         "password": "Amit"
#     #     })

from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def login(self):
        self.client.post("/login/", data={
            "email": "agrahariamitindus45@gmail.com",
            "password": "Amit"
        })

    def on_start(self):
        self.client.verify = False
