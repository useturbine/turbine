import requests
import tiktoken
import json


class OpenAIClient:
    EncodingName = "cl100k_base"
    EmbeddingEndpoint = "https://api.openai.com/v1/embeddings"

    APIKey = ""
    ActiveModel = "text-embedding-ada-002"

    @staticmethod
    def get_embedding(text: str) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OpenAIClient.APIKey}"
        }

        response = requests.post(
            OpenAIClient.EmbeddingEndpoint,
            headers=headers,
            data=json.dumps({
            "input": text,
            "model": OpenAIClient.ActiveModel
        }))
        if response.status_code != 200:
            raise Exception(f"Error in API call: {response.text}")

        return response.json().get("data", {}).get("embedding", [])

    @staticmethod
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(string))