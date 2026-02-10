import axios from "axios"

// Types matching backend schema
export interface ProductInput {
  name: string;
  max_price?: number;
  max_rating?: number;
  quantity: number;
}

export interface UserInput {
  website: string;
  products: ProductInput[];
}

export interface ExecuteResponse {
  task_prompt: string;
  execution_status: string;
}

export const api = axios.create({
  baseURL: "http://localhost:8000",
});

// API methods
export const executeTask = async (data: UserInput): Promise<ExecuteResponse> => {
  const response = await api.post<ExecuteResponse>('/execute', data);
  return response.data;
};