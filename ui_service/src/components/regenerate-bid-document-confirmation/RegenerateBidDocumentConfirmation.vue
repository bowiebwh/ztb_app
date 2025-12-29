
<script setup lang="ts">
import { ref } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import SafeIcon from '@/components/common/SafeIcon.vue'

const isOpen = ref(true)
const isLoading = ref(false)

const handleConfirm = () => {
  isLoading.value = true
  // 导航到生成配置页面
  if (typeof window !== 'undefined') {
    setTimeout(() => {
      window.location.href = './generate-configuration.html'
    }, 300)
  }
}

const handleCancel = () => {
  // 返回到投标书预览页面
  if (typeof window !== 'undefined') {
    window.location.href = './bid-document-preview.html'
  }
}

const handleOpenChange = (value: boolean) => {
  if (!value) {
    handleCancel()
  }
}
</script>

<template>
  <Dialog :open="isOpen" @update:open="handleOpenChange">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle class="text-lg">重新生成投标书</DialogTitle>
        <DialogDescription>
          确认是否要重新生成投标书
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4">
        <!-- Warning Alert -->
        <Alert variant="destructive">
          <SafeIcon name="AlertTriangle" :size="16" />
          <AlertTitle>重要提示</AlertTitle>
          <AlertDescription>
            重新生成投标书将覆盖现有的生成结果。此操作无法撤销，请确保已备份重要文件。
          </AlertDescription>
        </Alert>

        <!-- Information -->
        <div class="space-y-2 text-sm">
          <p class="text-muted-foreground">
            重新生成后，系统将：
          </p>
          <ul class="list-disc list-inside space-y-1 text-muted-foreground">
            <li>使用最新的文档编辑内容</li>
            <li>重新执行 AI 分析和内容生成</li>
            <li>覆盖之前生成的投标书文件</li>
          </ul>
        </div>
      </div>

      <DialogFooter class="gap-2 sm:gap-0">
        <Button
          variant="outline"
          @click="handleCancel"
          :disabled="isLoading"
        >
          取消
        </Button>
        <Button
          variant="destructive"
          @click="handleConfirm"
          :disabled="isLoading"
        >
          <SafeIcon v-if="isLoading" name="Loader2" :size="16" class="mr-2 animate-spin" />
          {{ isLoading ? '处理中...' : '确认重新生成' }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
