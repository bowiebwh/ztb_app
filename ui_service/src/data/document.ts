// Deprecated mock placeholder. Components should fetch from /api/document/{projectId}/structure
export type DocumentNodeType = 'chapter' | 'paragraph' | 'text' | 'image_placeholder' | 'table_placeholder' | 'image'
export interface RichTextNode {
  type: 'text'
  value: string
  format?: 'bold' | 'italic'
}
export interface PlaceholderModel {
  key: string
  type: 'image_placeholder' | 'table_placeholder'
  label: string
}
export interface BoundImageNode {
  type: 'image'
  placeholderKey: string
  materialId: string
  styleRef: string
}
export interface ParagraphNode {
  type: 'paragraph'
  children: Array<RichTextNode | PlaceholderModel | BoundImageNode>
}
export interface ChapterNode {
  type: 'chapter'
  title: string
  index: string
  children: Array<ChapterNode | ParagraphNode>
}
export type DocumentNodeModel = ChapterNode | ParagraphNode | RichTextNode | PlaceholderModel | BoundImageNode
export type DocumentContent = DocumentNodeModel[]

export const MOCK_DOCUMENT_CONTENT: DocumentContent = []
