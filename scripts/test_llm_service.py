
from src.services.llm_service import LLMService


def main():
    llm = LLMService(mode="mock")

    response = llm.generate(
        "Explain Kotlin programming."
    )

    print("LLM mode: mock")
    print("Response:")
    print(response)


if __name__ == "__main__":
    main()
