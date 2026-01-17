/**
 * API Client for backend communication
 */
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Paper {
  paper_id: string;
  title: string;
  abstract: string;
  authors: string[];
  num_pages: number;
  status: string;
}

export interface Contribution {
  contribution_type: string;
  specific_innovation: string;
  problem_addressed: string;
  evidence_location: string;
  comment: string;
}

export interface Experiment {
  experiment_id: string;
  name: string;
  description: string;
  task: string;
  datasets: any[];
  baselines: any[];
  proposed_methods: any[];
  evaluation_metrics: any[];
  results: any[];
  hyperparameters: Record<string, any>;
  evidence_location: string;
  notes: string;
}

// API Functions
export const paperApi = {
  // Upload a paper
  uploadPaper: async (file: File): Promise<Paper> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/papers', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get paper details
  getPaper: async (paperId: string): Promise<Paper> => {
    const response = await api.get(`/api/papers/${paperId}`);
    return response.data;
  },

  // List all papers
  listPapers: async (): Promise<{ papers: Paper[]; total: number }> => {
    const response = await api.get('/api/papers');
    return response.data;
  },

  // Extract contributions
  extractContributions: async (paperId: string): Promise<{ contributions: Contribution[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/contributions`);
    return response.data;
  },

  // Extract experiments
  extractExperiments: async (paperId: string): Promise<{ experiments: Experiment[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/experiments`);
    return response.data;
  },

  // Extract architectures
  extractArchitectures: async (paperId: string): Promise<{ architectures: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/architecture`);
    return response.data;
  },

  // Extract hyperparameters
  extractHyperparameters: async (paperId: string): Promise<{ hyperparameters: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/hyperparameters`);
    return response.data;
  },

  // Extract ablations
  extractAblations: async (paperId: string): Promise<{ ablations: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/ablations`);
    return response.data;
  },

  // Extract baselines
  extractBaselines: async (paperId: string): Promise<{ baselines: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/baselines`);
    return response.data;
  },

  // Extract equations
  extractEquations: async (paperId: string): Promise<{ equations: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/equations`);
    return response.data;
  },

  // Extract algorithms
  extractAlgorithms: async (paperId: string): Promise<{ algorithms: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/algorithms`);
    return response.data;
  },

  // Extract limitations
  extractLimitations: async (paperId: string): Promise<{ limitations: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/limitations`);
    return response.data;
  },

  // Extract future work
  extractFutureWork: async (paperId: string): Promise<{ future_work: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/future_work`);
    return response.data;
  },

  // Extract code resources
  extractCodeResources: async (paperId: string): Promise<{ code_resources: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/code_resources`);
    return response.data;
  },

  // Extract datasets
  extractDatasets: async (paperId: string): Promise<{ datasets: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/datasets`);
    return response.data;
  },

  // Extract loss functions
  extractLossFunctions: async (paperId: string): Promise<{ loss_functions: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/loss_functions`);
    return response.data;
  },

  // Extract metrics
  extractMetrics: async (paperId: string): Promise<{ metrics: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/metrics`);
    return response.data;
  },

  // Extract training procedures
  extractTraining: async (paperId: string): Promise<{ training: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/training`);
    return response.data;
  },

  // Extract related work
  extractRelatedWork: async (paperId: string): Promise<{ related_work: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/related_work`);
    return response.data;
  },

  // Extract claims
  extractClaims: async (paperId: string): Promise<{ claims: any[]; cached: boolean }> => {
    const response = await api.post(`/api/papers/${paperId}/extract/claims`);
    return response.data;
  },

  // Custom query
  queryPaper: async (paperId: string, query: string): Promise<{ result: string }> => {
    const response = await api.post(`/api/papers/${paperId}/query`, { query });
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<{ status: string; llm: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
};

