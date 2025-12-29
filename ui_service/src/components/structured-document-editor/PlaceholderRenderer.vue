
<script setup lang="ts">
import { computed } from 'vue'
import type { PlaceholderModel, BoundImageNode } from '@/data/document'
import type { MaterialModel } from '@/data/materials'
import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  node: PlaceholderModel | BoundImageNode
  draggedMaterial: MaterialModel | null
  isDragOver: boolean
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'drag-over': [event: DragEvent]
  'drag-leave': []
  'drop': [event: DragEvent]
}>()

const isBoundImage = computed(() => props.node.type === 'image')
const isPlaceholder = computed(() => props.node.type === 'image_placeholder' || props.node.type === 'table_placeholder')

const placeholderLabel = computed(() => {
  if (isPlaceholder.value) {
    return (props.node as PlaceholderModel).label
  }
  if (isBoundImage.value) {
    return (props.node as BoundImageNode).preview?.name || '已绑定素材'
  }
  return ''
})

const placeholderType = computed(() => {
  if (isPlaceholder.value) {
    return (props.node as PlaceholderModel).type
  }
  return 'image'
})

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.dataTransfer!.dropEffect = 'copy'
  emit('drag-over', e)
}

const handleDragLeave = () => {
  emit('drag-leave')
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  emit('drop', e)
}

const getPlaceholderIcon = () => {
  if (placeholderType.value === 'table_placeholder') return 'Table2'
  return 'Image'
}
</script>

<template>
  <!-- Bound Image -->
  <div v-if="isBoundImage" class="my-4">
    <div class="bg-muted/50 rounded-lg p-4 border border-border">
      <div class="flex items-start gap-3">
        <SafeIcon name="CheckCircle2" :size="20" class="text-green-600 flex-shrink-0 mt-1" />
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-foreground">已绑定素材</p>
          <p class="text-xs text-muted-foreground mt-1">{{ placeholderLabel }}</p>
        </div>
      </div>
      
      <!-- Preview Image -->
      <div v-if="(node as BoundImageNode).preview?.url" class="mt-3">
        <img
          :src="(node as BoundImageNode).preview!.url"
          :alt="placeholderLabel"
          class="max-w-full h-auto rounded border border-border"
        />
      </div>
    </div>
  </div>

  <!-- Unbound Placeholder -->
  <div
    v-else
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
    :class="cn(
      'my-4 p-6 rounded-lg border-2 border-dashed transition-all',
      isDragOver && 'border-primary bg-primary/10',
      !isDragOver && 'border-muted-foreground/30 bg-muted/20 hover:border-muted-foreground/50',
      isClient && 'cursor-copy'
    )"
  >
    <div class="flex flex-col items-center justify-center text-center">
<SafeIcon
        :name="getPlaceholderIcon()"
        :size="32"
        :class="cn(
          'mb-3',
          isDragOver ? 'text-primary' : 'text-muted-foreground'
        )"
      />
      
      <p class="text-sm font-medium text-foreground mb-1">
        {{ placeholderLabel }}
      </p>
      
      <p class="text-xs text-muted-foreground mb-3">
        {{ isDragOver ? '释放鼠标以绑定素材' : '拖拽素材到此处绑定' }}
      </p>
      
      <Badge variant="secondary" class="text-xs">
        {{ placeholderType === 'table_placeholder' ? '表格占位符' : '图片占位符' }}
      </Badge>
    </div>
  </div>
</template>
