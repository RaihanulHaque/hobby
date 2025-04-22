from locust import HttpUser, TaskSet, task, between

class KeywordExtractTasks(TaskSet):
    @task
    def test_keyword_extract(self):
        headers = {
            'Content-Type': 'application/json',
            'API_KEY': 'slkfsdjfjsidsfjkenfnvcjnlsdkfj'
        }
        payload = {
            "audio_transcription": "This is a sample audio transcription.",
            "keywords": ["her", "network", "mind"],
            "language": "en"
        }
        self.client.post(
            "http://20.244.32.168:8080/sensevoice/keyword-extract",
            json=payload,
            headers=headers,
            name="Keyword Extract"
        )

class KeywordExtractUser(HttpUser):
    tasks = [KeywordExtractTasks]
    wait_time = between(1, 5)  # Simulate users waiting between 1 and 5 seconds
    host = "http://20.244.32.168:8080"