
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.services.summary_service import SummaryService
from src.services.combined_summary_service import CombinedSummaryService


router = APIRouter()

summary_service = SummaryService()
combined_summary_service = CombinedSummaryService()


class CombinedSummaryRequest(BaseModel):
    document_ids: list[int] = Field(min_length=1)
    top_k: int = Field(default=20, ge=1, le=50)


@router.get("/{document_id}/summary")
def get_document_summary(document_id: int):

    if document_id < 1:
        raise HTTPException(
            status_code=400,
            detail="Document ID must be positive."
        )

    summary = summary_service.get_summary(document_id)

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Summary not found for this document."
        )

    return summary


@router.post("/combined-summary")
def generate_combined_summary(request: CombinedSummaryRequest):

    try:
        result = combined_summary_service.generate_combined_summary(
            document_ids=request.document_ids,
            top_k=request.top_k
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate combined summary."
        )
