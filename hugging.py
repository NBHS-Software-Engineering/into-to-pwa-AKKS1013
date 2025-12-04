import requests

def tag(inputs, tags):
    f = open("/home/arun/.cache/huggingface/token")
    token = f.read()

    API_URL = (
        "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
    )
    headers = {"Authorization": f"Bearer {token}"}

    def query(payload):
        print("Progressing")
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query(
        {
            "inputs": inputs,
            "parameters": {"candidate_labels": tags},
        }
    )
    return output[0]
