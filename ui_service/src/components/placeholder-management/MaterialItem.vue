
<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'
import type { MaterialModel } from '@/data/materials'

interface Props {
  material: MaterialModel
  draggable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  draggable: false,
})

const emit = defineEmits<{
  select: []
}>()

const isDragging = ref(false)

const materialIcon = computed(() => {
  const iconMap: Record<string, string> = {
    'Image': 'Image',
    'PDF': 'FileText',
    'Word': 'ScrollText',
    'Excel': 'LayoutGrid',
  }
  return iconMap[props.material.type] || 'File'
})

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const handleDragStart = (e: DragEvent) => {
  if (!props.draggable) return
  isDragging.value = true
  e.dataTransfer!.effectAllowed = 'copy'
  e.dataTransfer!.setData('application/json', JSON.stringify(props.material))
}

const handleDragEnd = () => {
  isDragging.value = false
}
</script>

<template>
  <Card
    :class="cn(
      'cursor-pointer transition-all hover:shadow-md',
      isDragging && 'opacity-50',
      draggable && 'cursor-grab active:cursor-grabbing'
    )"
    :draggable="draggable"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @click="emit('select')"
  >
    <CardContent class="p-3">
      <div class="flex gap-3">
        <!-- Thumbnail or Icon -->
        <div class="w-12 h-12 rounded-lg bg-muted flex items-center justify-center flex-shrink-0 overflow-hidden">
          <img
            v-if="material.type === 'Image' && material.thumbnailUrl"
            :src="material.thumbnailUrl"
            :alt="material.name"
            class="w-full h-full object-cover"
          />
<SafeIcon
             v-else
             :name="materialIcon"
             :size="20"
             class="text-muted-foreground"
           />
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium truncate">{{ material.name }}</p>
          <p class="text-xs text-muted-foreground mt-0.5">
            {{ formatFileSize(material.size) }}
          </p>
          <p class="text-xs text-muted-foreground">
            {{ formatDate(material.uploadTime) }}
          </p>
        </div>

        <!-- Drag Indicator -->
        <div v-if="draggable" class="flex items-center justify-center flex-shrink-0">
          <SafeIcon name="GripVertical" :size="16" class="text-muted-foreground" />
        </div>
      </div>
    </CardContent>
  </Card>
</template>
