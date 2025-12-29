
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'
import type { MaterialModel } from '@/src/data/materials'

interface Props {
  material: MaterialModel
  isClient?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isClient: true,
})

const isDragging = ref(false)
const isClient = ref(true)

const typeLabel = computed(() => {
  const labels: Record<string, string> = {
    Image: '图片',
    PDF: 'PDF',
    Word: 'Word',
    Excel: 'Excel',
  }
  return labels[props.material.type] || props.material.type
})

const fileSizeLabel = computed(() => {
  const bytes = props.material.size
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
})

const uploadTimeLabel = computed(() => {
  const date = new Date(props.material.uploadTime)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
})

const handleDragStart = (e: DragEvent) => {
  if (!isClient.value) return
  isDragging.value = true
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'copy'
    e.dataTransfer.setData('application/json', JSON.stringify({
      type: 'material',
      materialId: props.material.materialId,
      materialType: props.material.type,
      materialName: props.material.name,
      materialUrl: props.material.url,
    }))
  }
}

const handleDragEnd = () => {
  isDragging.value = false
}

const handleDownload = () => {
  if (typeof window !== 'undefined') {
    const link = document.createElement('a')
    link.href = props.material.url
    link.download = props.material.name
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <Card
    :class="cn(
      'overflow-hidden transition-all duration-200 cursor-move',
      (isDragging || !isClient) && 'opacity-50',
      isClient && 'hover:shadow-lg hover:border-primary/50'
    )"
    draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
  >
    <!-- Preview Area -->
    <div class="relative w-full h-40 bg-muted flex items-center justify-center overflow-hidden group">
      <!-- Image Preview -->
      <img
        v-if="material.type === 'Image' && material.thumbnailUrl"
        :src="material.thumbnailUrl"
        :alt="material.name"
        class="w-full h-full object-cover"
      />

      <!-- File Type Icon -->
      <div v-else class="flex flex-col items-center gap-2">
        <div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
          <SafeIcon
            :name="material.iconName || 'File'"
            :size="24"
            class="text-primary"
          />
        </div>
        <span class="text-xs font-medium text-muted-foreground">{{ typeLabel }}</span>
      </div>

      <!-- Drag Overlay -->
      <div
        v-if="isClient"
        class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center"
      >
        <div class="text-center text-white">
          <SafeIcon name="GripHorizontal" :size="24" class="mx-auto mb-1" />
          <p class="text-xs font-medium">拖拽到占位符</p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <CardContent class="p-3 space-y-2">
      <!-- File Name -->
      <div class="space-y-1">
        <p class="text-sm font-medium truncate" :title="material.name">
          {{ material.name }}
        </p>
        <p class="text-xs text-muted-foreground">
          {{ fileSizeLabel }}
        </p>
      </div>

      <!-- Meta Info -->
      <div class="text-xs text-muted-foreground space-y-0.5">
        <p>ID: {{ material.materialId }}</p>
        <p>上传: {{ uploadTimeLabel }}</p>
      </div>

      <!-- Actions -->
      <div class="flex gap-2 pt-2">
        <Button
          v-if="isClient"
          variant="outline"
          size="sm"
          class="flex-1 h-8"
          @click="handleDownload"
        >
          <SafeIcon name="Download" :size="14" />
          <span class="hidden sm:inline">下载</span>
        </Button>
        <Button
          variant="ghost"
          size="sm"
          class="flex-1 h-8"
          @click="() => {}"
        >
          <SafeIcon name="Copy" :size="14" />
          <span class="hidden sm:inline">复制</span>
        </Button>
      </div>
    </CardContent>
  </Card>
</template>
