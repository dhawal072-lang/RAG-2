export interface Document {
  document_id: number;
  filename: string;
  file_path?: string;
  sha256?: string;
  size_bytes?: number;
  status: "pending" | "processing" | "completed" | "failed";
  total_pages: number;
  total_chunks: number;
  error_message?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface DocumentSummary {
  document_id: number;
  filename: string;
  summary: string;
}

export interface CombinedSummary {
  document_ids: number[];
  summary: string;
  sources: DocumentSource[];
}

export interface DocumentSource {
  document_id: number;
  filename: string;
  page_number: number;
  chunk_id: number;
}