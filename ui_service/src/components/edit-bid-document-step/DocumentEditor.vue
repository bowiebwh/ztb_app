
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { DocumentContent, DocumentNodeModel } from '@/data/document'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import DocumentNode from './DocumentNode.vue'

interface Props {
  documentContent: DocumentContent
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'placeholder-drop': [placeholderKey: string]
}>()

const dragOverPlaceholder = ref<string | null>(null)

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.dataTransfer!.dropEffect = 'copy'
}

const handleDrop = (placeholderKey: string, e: DragEvent) => {
  e.preventDefault()
  dragOverPlaceholder.value = null
  emit('placeholder-drop', placeholderKey)
}

const handleDragEnter = (placeholderKey: string) => {
  dragOverPlaceholder.value = placeholderKey
}

const handleDragLeave = () => {
  dragOverPlaceholder.value = null
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- 编辑器工具栏 -->
    <div class="border-b bg-card p-4 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <SafeIcon name="BookOpen" :size="20" class="text-primary" />
        <h2 class="text-lg font-semibold">投标文档编辑</h2>
      </div>
      <div class="flex items-center gap-2">
        <Button variant="outline" size="sm">
          <SafeIcon name="ChevronUp" :size="16" />
          上一步
        </Button>
        <Button size="sm">
          下一步
          <SafeIcon name="ChevronRight" :size="16" />
        </Button>
      </div>
    </div>

    <!-- 编辑区域 -->
    <ScrollArea class="flex-1">
      <div class="p-8 max-w-4xl mx-auto">
        <!-- 文档内容 -->
        <div class="space-y-6">
          <template v-for="(node, index) in documentContent" :key="index">
            <DocumentNode
              :node="node"
              :is-client="isClient"
              :drag-over-placeholder="dragOverPlaceholder"
              @drag-over="handleDragOver"
              @drop="(key) => handleDrop(key, $event)"
              @drag-enter="handleDragEnter"
              @drag-leave="handleDragLeave"
            />
          </template>
        </div>

        <!-- 提示信息 -->
        <div class="mt-12 p-4 bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg">
          <p class="text-sm text-blue-900 dark:text-blue-200">
            <strong>提示：</strong>将右侧材料库中的文件拖拽到文档中的占位符上，即可替换占位符内容。替换后，占位符将更新为已绑定状态。
          </p>
        </div>
      </div>
    </ScrollArea>
  </div>
</template>
