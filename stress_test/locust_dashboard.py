from locust import HttpUser, TaskSet, task, between
import requests
import os

access_token = os.getenv("ACCESS_TOKEN")

class DashboardTasks(TaskSet):
    access_token = None

    # def on_start(self):
    #     """Login and retrieve access token before starting tasks."""
    #     login_payload = {
    #         "email": "raihanulhaque007@gmail.com",
    #         "password": "Sa1tama_"
    #     }
    #     response = self.client.post("/v1/auth/login", json=login_payload)
    #     if response.status_code == 200:
    #         self.access_token = response.json().get("data", {}).get("accessToken")
    #     else:
    #         raise Exception("Failed to login and retrieve access token.")

    @task
    def test_dashboard(self):
        headers = {"Authorization": f"Bearer {access_token}"}
        self.client.get("/v1/projects/", headers=headers, name="Dashboard")

class DashboardUser(HttpUser):
    tasks = [DashboardTasks]
    wait_time = between(1, 5)  # Simulate users waiting between 1 and 5 seconds
    host = "https://nihalbaigtest.site"  # Base URL for the dashboard API


