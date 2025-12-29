
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { toast } from 'vue-sonner'

interface Props {
  resultUrl?: string
}

const props = defineProps<Props>()

const isClient = ref(true)
const isDownloading = ref(false)

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})

const handleDownload = async () => {
  if (!props.resultUrl) {
    toast.error('下载链接不可用')
    return
  }

  isDownloading.value = true
  try {
    // Simulate download
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // In real implementation, this would trigger actual file download
    if (typeof window !== 'undefined') {
      const link = document.createElement('a')
      link.href = props.resultUrl
      link.download = 'bid-document.docx'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
    
    toast.success('投标书已下载')
  } catch (error) {
    toast.error('下载失败，请重试')
  } finally {
    isDownloading.value = false
  }
}

const handleRegenerate = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './generate-configuration.html'
  }
}

const handleBackToProject = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './project-detail-editor.html'
  }
}
</script>

<template>
  <Card class="mt-6">
    <CardContent class="pt-6">
      <div class="flex flex-col sm:flex-row gap-3 justify-between items-start sm:items-center">
        <div class="space-y-1">
          <p class="font-semibold">投标书已生成完毕</p>
          <p class="text-sm text-muted-foreground">
            您可以下载Word文件或选择重新生成
          </p>
        </div>

        <div class="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
          <Button
            variant="outline"
            @click="handleBackToProject"
            class="flex items-center gap-2"
          >
            <SafeIcon name="ArrowLeft" :size="16" />
            返回项目
          </Button>

          <Button
            variant="outline"
            @click="handleRegenerate"
            class="flex items-center gap-2"
          >
            <SafeIcon name="RotateCcw" :size="16" />
            重新生成
          </Button>

          <Button
            @click="handleDownload"
            :disabled="isDownloading || !resultUrl"
            class="flex items-center gap-2"
          >
            <SafeIcon
              :name="isDownloading ? 'Loader2' : 'Download'"
              :size="16"
              :class="isDownloading && 'animate-spin'"
            />
            {{ isDownloading ? '下载中...' : '下载Word文件' }}
          </Button>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
