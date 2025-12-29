
<script setup lang="ts">
import { computed } from 'vue'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { MaterialModel } from '@/data/materials'
import { BoundImageNode } from '@/data/document'

interface Props {
  material: MaterialModel
  boundNode?: BoundImageNode
}

const props = defineProps<Props>()

const fileSize = computed(() => {
  const bytes = props.material.size
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
})

const uploadDate = computed(() => {
  if (typeof window !== 'undefined') {
    const date = new Date(props.material.uploadTime)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }
  return props.material.uploadTime
})

const typeIcon = computed(() => {
  const typeMap: Record<string, string> = {
    Image: 'Image',
    PDF: 'FileText',
    Word: 'ScrollText',
    Excel: 'LayoutGrid',
  }
  return typeMap[props.material.type] || 'File'
})
</script>

<template>
  <div class="space-y-3">
    <!-- 预览图 -->
    <div v-if="material.type === 'Image' && material.url" class="rounded-lg overflow-hidden bg-muted">
      <img
        :src="material.url"
        :alt="material.name"
        class="w-full h-48 object-cover"
      />
    </div>

    <!-- 文件信息 -->
    <div class="space-y-2">
      <div class="flex items-start gap-3">
        <div class="flex-shrink-0 w-8 h-8 rounded bg-muted flex items-center justify-center">
          <SafeIcon :name="typeIcon" :size="16" class="text-muted-foreground" />
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-medium text-sm truncate">{{ material.name }}</p>
          <p class="text-xs text-muted-foreground">
            {{ fileSize }} · {{ uploadDate }}
          </p>
        </div>
      </div>

      <!-- 绑定信息 -->
      <div v-if="boundNode" class="bg-muted rounded-lg p-3 space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-muted-foreground">绑定信息</span>
          <Badge variant="secondary" class="text-xs">
            <SafeIcon name="Link2" :size="12" class="mr-1" />
            已关联
          </Badge>
        </div>
        <div class="text-xs space-y-1">
          <div class="flex justify-between">
            <span class="text-muted-foreground">占位符 Key:</span>
            <code class="bg-background px-2 py-1 rounded text-xs font-mono">
              {{ boundNode.placeholderKey }}
            </code>
          </div>
          <div class="flex justify-between">
            <span class="text-muted-foreground">样式引用:</span>
            <code class="bg-background px-2 py-1 rounded text-xs font-mono">
              {{ boundNode.styleRef }}
            </code>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
