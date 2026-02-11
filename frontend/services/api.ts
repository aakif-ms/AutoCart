import axios from "axios"

export interface ProductInput {
  name: string;
  max_price?: number;
  quantity: number;
  rating: string;
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
  baseURL: "http://localhost:8000"
});

export const executeTask = async (data: UserInput): Promise<ExecuteResponse> =>  {
  const response = await api.post<ExecuteResponse>("/execute", data);
  return response.data;
}