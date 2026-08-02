import type { Case, Report, Status } from "../types";

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "https://lexpilot-7r8w.onrender.com";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${BASE_URL}${path}`;

  console.log("Calling:", url);

  try {
    const response = await fetch(url, init);

    console.log("Status:", response.status);

    if (!response.ok) {
      const body = await response.text();
      console.error(body);
      throw new Error(body);
    }

    return response.json() as Promise<T>;
  } catch (err) {
    console.error("FETCH FAILED:", err);
    throw err;
  }
}

export const api = {
  listCases: () => request<Case[]>("/cases"),

  getCase: (id: string) =>
    request<Case>(`/cases/${id}`),

  getReport: (id: string) =>
    request<Report>(`/reports/${id}`),

  upload: (file: File, title?: string) => {
    const body = new FormData();

    body.append("file", file);

    if (title) {
      body.append("title", title);
    }

    return request<Case>("/cases/upload", {
      method: "POST",
      body,
    });
  },

  analyze: (id: string) =>
    request<{
      case_id: string;
      report_id: string;
      status: Status;
    }>(`/cases/${id}/analyze`, {
      method: "POST",
    }),
};
