import type { Citation } from "./citation";

export interface ChatRequest {
  question: string;
  top_k?: number;
  document_ids?: number[];
}

export interface ChatResponse {
  question: string;
  selected_document_ids: number[] | null;
  answer: string;
  sources: Citation[];
}