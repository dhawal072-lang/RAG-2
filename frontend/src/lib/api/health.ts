
import { apiRequest } from "./client";

export interface HealthResponse {
  status: string;
  application: string;
}

export async function checkApiHealth(): Promise<HealthResponse> {
  return apiRequest<HealthResponse>("/health", {
    method: "GET",
  });
}
