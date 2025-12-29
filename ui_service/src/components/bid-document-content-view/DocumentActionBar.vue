
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  isClient: boolean
  isLoading: boolean
}

defineProps<Props>()

const emit = defineEmits<{
  download: []
  regenerate: []
}>()
</script>

<template>
  <div class="border-t bg-card p-4 flex items-center justify-between">
    <div class="flex items-center gap-2 text-sm text-muted-foreground">
      <SafeIcon name="Info" :size="16" />
      <span>这是投标书的只读预览，不可编辑</span>
    </div>

    <div class="flex items-center gap-3">
      <Button
        variant="outline"
        @click="() => emit('regenerate')"
        :disabled="isLoading || !isClient"
      >
        <SafeIcon name="RotateCcw" :size="16" />
        重新生成
      </Button>

      <Button
        @click="() => emit('download')"
        :disabled="isLoading || !isClient"
      >
        <SafeIcon v-if="!isLoading" name="Download" :size="16" />
        <SafeIcon v-else name="Loader2" :size="16" class="animate-spin" />
        {{ isLoading ? '下载中...' : '下载 Word 文件' }}
      </Button>
    </div>
  </div>
</template>
