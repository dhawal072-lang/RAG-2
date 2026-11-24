
import os
import requests

from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(
        self,
        mode=None,
        base_url=None,
        model=None,
        temperature=None,
        max_tokens=None,
        timeout=None
    ):
        self.mode = mode or os.getenv("LLM_MODE", "mock")

        self.base_url = (
            base_url or os.getenv(
                "LLM_BASE_URL",
                "http://localhost:8000/v1"
            )
        ).rstrip("/")

        self.model = model or os.getenv("LLM_MODEL", "qwen-full")

        self.temperature = float(
            temperature if temperature is not None
            else os.getenv("LLM_TEMPERATURE", "0.2")
        )

        self.max_tokens = int(
            max_tokens if max_tokens is not None
            else os.getenv("LLM_MAX_TOKENS", "1500")
        )

        self.timeout = int(
            timeout if timeout is not None
            else os.getenv("LLM_TIMEOUT", "120")
        )

        if self.mode not in ("mock", "vllm"):
            raise ValueError(f"Unsupported LLM mode: {self.mode}")

    def generate(self, prompt: str):

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if self.mode == "mock":
            return (
                "MOCK RESPONSE: The question was received "
                "successfully. Document context was retrieved "
                "and prepared for language-model processing."
            )

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens
                },
                timeout=self.timeout
            )

            response.raise_for_status()

            result = response.json()

            answer = result["choices"][0]["message"]["content"]

            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("The LLM returned an empty response.")

            return answer

        except requests.Timeout as error:
            raise RuntimeError("The LLM server request timed out.") from error

        except requests.RequestException as error:
            raise RuntimeError(
                f"Could not communicate with the LLM server: {error}"
            ) from error

        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError(
                "The LLM server returned an unexpected response."
            ) from error
