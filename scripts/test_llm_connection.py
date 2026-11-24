
from src.services.llm_service import LLMService


def main():
    llm = LLMService()

    print("LLM Configuration")
    print("-----------------")
    print("Mode:", llm.mode)
    print("Base URL:", llm.base_url)
    print("Model:", llm.model)

    print("\nTesting LLM generation...")

    try:
        response = llm.generate(
            "Reply with exactly: QWEN CONNECTION TEST SUCCESSFUL"
        )

        print("\nLLM Response:")
        print(response)

    except Exception as error:
        print("\nLLM connection failed:")
        print(type(error).__name__, str(error))


if __name__ == "__main__":
    main()
