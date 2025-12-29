// Placeholder for backward compatibility. Prefer fetching from /api/projects.
export type ProjectStatus = 'Draft' | 'Generating' | 'Completed' | 'Failed'

export interface ProjectModel {
  projectId: string
  projectName: string
  status: ProjectStatus
  createTime: string
  updateTime: string
  currentStepId: string
  description?: string
}

export const MOCK_PROJECTS: ProjectModel[] = []

export function getProjectById(id: string): ProjectModel | undefined {
  return MOCK_PROJECTS.find(p => p.projectId === id)
}
