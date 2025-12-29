
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { MaterialModel } from '@/data/materials'
import { cn } from '@/lib/utils'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  materials: MaterialModel[]
  draggedMaterial: MaterialModel | null
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'drag-start': [material: MaterialModel]
  'drag-end': []
}>()

const searchQuery = ref('')

const filteredMaterials = computed(() => {
  if (!searchQuery.value) return props.materials
  
  const query = searchQuery.value.toLowerCase()
  return props.materials.filter(m => m.name.toLowerCase().includes(query))
})

const materialsByType = computed(() => {
  const grouped: Record<string, MaterialModel[]> = {}
  
  filteredMaterials.value.forEach(material => {
    if (!grouped[material.type]) {
      grouped[material.type] = []
    }
    grouped[material.type].push(material)
  })
  
  return grouped
})

const handleDragStart = (e: DragEvent, material: MaterialModel) => {
  e.dataTransfer!.effectAllowed = 'copy'
  e.dataTransfer!.setData('text/plain', material.materialId)
  emit('drag-start', material)
}

const handleDragEnd = () => {
  emit('drag-end')
}

const getTypeIcon = (type: string) => {
  const icons: Record<string, string> = {
    'Image': 'Image',
    'PDF': 'FileText',
    'Word': 'ScrollText',
    'Excel': 'LayoutGrid',
  }
  return icons[type] || 'File'
}

const getTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    'Image': '图片',
    'PDF': 'PDF',
    'Word': 'Word',
    'Excel': 'Excel',
  }
  return labels[type] || type
}

const formatFileSize = (bytes: number) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Header -->
    <div class="border-b bg-card p-4 flex-shrink-0">
      <h2 class="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
        <SafeIcon name="Library" :size="16" />
        材料库
      </h2>
      <Input
        v-model="searchQuery"
        placeholder="搜索素材..."
        class="h-8 text-sm"
      />
    </div>

    <!-- Materials List -->
    <ScrollArea class="flex-1">
      <div class="p-4 space-y-4">
        <template v-for="(materials, type) in materialsByType" :key="type">
          <!-- Type Group Header -->
          <div class="sticky top-0 bg-card/95 backdrop-blur py-2 z-10">
            <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              {{ getTypeLabel(type) }}
            </h3>
          </div>

          <!-- Material Items -->
          <div class="space-y-2">
            <template v-for="material in materials" :key="material.materialId">
              <div
                draggable="true"
                @dragstart="handleDragStart($event, material)"
                @dragend="handleDragEnd"
                :class="cn(
                  'p-3 rounded-lg border bg-card transition-all',
                  'hover:border-primary/50 hover:bg-muted/50',
                  isClient && 'cursor-grab active:cursor-grabbing',
                  draggedMaterial?.materialId === material.materialId && 'opacity-50'
                )"
              >
                <!-- Thumbnail or Icon -->
                <div v-if="material.type === 'Image' && material.thumbnailUrl" class="mb-2 rounded overflow-hidden bg-muted h-24">
                  <img
                    :src="material.thumbnailUrl"
                    :alt="material.name"
                    class="w-full h-full object-cover"
                  />
                </div>
<div v-else class="mb-2 rounded bg-muted h-12 flex items-center justify-center">
                   <SafeIcon
                     :name="getTypeIcon(material.type)"
                     :size="24"
                     class="text-muted-foreground"
                   />
                </div>

                <!-- Info -->
                <p class="text-xs font-medium text-foreground truncate">
                  {{ material.name }}
                </p>
                <p class="text-xs text-muted-foreground mt-1">
                  {{ formatFileSize(material.size) }}
                </p>

                <!-- Upload Time -->
                <p class="text-xs text-muted-foreground/70 mt-1">
                  {{ new Date(material.uploadTime).toLocaleDateString('zh-CN') }}
                </p>
              </div>
            </template>
          </div>
        </template>

        <!-- Empty State -->
        <div v-if="filteredMaterials.length === 0" class="py-8 text-center">
          <SafeIcon name="Inbox" :size="32" class="mx-auto text-muted-foreground mb-2" />
          <p class="text-sm text-muted-foreground">
            {{ searchQuery ? '未找到匹配的素材' : '暂无素材' }}
          </p>
        </div>
      </div>
    </ScrollArea>

    <!-- Hint -->
    <div class="border-t bg-muted/30 p-3 flex-shrink-0">
      <p class="text-xs text-muted-foreground text-center">
        💡 拖拽素材到占位符进行绑定
      </p>
    </div>
  </div>
</template>
