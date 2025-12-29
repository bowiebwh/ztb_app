
<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'

interface PlaceholderItem {
  key: string
  label: string
  type: 'image_placeholder' | 'table_placeholder'
  isBound: boolean
  boundMaterialId?: string
  boundMaterialName?: string
  boundMaterialUrl?: string
}

interface Props {
  placeholder: PlaceholderItem
  selected?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  selected: false,
})

const emit = defineEmits<{
  select: []
  bind: [material: any]
  unbind: []
}>()

const isDraggingOver = ref(false)

const placeholderIcon = computed(() => {
  return props.placeholder.type === 'image_placeholder' ? 'Image' : 'Table2'
})

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  isDraggingOver.value = true
}

const handleDragLeave = () => {
  isDraggingOver.value = false
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  isDraggingOver.value = false
  
  const materialData = e.dataTransfer?.getData('application/json')
  if (materialData) {
    try {
      const material = JSON.parse(materialData)
      emit('bind', material)
    } catch (error) {
      console.error('Failed to parse material data:', error)
    }
  }
}

const handleUnbind = () => {
  emit('unbind')
}
</script>

<template>
  <Card
    :class="cn(
      'cursor-pointer transition-all',
      selected && 'ring-2 ring-primary',
      isDraggingOver && 'ring-2 ring-primary bg-primary/5'
    )"
    @click="emit('select')"
    @dragover="handleDragOver"
    @dragleave="handleDragLeave"
    @drop="handleDrop"
  >
    <CardHeader class="pb-3">
      <div class="flex items-start justify-between gap-2">
        <div class="flex items-start gap-3 flex-1 min-w-0">
          <div class="w-8 h-8 rounded-lg bg-muted flex items-center justify-center flex-shrink-0 mt-0.5">
            <SafeIcon :name="placeholderIcon" :size="18" class="text-muted-foreground" />
          </div>
          <div class="flex-1 min-w-0">
            <CardTitle class="text-base truncate">{{ placeholder.label }}</CardTitle>
            <CardDescription class="text-xs mt-1 font-mono">{{ placeholder.key }}</CardDescription>
          </div>
        </div>
        <Badge
          :variant="placeholder.isBound ? 'default' : 'secondary'"
          class="flex-shrink-0"
        >
          {{ placeholder.isBound ? '已绑定' : '未绑定' }}
        </Badge>
      </div>
    </CardHeader>

    <!-- Bound Material Info -->
    <CardContent v-if="placeholder.isBound" class="space-y-3">
      <div class="p-3 rounded-lg bg-muted/50 border border-border">
        <p class="text-xs text-muted-foreground mb-1">绑定素材</p>
        <p class="text-sm font-medium truncate">{{ placeholder.boundMaterialName }}</p>
      </div>
      <Button
        variant="outline"
        size="sm"
        class="w-full gap-2"
        @click.stop="handleUnbind"
      >
        <SafeIcon name="Trash2" :size="16" />
        解除绑定
      </Button>
    </CardContent>

    <!-- Drop Zone -->
    <CardContent v-else class="pt-0">
      <div
        :class="cn(
          'p-6 rounded-lg border-2 border-dashed transition-colors',
          isDraggingOver ? 'border-primary bg-primary/5' : 'border-border bg-muted/30'
        )"
      >
        <div class="flex flex-col items-center justify-center text-center">
          <SafeIcon name="Upload" :size="24" class="text-muted-foreground mb-2" />
          <p class="text-xs text-muted-foreground">
            拖拽素材到此处
          </p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
