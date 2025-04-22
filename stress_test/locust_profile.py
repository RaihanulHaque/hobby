from locust import HttpUser, TaskSet, task, between
import os

access_token = os.getenv("ACCESS_TOKEN")

class ProfileViewTasks(TaskSet):
    access_token = None

    @task
    def test_profile_view(self):
        headers = {"Authorization": f"Bearer {access_token}"}
        self.client.get("/v1/user/me", headers=headers, name="Profile View")

class ProfileViewUser(HttpUser):
    tasks = [ProfileViewTasks]
    wait_time = between(1, 5)  # Simulate users waiting between 1 and 5 seconds
    host = "https://nihalbaigtest.site"  # Base URL for the profile view API