import requests
import time

# Define the API endpoint and headers
API_URL = "http://20.244.32.168:8080/sensevoice/keyword-extract"
HEADERS = {
    'Content-Type': 'application/json',
    'API_KEY': 'slkfsdjfjsidsfjkenfnvcjnlsdkfj'
}

# Define the payload for the request
PAYLOAD = {
    "audio_transcription": """In the year 2456, Earth stands on the brink of collapse. After decades of war and environmental decay, the planet is a shadow of its former self. Governments have fallen, and humanity's last hope lies in the Cypher Program, a secret initiative led by the brilliant but mysterious Dr. Kairos. The project seeks to transcend the limitations of human biology by uploading human consciousness into highly advanced, bio-synthetic bodies capable of withstanding the harshest conditions of deep space. Dr. Kairos believes that the key to saving humanity lies not in preserving the human form, but in evolving it—melding mind and machine to create a new breed of human capable of surviving the galactic conflicts brewing beyond the solar system.

Elara, a troubled young woman with a criminal past, is selected as one of the first test subjects for the Cypher Program. Having been drawn into a life of rebellion and resistance against Earth's failing governments, she has little faith in any system, let alone one as controversial as Cypher. But when she awakens in a sleek, artificial body, she quickly realizes the stakes are far higher than she ever imagined. Her mind has been linked to a massive virtual network that controls Earth’s defenses, deep space exploration vessels, and even military satellites. At first, the powers at her disposal seem like a miracle—her body is enhanced, her senses amplified, and her strength limitless. She begins to feel a growing sense of power, one she’s never known before.

But as Elara begins to explore her new reality, she uncovers unsettling truths hidden within the network. Strange glitches start to manifest—distorted memories of past test subjects, voices that seem to speak from nowhere, and whispers from forgotten minds once trapped in the program. These aren’t mere anomalies; they are fragments of the consciousnesses of those who came before her—humans who were uploaded into the system and never returned. Elara learns that the Cypher Program has been plagued with failure, its previous participants having been lost in the digital void, their minds shattered or corrupted by the system’s imperfect technology.

As the mysterious force behind these disturbances grows stronger, Elara begins to lose track of where her mind ends and the voices of those trapped within the program begin. With each passing day, the line between her humanity and the artificial body she inhabits becomes more and more blurred. Desperate for answers, she confronts Dr. Kairos, only to learn that he has been hiding the most dangerous secret of all: the Cypher Program wasn’t just designed to save humanity—it was designed to create a new form of life, a hybrid race that would inherit Earth and beyond. Humanity, as it is known, would cease to exist.

With war on the horizon and her own identity disintegrating, Elara must navigate a complex web of deceit, ethical dilemmas, and the dark truth of the Cypher Program. As the final battle for control of the virtual network looms, she must make a choice: continue to fight for the survival of a species that may no longer be worthy of saving, or embrace the digital future that could reshape the very meaning of life itself. In a world where mind and machine merge, where does the human soul truly belong?""",
    
    "keywords": ["her", "network", "mind"],
    "language": "en"
}

def test_keyword_extract():
    """
    Function to test the Keyword Extraction API and measure response time.
    """
    try:
        # Record the start time
        start_time = time.time()

        # Send the POST request to the API
        response = requests.post(API_URL, json=PAYLOAD, headers=HEADERS)

        # Record the end time
        end_time = time.time()

        # Calculate the response time
        response_time = end_time - start_time

        # Print the response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time:.4f} seconds")
        print(f"Response Body: {response.json()}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Run the test function
    test_keyword_extract()