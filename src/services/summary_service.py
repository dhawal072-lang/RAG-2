import json
from pathlib import Path

from src.services.llm_service import LLMService


SUMMARY_DIRECTORY = Path("data/summaries")


class SummaryService:
    def __init__(self):
        self.llm_service = LLMService()
        SUMMARY_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def get_summary_path(self, document_id: int) -> Path:
        return SUMMARY_DIRECTORY / f"{document_id}.json"

    def get_summary(self, document_id: int):
        summary_path = self.get_summary_path(document_id)

        if not summary_path.exists():
            return None

        with summary_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def generate_summary(self, document_id: int, filename: str, chunks: list[dict]):
        existing_summary = self.get_summary(document_id)

        if existing_summary:
            return existing_summary

        document_text = "\n\n".join(
            chunk["text"] for chunk in chunks
        )

        prompt = f"""
Create a clear and structured summary of this PDF.

Include:
1. Main topic
2. Key points
3. Important findings
4. Applications or use cases
5. Conclusion

PDF:
{filename}

Content:
{document_text}
"""

        summary_text = self.llm_service.generate(prompt)

        summary_data = {
            "document_id": document_id,
            "filename": filename,
            "summary": summary_text
        }

        summary_path = self.get_summary_path(document_id)

        with summary_path.open("w", encoding="utf-8") as file:
            json.dump(summary_data, file, indent=4, ensure_ascii=False)

        return summary_data