
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  projectId?: string
}

const props = withDefaults(defineProps<Props>(), {
  projectId: 'project-001',
})

const emit = defineEmits<{
  back: []
}>()

const handleBack = () => {
  emit('back')
}
</script>

<template>
  <div class="sticky top-16 z-40 bg-background border-b">
    <div class="container mx-auto px-4 py-4 max-w-4xl">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            @click="handleBack"
            aria-label="返回章节目录"
          >
            <SafeIcon name="ChevronLeft" :size="20" />
          </Button>
          <div>
            <h1 class="text-lg font-semibold">投标书内容预览</h1>
            <p class="text-sm text-muted-foreground">只读浏览 - 最终检查</p>
          </div>
        </div>
        
        <div class="flex items-center gap-2">
          <span class="text-xs text-muted-foreground">
            {{ new Date().toLocaleDateString('zh-CN') }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
