from locust import HttpUser, task, between
import json

class LoginUser(HttpUser):
    # Define the base URL (host) for your API
    host = "https://nihalbaigtest.site"  # Your API host URL
    # Define the wait time between tasks (this simulates real-world pacing between requests)
    wait_time = between(1, 3)  # Random wait time between 1 to 3 seconds
    
    @task
    def login(self):
        """Function to send a POST request to the login API."""
        url = "/v1/auth/login"  # The login endpoint URL (relative path)
        
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        payload = {
            "email": "raihanulhaque007@gmail.com",
            "password": "Sa1tama_"
        }
        
        try:
            # Send POST request with JSON payload
            response = self.client.post(url, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 200:
                print(f"Login Success: {response.json().get('success')}")
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")

    def on_start(self):
        """This is run when a simulated user starts."""
        print("Starting the Locust test")

