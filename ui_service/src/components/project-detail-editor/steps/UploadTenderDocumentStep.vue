<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { Project } from '@/lib/api'
import { uploadFile } from '@/lib/api'

interface Props {
  projectId: string
  project: Project | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'step-change': [stepId: string]
}>()

const isDragging = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const uploadedFile = ref<File | null>(null)
const fileInputRef = ref<HTMLInputElement | null>(null)
const uploadError = ref('')
const timerId = ref<number | null>(null)

const canProceed = computed(() => !isUploading.value && !!uploadedFile.value)

const clearTimer = () => {
  if (timerId.value !== null) {
    clearInterval(timerId.value)
    timerId.value = null
  }
}

const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    handleFileSelect(files[0])
  }
}

const handleFileSelect = (file: File) => {
  uploadedFile.value = file
  uploadError.value = ''
  simulateUpload()
}

const simulateUpload = async () => {
  if (!uploadedFile.value) return
  isUploading.value = true
  uploadProgress.value = 0
  uploadError.value = ''
  clearTimer()

  timerId.value = window.setInterval(() => {
    uploadProgress.value = Math.min(uploadProgress.value + Math.random() * 20, 90)
  }, 200)

  try {
    await uploadFile(uploadedFile.value, props.projectId)
    uploadProgress.value = 100
  } catch (error) {
    console.error('文件上传失败', error)
    uploadError.value = '文件上传失败，请重试或更换文件'
    uploadProgress.value = 0
    uploadedFile.value = null
  } finally {
    clearTimer()
    isUploading.value = false
  }
}

const handleInputChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    handleFileSelect(input.files[0])
  }
}

const triggerSelect = () => {
  fileInputRef.value?.click()
}

const goBackToList = () => {
  window.location.href = '/project-list.html'
}

const handleNextStep = () => {
  if (!canProceed.value) {
    uploadError.value = '请先选择并上传招标文件'
    return
  }
  uploadError.value = ''
  try {
    if (typeof window !== 'undefined') {
      window.sessionStorage.setItem('autoRunAnalysis', '1')
    }
  } catch {
    // ignore storage failures
  }
  emit('step-change', 'analyze_tender_content_step')
}

const formatSize = (bytes: number) => (bytes / 1024 / 1024).toFixed(2)

onBeforeUnmount(() => {
  clearTimer()
})
</script>

<template>
  <div class="space-y-6">
    <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
      <div class="flex gap-3">
        <SafeIcon name="Info" :size="20" class="text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
        <div class="text-sm text-blue-900 dark:text-blue-300">
          <p class="font-medium mb-1">上传招标文件</p>
          <p>请上传招标说明书或招标文件（PDF、Word 等格式），系统将对其进行 AI 解析。</p>
        </div>
      </div>
    </div>

    <div
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
      :class="[
        'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
        isDragging ? 'border-primary bg-primary/5' : 'border-border',
        isUploading ? 'opacity-50 pointer-events-none' : ''
      ]"
    >
      <div class="flex flex-col items-center gap-4">
        <div class="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
          <SafeIcon name="Upload" :size="32" class="text-muted-foreground" />
        </div>
        
        <div>
          <p class="text-lg font-semibold mb-1">拖拽文件到此处</p>
          <p class="text-sm text-muted-foreground">或点击下方按钮选择文件</p>
        </div>

        <input
          type="file"
          id="file-input"
          accept=".pdf,.doc,.docx,.txt"
          @change="handleInputChange"
          ref="fileInputRef"
          class="hidden"
        />
        
        <Button
          @click="triggerSelect"
          :disabled="isUploading"
        >
          <SafeIcon name="Plus" :size="16" class="mr-2" />
          选择文件
        </Button>
      </div>
    </div>

    <div v-if="isUploading" class="space-y-2">
      <div class="flex items-center justify-between text-sm">
        <span>上传进度</span>
        <span class="font-medium">{{ Math.round(uploadProgress) }}%</span>
      </div>
      <div class="w-full bg-muted rounded-full h-2 overflow-hidden">
        <div
          class="bg-primary h-full transition-all duration-300"
          :style="{ width: `${uploadProgress}%` }"
        />
      </div>
    </div>

    <div v-if="uploadError" class="text-sm text-red-500">{{ uploadError }}</div>

    <div v-if="!isUploading && uploadedFile" class="bg-card border rounded-lg p-4">
      <div class="flex items-start gap-3">
        <div class="w-10 h-10 rounded bg-red-100 dark:bg-red-900/30 flex items-center justify-center flex-shrink-0">
          <SafeIcon name="FileText" :size="20" class="text-red-600 dark:text-red-400" />
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-medium text-sm">{{ uploadedFile?.name }}</p>
          <p class="text-xs text-muted-foreground mt-1">
            大小：{{ formatSize(uploadedFile?.size || 0) }} MB
          </p>
        </div>
        <button
          @click="uploadedFile = null"
          class="p-1 hover:bg-muted rounded transition-colors flex-shrink-0"
          aria-label="删除文件"
        >
          <SafeIcon name="X" :size="18" />
        </button>
      </div>
    </div>

    <div class="flex gap-3 justify-end pt-4 border-t">
      <Button variant="outline" type="button" @click="goBackToList">
        返回项目列表
      </Button>
      <Button
        @click="handleNextStep"
        :disabled="!canProceed"
      >
        下一步：招标内容解析
        <SafeIcon name="ArrowRight" :size="16" class="ml-2" />
      </Button>
    </div>
  </div>
</template>
