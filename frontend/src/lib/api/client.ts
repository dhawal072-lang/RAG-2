
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type RequestOptions = {
  timeout?: number;
};

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  config: RequestOptions = {}
): Promise<T> {
  const controller = new AbortController();

  const timeout = setTimeout(
    () => controller.abort(),
    config.timeout ?? 30000
  );

  try {
    const response = await fetch(
      `${API_BASE_URL}${endpoint}`,
      {
        ...options,
        signal: controller.signal,
        headers: {
          ...(options.body instanceof FormData
            ? {}
            : { "Content-Type": "application/json" }),
          ...options.headers,
        },
      }
    );

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const message =
        data?.detail ||
        `API request failed (${response.status})`;

      throw new ApiError(message, response.status);
    }

    return data as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    if (error instanceof Error && error.name === "AbortError") {
      throw new Error("The request timed out. Please try again.");
    }

    throw new Error(
      "Unable to connect to the Document Intelligence API."
    );
  } finally {
    clearTimeout(timeout);
  }
}
