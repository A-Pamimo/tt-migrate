import {
  AnalyzeRequest,
  AnalysisResult,
  RefactorRequest,
  RefactorStreamEvent,
  ExportRequest,
  ApiError,
} from "./types";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  setBaseUrl(url: string) {
    this.baseUrl = url;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      let detail = `Request failed with status ${response.status}`;
      try {
        const errorBody = await response.json();
        detail = errorBody.detail || detail;
      } catch {
        // ignore parse error
      }
      const error: ApiError = { detail, status: response.status };
      throw error;
    }

    return response.json();
  }

  async analyze(code: string): Promise<AnalysisResult> {
    const body: AnalyzeRequest = { code };
    return this.request<AnalysisResult>("/api/v1/analyze", {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async refactorStream(
    request: RefactorRequest,
    onChunk: (content: string) => void,
    onDone: () => void,
    onError: (error: string) => void
  ): Promise<void> {
    const url = `${this.baseUrl}/api/v1/refactor`;

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      let detail = `Request failed with status ${response.status}`;
      try {
        const errorBody = await response.json();
        detail = errorBody.detail || detail;
      } catch {
        // ignore
      }
      onError(detail);
      return;
    }

    const contentType = response.headers.get("content-type") || "";

    // Handle SSE streaming
    if (contentType.includes("text/event-stream") || contentType.includes("text/plain")) {
      const reader = response.body?.getReader();
      if (!reader) {
        onError("No response body");
        return;
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();
            if (data === "[DONE]") {
              onDone();
              return;
            }
            try {
              const event: RefactorStreamEvent = JSON.parse(data);
              if (event.type === "chunk" && event.content) {
                onChunk(event.content);
              } else if (event.type === "done") {
                onDone();
                return;
              } else if (event.type === "error" && event.error) {
                onError(event.error);
                return;
              }
            } catch {
              // Not JSON, treat as raw text chunk
              if (data) {
                onChunk(data);
              }
            }
          }
        }
      }

      // Process remaining buffer
      if (buffer.trim()) {
        onChunk(buffer);
      }
      onDone();
      return;
    }

    // Handle regular JSON response (non-streaming fallback)
    const result = await response.json();
    if (result.refactoredCode) {
      onChunk(result.refactoredCode);
    } else if (result.code) {
      onChunk(result.code);
    }
    onDone();
  }

  async exportCode(request: ExportRequest): Promise<Blob> {
    const url = `${this.baseUrl}/api/v1/export`;
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      let detail = `Export failed with status ${response.status}`;
      try {
        const errorBody = await response.json();
        detail = errorBody.detail || detail;
      } catch {
        // ignore
      }
      const error: ApiError = { detail, status: response.status };
      throw error;
    }

    return response.blob();
  }
}

export const apiClient = new ApiClient("http://localhost:8000");
export default apiClient;
