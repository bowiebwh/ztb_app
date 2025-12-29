
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import SafeIcon from '@/components/common/SafeIcon.vue'
import TextEditorHeader from './TextEditorHeader.vue'
import TextEditorToolbar from './TextEditorToolbar.vue'
import TextBlockEditor from './TextBlockEditor.vue'
import DocumentStructurePanel from './DocumentStructurePanel.vue'

// Mock document structure
const mockDocument = {
  id: 'doc-001',
  title: '投标文档 - 技术方案',
  sections: [
    {
      id: 'sec-1',
      type: 'heading',
      level: 1,
      content: '第一章 技术方案概述',
      children: [
        {
          id: 'para-1-1',
          type: 'paragraph',
          content: '本章节详细阐述我们的技术方案整体框架和核心思路。',
        },
        {
          id: 'para-1-2',
          type: 'paragraph',
          content: '系统采用微服务架构，支持高并发和弹性扩展。',
        },
      ],
    },
    {
      id: 'sec-2',
      type: 'heading',
      level: 1,
      content: '第二章 系统架构设计',
      children: [
        {
          id: 'para-2-1',
          type: 'paragraph',
          content: '系统总体架构如图所示：',
        },
        {
          id: 'img-2-1',
          type: 'image_placeholder',
          key: 'SYSTEM_ARCH',
          label: '系统架构图',
        },
        {
          id: 'para-2-2',
          type: 'paragraph',
          content: '架构包含以下主要模块：前端应用层、API网关层、业务服务层、数据存储层。',
        },
      ],
    },
  ],
}

const isClient = ref(true)
const selectedBlockId = ref<string | null>(null)
const editingContent = ref<Record<string, string>>({})
const viewMode = ref<'edit' | 'preview'>('edit')
const showStructure = ref(true)

// Initialize editing content from mock data
const initializeEditingContent = () => {
  const content: Record<string, string> = {}
  const traverse = (sections: any[]) => {
    sections.forEach((section) => {
      if (section.type === 'heading' || section.type === 'paragraph') {
        content[section.id] = section.content
      }
      if (section.children) {
        traverse(section.children)
      }
    })
  }
  traverse(mockDocument.sections)
  editingContent.value = content
}

// Get all editable blocks
const editableBlocks = computed(() => {
  const blocks: any[] = []
  const traverse = (sections: any[]) => {
    sections.forEach((section) => {
      if (section.type === 'heading' || section.type === 'paragraph') {
        blocks.push(section)
      }
      if (section.children) {
        traverse(section.children)
      }
    })
  }
  traverse(mockDocument.sections)
  return blocks
})

const updateBlockContent = (blockId: string, content: string) => {
  editingContent.value[blockId] = content
}

const handleSelectBlock = (blockId: string) => {
  selectedBlockId.value = blockId
}

const handleSave = () => {
  // In real implementation, this would save to backend
  console.log('Saving document:', editingContent.value)
  // Show success toast
}

const handleNavigateBack = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './edit-bid-document-step.html'
  }
}

