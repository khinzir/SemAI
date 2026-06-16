"""
LLM Client with streaming support and model fallback
"""
import os
import requests
import json
from typing import List, Dict, Any, Generator

class LLMClient:
    def __init__(self):
        # GitHub Models (Free)
        self.github_endpoint = "https://models.inference.ai.azure.com"
        self.github_token = os.getenv("GITHUB_TOKEN")

        # Azure OpenAI (Premium)
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_key = os.getenv("AZURE_OPENAI_KEY")
        self.azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

        self.use_github = bool(self.github_token)
        self.use_azure = bool(self.azure_endpoint and self.azure_key)

        if not self.use_github and not self.use_azure:
            print("⚠️ No LLM configuration found. Using mock responses.")

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Non-streaming chat (for simple responses)"""
        if self.use_github:
            return self._github_chat(messages, temperature)
        elif self.use_azure:
            return self._azure_chat(messages, temperature)
        else:
            return self._mock_chat(messages)

    def chat_stream(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> Generator:
        """Streaming chat response"""
        if self.use_github:
            yield from self._github_chat_stream(messages, temperature)
        elif self.use_azure:
            yield from self._azure_chat_stream(messages, temperature)
        else:
            yield self._mock_chat(messages)

    def _github_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """Non-streaming GitHub Models call"""
        url = f"{self.github_endpoint}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"⚠️ Error: {response.status_code}\nPlease try again."
        except Exception as e:
            return f"⚠️ Connection error: {str(e)}"

    def _github_chat_stream(self, messages: List[Dict[str, str]], temperature: float) -> Generator:
        """Streaming chat with GitHub Models"""
        url = f"{self.github_endpoint}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000,
            "stream": True
        }

        try:
            response = requests.post(url, headers=headers, json=payload, stream=True, timeout=60)

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        try:
                            data = json.loads(line[6:])
                            if 'choices' in data and data['choices'][0].get('delta', {}).get('content'):
                                yield data['choices'][0]['delta']['content']
                        except:
                            continue
        except Exception as e:
            yield f"⚠️ Error: {str(e)}"

    def _azure_chat(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """Azure OpenAI call (premium)"""
        # Implement when Azure OpenAI is configured
        return "Premium Azure OpenAI not configured. Please check your .env file."

    def _azure_chat_stream(self, messages: List[Dict[str, str]], temperature: float) -> Generator:
        """Azure OpenAI streaming"""
        yield "Premium streaming not configured."

    def _mock_chat(self, messages: List[Dict[str, str]]) -> str:
        """Mock response for testing"""
        return """🤖 **CSIT Guru Assistant**

I'm currently in demo mode. To get real AI responses:

1. **Free Option:** Get a GitHub token from https://github.com/settings/tokens
2. **Premium Option:** Configure Azure OpenAI in your .env file

Once configured, I'll provide intelligent answers based on your CSIT textbooks! 📚"""