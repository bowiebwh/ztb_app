
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import GenerateConfigForm from '@/components/generate-configuration/GenerateConfigForm.vue'
import SafeIcon from '@/components/common/SafeIcon.vue'

const isClient = ref(true)
const isLoading = ref(false)

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})

const handleStartGeneration = async () => {
  isLoading.value = true
  try {
    // 模拟生成任务提交
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 导航到生成状态页面
    if (typeof window !== 'undefined') {
      window.location.href = './generation-status.html'
    }
  } catch (error) {
    console.error('生成失败:', error)
  } finally {
    isLoading.value = false
  }
}

const handleGoBack = () => {
  if (typeof window !== 'undefined') {
    window.location.href = './edit-bid-document-step.html'
  }
}
</script>

<template>
  <main class="flex-1 container mx-auto px-4 py-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">生成配置</h1>
      <p class="text-muted-foreground">
        配置投标书的生成参数，包括输出语言、范围和格式
      </p>
    </div>

    <!-- Main Content -->
    <div class="grid gap-6 max-w-2xl">
      <!-- Configuration Card -->
      <Card>
        <CardHeader>
          <CardTitle>生成选项</CardTitle>
          <CardDescription>
            请选择投标书的生成参数，系统将根据您的配置生成最终的 Word 文档
          </CardDescription>
        </CardHeader>
        <CardContent>
          <GenerateConfigForm client:load />
        </CardContent>
      </Card>

      <!-- Info Card -->
      <Card class="bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-900">
        <CardContent class="pt-6">
          <div class="flex gap-3">
            <SafeIcon name="Info" :size="20" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div class="text-sm text-blue-900 dark:text-blue-300">
              <p class="font-medium mb-1">生成说明</p>
              <ul class="space-y-1 text-xs">
                <li>• 生成过程为异步任务，可能需要 2-5 分钟</li>
                <li>• 系统将基于您编辑的文档内容和配置参数生成 Word 文件</li>
                <li>• 生成完成后可预览和下载最终文档</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Action Buttons -->
      <div class="flex gap-3 pt-4">
        <Button
          variant="outline"
          @click="handleGoBack"
          :disabled="isLoading || !isClient"
          class="flex-1"
        >
          <SafeIcon name="ChevronLeft" :size="16" class="mr-2" />
          返回编辑
        </Button>
        <Button
          @click="handleStartGeneration"
          :disabled="isLoading || !isClient"
          class="flex-1"
        >
          <SafeIcon
            v-if="isLoading"
            name="Loader2"
            :size="16"
            class="mr-2 animate-spin"
          />
          <SafeIcon
            v-else
            name="Zap"
            :size="16"
            class="mr-2"
          />
          {{ isLoading ? '生成中...' : '开始生成投标书' }}
        </Button>
      </div>
    </div>
  </main>
</template>