onMounted(() => {
  isClient.value = false
  initializeEditingContent()
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <div class="flex flex-col h-[calc(100vh-64px)] bg-background">
    <!-- Header -->
    <TextEditorHeader
      :title="mockDocument.title"
      :view-mode="viewMode"
      @update:view-mode="viewMode = $event"
      @back="handleNavigateBack"
    />

    <!-- Main Content -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Left Panel: Document Structure -->
      <div
        v-if="showStructure && (isClient || true)"
        class="w-64 border-r bg-muted/30 overflow-y-auto flex-shrink-0 transition-all duration-300"
      >
        <DocumentStructurePanel
          :sections="mockDocument.sections"
          :selected-block-id="selectedBlockId"
          @select="handleSelectBlock"
        />
      </div>

      <!-- Center: Editor -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Toolbar -->
        <TextEditorToolbar
          :view-mode="viewMode"
          @toggle-structure="showStructure = !showStructure"
          @save="handleSave"
        />

        <!-- Editor Content -->
        <div class="flex-1 overflow-y-auto p-6">
          <div v-if="viewMode === 'edit'" class="max-w-4xl mx-auto space-y-6">
            <!-- Document Title -->
            <div class="mb-8">
              <h1 class="text-3xl font-bold text-foreground">{{ mockDocument.title }}</h1>
              <p class="text-sm text-muted-foreground mt-2">
                最后修改：{{ new Date().toLocaleString('zh-CN') }}
              </p>
            </div>

            <!-- Editable Sections -->
            <div class="space-y-6">
              <template v-for="section in mockDocument.sections" :key="section.id">
                <!-- Section Heading -->
                <TextBlockEditor
                  :block-id="section.id"
                  :block-type="section.type"
                  :level="section.level"
                  :content="editingContent[section.id] || ''"
                  :is-selected="selectedBlockId === section.id"
                  @select="handleSelectBlock"
                  @update:content="updateBlockContent"
                />

                <!-- Section Children -->
                <div v-if="section.children" class="ml-4 space-y-4">
                  <template v-for="child in section.children" :key="child.id">
                    <TextBlockEditor
                      v-if="child.type === 'paragraph' || child.type === 'heading'"
                      :block-id="child.id"
                      :block-type="child.type"
                      :level="child.level"
                      :content="editingContent[child.id] || ''"
                      :is-selected="selectedBlockId === child.id"
                      @select="handleSelectBlock"
                      @update:content="updateBlockContent"
                    />
                    <!-- Placeholder -->
                    <div
                      v-else-if="child.type === 'image_placeholder'"
                      class="p-4 border-2 border-dashed border-muted-foreground/30 rounded-lg bg-muted/20 text-center cursor-pointer hover:bg-muted/40 transition-colors"
                      @click="handleSelectBlock(child.id)"
                    >
                      <SafeIcon name="Image" :size="32" class="mx-auto text-muted-foreground mb-2" />
                      <p class="text-sm font-medium text-muted-foreground">{{ child.label }}</p>
                      <p class="text-xs text-muted-foreground mt-1">拖拽图片到此处替换</p>
                    </div>
                  </template>
                </div>
              </template>
            </div>
          </div>

          <!-- Preview Mode -->
          <div v-else class="max-w-4xl mx-auto prose prose-sm dark:prose-invert">
            <div class="space-y-6">
              <template v-for="section in mockDocument.sections" :key="section.id">
                <component
                  :is="section.type === 'heading' ? `h${section.level}` : 'p'"
                  class="text-foreground"
                >
                  {{ editingContent[section.id] || section.content }}
                </component>

                <template v-if="section.children">
                  <template v-for="child in section.children" :key="child.id">
                    <component
                      v-if="child.type === 'paragraph' || child.type === 'heading'"
                      :is="child.type === 'heading' ? `h${child.level}` : 'p'"
                      class="text-foreground"
                    >
                      {{ editingContent[child.id] || child.content }}
                    </component>
                    <div v-else-if="child.type === 'image_placeholder'" class="p-4 bg-muted rounded text-center">
                      <p class="text-sm text-muted-foreground">[{{ child.label }}]</p>
                    </div>
                  </template>
                </template>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Actions -->
    <div
      v-if="isClient || true"
      class="border-t bg-background px-6 py-4 flex justify-between items-center"
    >
      <div class="text-sm text-muted-foreground">
        已编辑 {{ Object.keys(editingContent).length }} 个文本块
      </div>
      <div class="flex gap-3">
        <Button variant="outline" @click="handleNavigateBack">
          <SafeIcon name="ArrowLeft" :size="16" class="mr-2" />
          返回编辑
        </Button>
        <Button @click="handleSave">
          <SafeIcon name="Save" :size="16" class="mr-2" />
          保存修改
        </Button>
      </div>
    </div>
  </div>
</template>
