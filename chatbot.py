import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="featherless-ai",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message)
