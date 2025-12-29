
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import SafeIcon from '@/components/common/SafeIcon.vue'

const isClient = ref(true)

const handleReturnConfig = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './generate-configuration.html'
  }
}

const handleViewHistory = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './generation-history.html'
  }
}

const handleReturnProject = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './project-detail-editor.html'
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
  <Card>
    <CardContent class="pt-6">
      <div class="flex flex-col sm:flex-row gap-3">
        <Button
          variant="outline"
          class="flex-1"
          @click="handleReturnConfig"
        >
          <SafeIcon name="ArrowLeft" :size="16" class="mr-2" />
          返回配置
        </Button>

        <Button
          variant="outline"
          class="flex-1"
          @click="handleViewHistory"
        >
          <SafeIcon name="History" :size="16" class="mr-2" />
          查看历史
        </Button>

        <Button
          variant="outline"
          class="flex-1"
          @click="handleReturnProject"
        >
          <SafeIcon name="Home" :size="16" class="mr-2" />
          返回项目
        </Button>
      </div>

      <!-- Additional Info -->
      <div class="mt-6 pt-6 border-t">
        <div class="text-xs text-muted-foreground space-y-2">
          <div class="flex items-start gap-2">
            <SafeIcon name="AlertCircle" :size="14" class="flex-shrink-0 mt-0.5" />
            <span>生成过程中如遇到问题，请查看错误日志或联系技术支持。</span>
          </div>
          <div class="flex items-start gap-2">
            <SafeIcon name="Clock" :size="14" class="flex-shrink-0 mt-0.5" />
            <span>大型文档生成可能需要 5-10 分钟，请耐心等待。</span>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
