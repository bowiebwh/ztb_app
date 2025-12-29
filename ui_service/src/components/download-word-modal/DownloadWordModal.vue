
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'

interface DownloadInfo {
  fileName: string
  fileSize: string
  projectName: string
}

// 模拟数据
const mockDownloadInfo: DownloadInfo = {
  fileName: '智标助手_投标文件_2024.docx',
  fileSize: '2.5 MB',
  projectName: '某某项目投标文件',
}

const isClient = ref(true)
const open = ref(true)
const isDownloading = ref(false)
const downloadProgress = ref(0)
const downloadComplete = ref(false)
const downloadError = ref(false)

const downloadInfo = ref<DownloadInfo>(mockDownloadInfo)

const downloadButtonText = computed(() => {
  if (downloadComplete.value) return '下载完成'
  if (isDownloading.value) return `下载中 (${downloadProgress.value}%)`
  return '确认下载'
})

const downloadButtonDisabled = computed(() => {
  return isDownloading.value || downloadComplete.value
})

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})

const handleDownload = async () => {
  isDownloading.value = true
  downloadProgress.value = 0
  downloadError.value = false

  try {
    // 模拟下载进度
    const progressInterval = setInterval(() => {
      downloadProgress.value += Math.random() * 30
      if (downloadProgress.value >= 100) {
        downloadProgress.value = 100
        clearInterval(progressInterval)
      }
    }, 300)

    // 模拟下载延迟
    await new Promise(resolve => setTimeout(resolve, 2000))

    downloadProgress.value = 100
    downloadComplete.value = true
    isDownloading.value = false

    // 模拟实际下载（在真实应用中调用后端API）
    // const response = await fetch('/api/download-word', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ projectId: '...' })
    // })
    // const blob = await response.blob()
    // const url = window.URL.createObjectURL(blob)
    // const a = document.createElement('a')
    // a.href = url
    // a.download = downloadInfo.value.fileName
    // a.click()
    // window.URL.revokeObjectURL(url)

    // 延迟关闭对话框
    setTimeout(() => {
      handleClose()
    }, 1500)
  } catch (error) {
    console.error('下载失败:', error)
    downloadError.value = true
    isDownloading.value = false
  }
}

const handleRetry = () => {
  downloadProgress.value = 0
  downloadComplete.value = false
  downloadError.value = false
  handleDownload()
}

const handleClose = () => {
  open.value = false
  // 返回到投标书预览页面
  if (typeof window !== 'undefined') {
    window.location.href = './bid-document-preview.html'
  }
}

const handleCancel = () => {
  if (!isDownloading.value) {
    handleClose()
  }
}
</script>

<template>
  <Dialog :open="open" @update:open="handleCancel">
    <DialogContent class="sm:max-w-md">
      <!-- 下载成功状态 -->
      <template v-if="downloadComplete && !downloadError">
        <DialogHeader class="text-center">
          <div class="flex justify-center mb-4">
            <div class="w-16 h-16 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
              <SafeIcon name="CheckCircle2" :size="32" class="text-green-600 dark:text-green-400" />
            </div>
          </div>
          <DialogTitle>下载完成</DialogTitle>
          <DialogDescription>
            您的投标文件已成功下载
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-3 py-4">
          <div class="bg-muted rounded-lg p-3">
            <div class="flex items-start gap-3">
              <SafeIcon name="FileText" :size="20" class="text-primary mt-0.5 flex-shrink-0" />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium truncate">{{ downloadInfo.fileName }}</p>
                <p class="text-xs text-muted-foreground">{{ downloadInfo.fileSize }}</p>
              </div>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" @click="handleClose" class="w-full">
            关闭
          </Button>
        </DialogFooter>
      </template>

      <!-- 下载失败状态 -->
      <template v-else-if="downloadError">
        <DialogHeader class="text-center">
          <div class="flex justify-center mb-4">
            <div class="w-16 h-16 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
              <SafeIcon name="AlertCircle" :size="32" class="text-red-600 dark:text-red-400" />
            </div>
          </div>
          <DialogTitle>下载失败</DialogTitle>
          <DialogDescription>
            文件下载过程中出现错误，请重试
          </DialogDescription>
        </DialogHeader>

        <DialogFooter class="gap-2">
          <Button variant="outline" @click="handleCancel">
            取消
          </Button>
          <Button @click="handleRetry">
            重试
          </Button>
        </DialogFooter>
      </template>

      <!-- 下载进行中状态 -->
      <template v-else-if="isDownloading">
        <DialogHeader>
          <DialogTitle>下载文件</DialogTitle>
          <DialogDescription>
            正在下载您的投标文件...
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-4 py-4">
          <!-- 文件信息 -->
          <div class="bg-muted rounded-lg p-3">
            <div class="flex items-start gap-3">
              <SafeIcon name="FileText" :size="20" class="text-primary mt-0.5 flex-shrink-0" />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium truncate">{{ downloadInfo.fileName }}</p>
                <p class="text-xs text-muted-foreground">{{ downloadInfo.fileSize }}</p>
              </div>
            </div>
          </div>

          <!-- 进度条 -->
          <div class="space-y-2">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium">下载进度</span>
              <span class="text-sm text-muted-foreground">{{ downloadProgress }}%</span>
            </div>
            <Progress :value="downloadProgress" class="h-2" />
          </div>

          <!-- 提示信息 -->
          <p class="text-xs text-muted-foreground text-center">
            请勿关闭此窗口，下载进行中...
          </p>
        </div>

        <DialogFooter>
          <Button variant="outline" disabled class="w-full">
            <SafeIcon name="Loader2" :size="16" class="mr-2 animate-spin" />
            下载中...
          </Button>
        </DialogFooter>
      </template>

      <!-- 初始确认状态 -->
      <template v-else>
        <DialogHeader>
          <DialogTitle>下载投标文件</DialogTitle>
          <DialogDescription>
            确认下载已生成的投标文件
          </DialogDescription>
        </DialogHeader>

        <div class="space-y-4 py-4">
          <!-- 项目信息 -->
          <div class="bg-muted rounded-lg p-3">
            <div class="space-y-2">
              <div class="flex justify-between items-start">
                <span class="text-sm text-muted-foreground">项目名称</span>
                <span class="text-sm font-medium text-right">{{ downloadInfo.projectName }}</span>
              </div>
              <div class="flex justify-between items-start">
                <span class="text-sm text-muted-foreground">文件名</span>
                <span class="text-sm font-medium text-right truncate ml-2">{{ downloadInfo.fileName }}</span>
              </div>
              <div class="flex justify-between items-start">
                <span class="text-sm text-muted-foreground">文件大小</span>
                <span class="text-sm font-medium">{{ downloadInfo.fileSize }}</span>
              </div>
            </div>
          </div>

          <!-- 提示信息 -->
          <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 flex gap-2">
            <SafeIcon name="Info" :size="16" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <p class="text-xs text-blue-700 dark:text-blue-300">
              下载的文件将保存到您的默认下载文件夹中
            </p>
          </div>
        </div>

        <DialogFooter class="gap-2">
          <Button variant="outline" @click="handleCancel">
            取消
          </Button>
          <Button @click="handleDownload" :disabled="downloadButtonDisabled">
            <SafeIcon v-if="!isDownloading" name="Download" :size="16" class="mr-2" />
            {{ downloadButtonText }}
          </Button>
        </DialogFooter>
      </template>
    </DialogContent>
  </Dialog>
</template>
