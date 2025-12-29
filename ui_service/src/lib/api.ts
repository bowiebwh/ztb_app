export const API_BASE =
  (import.meta as any).env?.VITE_API_BASE?.replace(/\/$/, '') ||
  'http://localhost:8000'

export interface Project {
  projectId: string
  projectName: string
  status: string
  createTime: string
  updateTime: string
  currentStepId?: string
  description?: string | null
}

export interface Material {
  materialId: string
  type: string
  name: string
  size: number
  uploadTime: string
  url: string
  thumbnailUrl?: string | null
  iconName?: string | null
  contentType?: string | null
}

export interface GenerationTask {
  taskId: number
  projectId: number
  status: string
  progress: number
  currentStage?: string
  statusMessage?: string
  resultUrl?: string
  errorMessage?: string
  configId?: string
  startTime: string
  updateTime: string
}

export interface TenderAnalysis {
  summary: string
  keyDates: Array<{ label: string; date: string }>
  documentStructure: Array<{ id: string; title: string; sections: string[] }>
}

const defaultHeaders = {
  'Content-Type': 'application/json',
}

export async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${API_BASE}/api/projects`)
  if (!res.ok) throw new Error('获取项目列表失败')
  return res.json()
}

export async function fetchProject(id: string | number): Promise<Project> {
  const res = await fetch(`${API_BASE}/api/projects/${id}`)
  if (!res.ok) throw new Error('获取项目失败')
  return res.json()
}

export async function createProject(payload: { projectName: string; description?: string }) {
  const res = await fetch(`${API_BASE}/api/projects`, {
    method: 'POST',
    headers: defaultHeaders,
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('创建项目失败')
  return res.json() as Promise<Project>
}

export async function fetchMaterials(): Promise<Material[]> {
  const res = await fetch(`${API_BASE}/api/materials`)
  if (!res.ok) throw new Error('获取素材失败')
  return res.json()
}

export async function uploadMaterial(file: File): Promise<Material> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/api/materials/upload`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) throw new Error('上传素材失败')
  return res.json()
}

export async function fetchLatestGenerationTask(projectId: string | number): Promise<GenerationTask> {
  const res = await fetch(`${API_BASE}/api/generation/${projectId}/latest`)
  if (!res.ok) throw new Error('获取生成任务失败')
  return res.json()
}

export async function fetchGenerationHistory(projectId: string | number): Promise<GenerationTask[]> {
  const res = await fetch(`${API_BASE}/api/generation/${projectId}/history`)
  if (!res.ok) throw new Error('获取生成历史失败')
  return res.json()
}

export async function fetchDocument(projectId: string | number) {
  const res = await fetch(`${API_BASE}/api/document/${projectId}`)
  if (!res.ok) throw new Error('获取文档数据失败')
  return res.json()
}

export async function fetchDocumentStructure(projectId: string | number) {
  const res = await fetch(`${API_BASE}/api/document/${projectId}/structure`)
  if (!res.ok) throw new Error('获取文档结构失败')
  return res.json()
}

export async function saveDocumentStructure(projectId: string | number, content: any, structure?: any) {
  const res = await fetch(`${API_BASE}/api/document/${projectId}/structure`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, structure }),
  })
  if (!res.ok) throw new Error('保存文档结构失败')
  return res.json()
}

export async function exportCurrentDocument(projectId: string | number) {
  const res = await fetch(`${API_BASE}/api/generation/${projectId}/export_current`, {
    method: 'POST',
    headers: defaultHeaders,
  })
  if (!res.ok) throw new Error('导出最新文档失败')
  return res.json() as Promise<GenerationTask>
}

export async function deleteMaterialBinding(bindingId: string | number) {
  const res = await fetch(`${API_BASE}/api/materials/bindings/${bindingId}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('删除占位符绑定失败')
  return res.json()
}

export async function fetchMaterialBindings(projectId?: string | number) {
  const url = projectId
    ? `${API_BASE}/api/materials/bindings?project_id=${projectId}`
    : `${API_BASE}/api/materials/bindings`
  const res = await fetch(url)
  if (!res.ok) throw new Error('获取占位符绑定失败')
  return res.json()
}

export async function bindMaterial(payload: { projectId: string | number; placeholderKey: string; materialId: string | number }) {
  const res = await fetch(`${API_BASE}/api/materials/bind`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('绑定素材失败')
  return res.json()
}

export async function startGeneration(projectId: string | number, configId?: string) {
  const res = await fetch(`${API_BASE}/api/generation/${projectId}`, {
    method: 'POST',
    headers: defaultHeaders,
    body: JSON.stringify({ configId }),
  })
  if (!res.ok) throw new Error('启动生成任务失败')
  return res.json() as Promise<GenerationTask>
}

export async function fetchAnalysis(projectId: string | number, refresh: boolean = false): Promise<TenderAnalysis> {
  const url = new URL(`${API_BASE}/api/analysis/${projectId}`)
  if (refresh) url.searchParams.set('refresh', 'true')
  const res = await fetch(url.toString())
  if (!res.ok) {
    let msg = '获取分析结果失败'
    try {
      const data = await res.json()
      msg = (data as any)?.detail || msg
    } catch {
      // ignore
    }
    throw new Error(msg)
  }
  return res.json()
}

export async function uploadFile(file: File, projectId?: string | number) {
  const formData = new FormData()
  if (projectId) formData.append('project_id', String(projectId))
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/api/files/upload`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) throw new Error('文件上传失败')
  return res.json()
}
