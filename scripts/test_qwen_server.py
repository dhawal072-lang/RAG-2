
from src.services.llm_service import LLMService


def main():
    llm = LLMService(
        mode="vllm",
        base_url="http://localhost:8000/v1",
        model="qwen-full"
    )

    prompt = """
You are a helpful AI assistant.

Explain three advantages of the Kotlin programming language.

Use a numbered list.
Keep your answer concise.
"""

    print("Testing actual Qwen generation...")
    print("Model:", llm.model)
    print("Server:", llm.base_url)

    try:
        answer = llm.generate(prompt)

        print("\nQWEN GENERATED ANSWER")
        print("=" * 50)
        print(answer)
        print("=" * 50)

    except Exception as error:
        print("Qwen generation failed:")
        print(type(error).__name__, str(error))


if __name__ == "__main__":
    main()
