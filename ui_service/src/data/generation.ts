export type TaskStatus = 'Pending' | 'InProgress' | 'Completed' | 'Failed'
export type TaskStage = 'Initialization' | 'Analysis' | 'KnowledgeRetrieval' | 'Drafting' | 'Finalizing' | 'Rendering'

export interface DocumentTOCModel {
  id: string
  index: string
  title: string
  children: DocumentTOCModel[]
}

export interface GenerationTaskModel {
  taskId: string
  projectId: string
  startTime: string
  status: TaskStatus
  progress: number
  currentStage: TaskStage
  statusMessage: string
  resultUrl?: string
  errorMessage?: string
  generatedToc?: DocumentTOCModel[]
  configId: string
}

// Deprecated: mock data removed; consumers should fetch from /api/generation endpoints.
export const MOCK_TOC: DocumentTOCModel[] = []
export const MOCK_GENERATION_TASK_IN_PROGRESS: GenerationTaskModel = {} as any
export const MOCK_GENERATION_TASK_COMPLETED: GenerationTaskModel = {} as any
export const MOCK_GENERATION_TASK_FAILED: GenerationTaskModel = {} as any
export const MOCK_GENERATION_HISTORY: GenerationTaskModel[] = []
