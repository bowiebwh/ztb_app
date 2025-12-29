
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  isClient?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isClient: true,
})

const emit = defineEmits<{
  download: []
  regenerate: []
  back: []
}>()

const handleDownload = () => {
  emit('download')
}

const handleRegenerate = () => {
  emit('regenerate')
}

const handleBack = () => {
  emit('back')
}
</script>

<template>
  <footer class="border-t bg-background mt-12">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
      <Separator class="mb-6" />
      
      <div class="flex flex-col sm:flex-row gap-4 justify-between items-center">
        <!-- Left Actions -->
        <div class="flex gap-2">
          <Button
            variant="outline"
            @click="handleBack"
            :disabled="!isClient"
          >
            <SafeIcon name="ChevronLeft" :size="16" class="mr-2" />
            返回章节目录
          </Button>
        </div>

        <!-- Right Actions -->
        <div class="flex gap-2">
          <Button
            variant="outline"
            @click="handleRegenerate"
            :disabled="!isClient"
          >
            <SafeIcon name="RotateCcw" :size="16" class="mr-2" />
            重新生成
          </Button>
          <Button
            @click="handleDownload"
            :disabled="!isClient"
          >
            <SafeIcon name="Download" :size="16" class="mr-2" />
            下载Word文件
          </Button>
        </div>
      </div>

      <!-- Info -->
      <div class="mt-6 pt-6 border-t text-center text-xs text-muted-foreground">
        <p>此为只读预览，内容已通过验证。点击"下载Word文件"获取最终投标书。</p>
      </div>
    </div>
  </footer>
</template>
