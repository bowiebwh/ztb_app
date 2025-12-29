
<script setup lang="ts">
import type { BoundImageNode as BoundImageNodeType } from '@/data/document'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  node: BoundImageNodeType
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'replace': []
}>()
</script>

<template>
  <div class="block w-full">
    <div class="relative group">
      <!-- 图片容器 -->
      <div class="bg-muted rounded-lg overflow-hidden border border-border">
        <img
          v-if="node.preview?.url"
          :src="node.preview.url"
          :alt="node.preview.name"
          class="w-full h-auto object-cover max-h-96"
        />
        <div v-else class="w-full h-64 flex items-center justify-center bg-muted">
          <SafeIcon name="Image" :size="48" class="text-muted-foreground" />
        </div>
      </div>

      <!-- 图片信息 -->
      <div class="mt-2 flex items-center justify-between">
        <div class="flex-1">
          <p class="text-sm font-medium text-foreground">{{ node.preview?.name }}</p>
          <p class="text-xs text-muted-foreground">已绑定素材</p>
        </div>
        <Button
          v-if="isClient"
          variant="ghost"
          size="sm"
          @click="emit('replace')"
          class="opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <SafeIcon name="RotateCcw" :size="16" />
          替换
        </Button>
      </div>
    </div>
  </div>
</template>
