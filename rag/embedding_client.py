# """Embedding client for generating vector representations using GitHub Models"""
# import os
# import json
# import time
# import urllib.request
# import urllib.error
#
#
# class EmbeddingClient:
#     def __init__(self):
#         self.github_token = os.getenv("GITHUB_TOKEN")
#         endpoint = os.getenv("GITHUB_MODELS_ENDPOINT", "https://models.inference.ai.azure.com")
#
#         # Clean up the endpoint to ensure it hits the right v1/embeddings route
#         self.url = f"{endpoint.rstrip('/')}/embeddings"
#         self.model_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
#
#         print(f"💡 Embedding client initialized with GitHub Models ({self.model_name}) using direct HTTP protocol.")
#
#     def get_embedding(self, text: str):
#         """Generate a 1536-dimensional vector embedding for a given text snippet"""
#         if not text or not text.strip():
#             return [0.0] * 1536
#
#         text = text.replace("\n", " ").strip()
#
#         # Prepare headers and payload
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {self.github_token}"
#         }
#         data = json.dumps({
#             "input": [text],
#             "model": self.model_name
#         }).encode("utf-8")
#
#         max_retries = 5
#         delay = 1
#
#         for attempt in range(max_retries):
#             try:
#                 req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
#                 with urllib.request.urlopen(req) as response:
#                     res_body = json.loads(response.read().decode("utf-8"))
#                     return res_body["data"][0]["embedding"]
#
#             except urllib.error.HTTPError as e:
#                 # Catch actual server errors
#                 error_info = e.read().decode("utf-8") if e.fp else ""
#                 print(f"\n⚠️ HTTP Error {e.code} on attempt {attempt + 1}: {e.reason} - {error_info}")
#                 if attempt == max_retries - 1:
#                     return None
#
#             except Exception as e:
#                 # Catch general network hiccups
#                 print(f"\n⚠️ Network error on attempt {attempt + 1}: {e}")
#                 if attempt == max_retries - 1:
#                     return None
#
#             time.sleep(delay)
#             delay *= 2





# this above one works all fine, but im hitting github 15 per minute rate limits, so adding delay





#
# """Embedding client for generating vector representations using GitHub Models with Smart Rate-Limiting"""
# import os
# import json
# import time
# import urllib.request
# import urllib.error
#
#
# class EmbeddingClient:
#     def __init__(self):
#         self.github_token = os.getenv("GITHUB_TOKEN")
#         endpoint = os.getenv("GITHUB_MODELS_ENDPOINT", "https://models.inference.ai.azure.com")
#         self.url = f"{endpoint.rstrip('/')}/embeddings"
#         self.model_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
#         print(f"💡 Embedding client initialized with GitHub Models ({self.model_name}) using direct HTTP protocol.")
#
#     def get_embedding(self, text: str):
#         """Generate a 1536-dimensional vector embedding for a given text snippet with adaptive backoff"""
#         if not text or not text.strip():
#             return [0.0] * 1536
#
#         text = text.replace("\n", " ").strip()
#
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": f"Bearer {self.github_token}"
#         }
#         data = json.dumps({
#             "input": [text],
#             "model": self.model_name
#         }).encode("utf-8")
#
#         # Increase retries and use adaptive waiting for free tier limits
#         max_retries = 10
#         delay = 2
#
#         for attempt in range(max_retries):
#             try:
#                 req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
#                 with urllib.request.urlopen(req) as response:
#                     res_body = json.loads(response.read().decode("utf-8"))
#                     return res_body["data"][0]["embedding"]
#
#             except urllib.error.HTTPError as e:
#                 error_info = e.read().decode("utf-8") if e.fp else ""
#
#                 # Check if it is a Rate Limit (429) error
#                 if e.code == 429:
#                     print(
#                         f"\n⏳ Rate limit hit. GitHub says: 15 reqs/min max. Cooling down for {delay} seconds before retrying...")
#                     time.sleep(delay)
#                     # Dynamically step up the delay aggressively for 429s
#                     delay = max(delay * 2, 32)
#                     continue
#
#                 print(f"\n⚠️ HTTP Error {e.code} on attempt {attempt + 1}: {e.reason} - {error_info}")
#                 if attempt == max_retries - 1:
#                     return None
#
#             except Exception as e:
#                 print(f"\n⚠️ Network error on attempt {attempt + 1}: {e}")
#                 if attempt == max_retries - 1:
#                     return None
#
#             time.sleep(delay)
#
#         return None




# this  above also works fine, it added delay to the rate limits, but still wasnt worth it, so its a newer code


"""Embedding client for generating vector representations using GitHub Models"""
import os
import json
import time
import urllib.request
import urllib.error


class EmbeddingClient:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        endpoint = os.getenv("GITHUB_MODELS_ENDPOINT", "https://models.inference.ai.azure.com")
        self.url = f"{endpoint.rstrip('/')}/embeddings"
        self.model_name = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
        print(f"💡 Embedding client initialized with GitHub Models ({self.model_name}) using direct HTTP protocol.")

    def get_embedding(self, text: str):
        """Fallback for singular strings"""
        res = self.get_embeddings_batch([text])
        return res[0] if res else None

    def get_embeddings_batch(self, texts: list):
        """Generate 1536-dimensional vector embeddings for a list of strings in ONE single request"""
        if not texts:
            return []

        # Clean up text snippets safely
        cleaned_texts = [t.replace("\n", " ").strip() if t and t.strip() else " " for t in texts]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.github_token}"
        }
        data = json.dumps({
            "input": cleaned_texts,
            "model": self.model_name
        }).encode("utf-8")

        max_retries = 5
        delay = 5

        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req) as response:
                    res_body = json.loads(response.read().decode("utf-8"))
                    # Return all arrays from inside the server payload response
                    return [item["embedding"] for item in res_body["data"]]

            except urllib.error.HTTPError as e:
                error_info = e.read().decode("utf-8") if e.fp else ""
                if e.code == 429:
                    print(f"\n⏳ Rate limit hit inside batch. Pausing for {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2
                    continue
                print(f"\n⚠️ HTTP Error {e.code} on batch attempt {attempt + 1}: {e.reason} - {error_info}")

            except Exception as e:
                print(f"\n⚠️ Network error on batch attempt {attempt + 1}: {e}")

            time.sleep(delay)

        return None