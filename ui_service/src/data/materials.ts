// Kept for backward compatibility; prefer fetching from API in new code.
export type MaterialType = 'Image' | 'PDF' | 'Word' | 'Excel' | 'Other'

export interface MaterialModel {
  materialId: string
  type: MaterialType
  name: string
  size: number
  uploadTime: string
  url: string
  thumbnailUrl?: string
  iconName?: string
}

export const MOCK_MATERIALS: MaterialModel[] = []
