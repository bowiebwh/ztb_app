
<script setup lang="ts">
import type { MaterialModel } from '@/data/materials'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  material: MaterialModel
  isDragging: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'drag-start': []
  'drag-end': []
}>()

const handleDragStart = (e: DragEvent) => {
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'copy'
    e.dataTransfer.setData('text/plain', props.material.materialId)
  }
  emit('drag-start')
}

const handleDragEnd = () => {
  emit('drag-end')
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

const getIconName = (): string => {
  if (props.material.type === 'Image') return 'Image'
  if (props.material.type === 'PDF') return 'FileText'
  if (props.material.type === 'Word') return 'ScrollText'
  if (props.material.type === 'Excel') return 'LayoutGrid'
  return 'File'
}
</script>

<template>
  <div
    draggable="true"
    :class="cn(
      'p-2 rounded-lg border cursor-move transition-all',
      isDragging
        ? 'bg-primary/20 border-primary opacity-50'
        : 'bg-muted/50 border-border hover:bg-muted hover:border-primary/50'
    )"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
  >
    <!-- 图片缩略图 -->
    <div v-if="material.type === 'Image' && material.thumbnailUrl" class="mb-2 rounded overflow-hidden bg-muted">
      <img
        :src="material.thumbnailUrl"
        :alt="material.name"
        class="w-full h-20 object-cover"
      />
    </div>

    <!-- 文件信息 -->
    <div class="flex items-start gap-2">
      <SafeIcon
        :name="getIconName()"
        :size="16"
        class="text-muted-foreground flex-shrink-0 mt-0.5"
      />
      <div class="flex-1 min-w-0">
        <p class="text-xs font-medium text-foreground truncate">
          {{ material.name }}
        </p>
        <p class="text-xs text-muted-foreground">
          {{ formatFileSize(material.size) }}
        </p>
      </div>
    </div>
  </div>
</template>
