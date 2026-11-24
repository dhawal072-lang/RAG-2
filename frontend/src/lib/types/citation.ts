export interface Citation {
  citation_id: number;
  reference: string;
  document_id: number;
  filename: string;
  page_number: number;
  chunk_id: number;
  text: string;
  score: number | null;
}