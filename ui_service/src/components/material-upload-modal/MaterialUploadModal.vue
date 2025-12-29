
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

interface UploadingFile {
  id: string
  name: string
  size: number
  progress: number
  status: 'uploading' | 'success' | 'error'
  error?: string
}

interface Props {
  open: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'upload-complete': [files: UploadingFile[]]
}>()

const isClient = ref(true)
const isDragging = ref(false)
const uploadingFiles = ref<UploadingFile[]>([])
const fileInput = ref<HTMLInputElement>()

// 允许的文件类型
const ALLOWED_TYPES = {
  'Image': ['image/png', 'image/jpeg', 'image/jpg'],
  'PDF': ['application/pdf'],
  'Word': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'],
  'Excel': ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'],
}

const allAllowedTypes = computed(() => {
  return Object.values(ALLOWED_TYPES).flat()
})

const isUploading = computed(() => {
  return uploadingFiles.value.some(f => f.status === 'uploading')
})

const successCount = computed(() => {
  return uploadingFiles.value.filter(f => f.status === 'success').length
})

const errorCount = computed(() => {
  return uploadingFiles.value.filter(f => f.status === 'error').length
})

const getFileType = (file: File): string => {
  for (const [type, mimes] of Object.entries(ALLOWED_TYPES)) {
    if (mimes.includes(file.type)) {
      return type
    }
  }
  return 'Unknown'
}

const getFileIcon = (file: File): string => {
  const type = getFileType(file)
  const iconMap: Record<string, string> = {
    'Image': 'Image',
    'PDF': 'FileText',
    'Word': 'ScrollText',
    'Excel': 'LayoutGrid',
    'Unknown': 'File',
  }
  return iconMap[type] || 'File'
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

const validateFile = (file: File): { valid: boolean; error?: string } => {
  // 检查文件类型
  if (!allAllowedTypes.includes(file.type)) {
    return {
      valid: false,
      error: `不支持的文件类型: ${file.name}`,
    }
  }

  // 检查文件大小 (最大 100MB)
  const maxSize = 100 * 1024 * 1024
  if (file.size > maxSize) {
    return {
      valid: false,
      error: `文件过大: ${file.name} (最大 100MB)`,
    }
  }

  return { valid: true }
}

const simulateUpload = (file: UploadingFile) => {
  return new Promise<void>((resolve) => {
    let progress = 0
    const interval = setInterval(() => {
      progress += Math.random() * 30
      if (progress >= 100) {
        progress = 100
        file.progress = progress
        file.status = 'success'
        clearInterval(interval)
        resolve()
      } else {
        file.progress = progress
      }
    }, 300)
  })
}

const handleFiles = async (files: FileList | null) => {
  if (!files) return

  const newFiles: UploadingFile[] = []

  // 验证并添加文件
  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    const validation = validateFile(file)

    if (!validation.valid) {
      newFiles.push({
        id: `file-${Date.now()}-${i}`,
        name: file.name,
        size: file.size,
        progress: 0,
        status: 'error',
        error: validation.error,
      })
    } else {
      newFiles.push({
        id: `file-${Date.now()}-${i}`,
        name: file.name,
        size: file.size,
        progress: 0,
        status: 'uploading',
      })
    }
  }

  uploadingFiles.value.push(...newFiles)

  // 模拟上传
  for (const uploadFile of newFiles) {
    if (uploadFile.status === 'uploading') {
      await simulateUpload(uploadFile)
    }
  }
}

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = true
}

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = false
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragging.value = false

  if (e.dataTransfer?.files) {
    handleFiles(e.dataTransfer.files)
  }
}

const handleFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (input.files) {
    handleFiles(input.files)
  }
}

const handleClickUpload = () => {
  fileInput.value?.click()
}

const handleClearCompleted = () => {
  uploadingFiles.value = uploadingFiles.value.filter(f => f.status === 'uploading')
}

const handleConfirmUpload = () => {
  const successFiles = uploadingFiles.value.filter(f => f.status === 'success')
  if (successFiles.length > 0) {
    emit('upload-complete', successFiles)
    emit('update:open', false)
    uploadingFiles.value = []
  }
}

const handleOpenChange = (value: boolean) => {
  if (!value) {
    uploadingFiles.value = []
  }
  emit('update:open', value)
}

onMounted(() => {
  isClient.value = false
  requestAnimationFrame(() => {
    isClient.value = true
  })
})
</script>

<template>
  <Dialog :open="open" @update:open="handleOpenChange">
    <DialogContent class="max-w-2xl">
      <DialogHeader>
        <DialogTitle>上传材料文件</DialogTitle>
        <DialogDescription>
          支持上传图片、PDF、Word 和 Excel 文件，单个文件最大 100MB
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-6">
        <!-- 拖拽上传区域 -->
        <div
          v-if="isClient || uploadingFiles.length === 0"
          @dragover="handleDragOver"
          @dragleave="handleDragLeave"
          @drop="handleDrop"
          :class="cn(
            'border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer',
            isDragging
              ? 'border-primary bg-primary/5'
              : 'border-border hover:border-primary/50 hover:bg-muted/50'
          )"
          @click="handleClickUpload"
        >
          <input
            ref="fileInput"
            type="file"
            multiple
            :accept="Object.values(ALLOWED_TYPES).flat().join(',')"
            class="hidden"
            @change="handleFileSelect"
          />

          <div class="flex flex-col items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <SafeIcon name="Upload" :size="24" class="text-primary" />
            </div>
            <div>
              <p class="font-medium">拖拽文件到此处或点击选择</p>
              <p class="text-sm text-muted-foreground mt-1">
                支持 PNG、JPG、PDF、Word、Excel 格式
              </p>
            </div>
          </div>
        </div>

        <!-- 上传文件列表 -->
        <div v-if="uploadingFiles.length > 0" class="space-y-3 max-h-96 overflow-y-auto">
          <div class="flex items-center justify-between">
            <h4 class="font-medium text-sm">
              上传进度 ({{ successCount }} 成功
              <span v-if="errorCount > 0" class="text-destructive">{{ errorCount }} 失败</span>)
            </h4>
            <button
              v-if="!isUploading && uploadingFiles.some(f => f.status !== 'uploading')"
              @click="handleClearCompleted"
              class="text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              清除已完成
            </button>
          </div>

          <div class="space-y-2">
            <div
              v-for="file in uploadingFiles"
              :key="file.id"
              class="flex items-start gap-3 p-3 rounded-lg bg-muted/50"
            >
              <!-- 文件图标 -->
              <div class="flex-shrink-0 w-10 h-10 rounded bg-background flex items-center justify-center">
                <SafeIcon
                  :name="getFileIcon(new File([], file.name))"
                  :size="20"
                  class="text-muted-foreground"
                />
              </div>

              <!-- 文件信息 -->
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-2">
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium truncate">{{ file.name }}</p>
                    <p class="text-xs text-muted-foreground">{{ formatFileSize(file.size) }}</p>
                  </div>

                  <!-- 状态图标 -->
                  <div class="flex-shrink-0">
                    <SafeIcon
                      v-if="file.status === 'uploading'"
                      name="Loader2"
                      :size="16"
                      class="text-primary animate-spin"
                    />
                    <SafeIcon
                      v-else-if="file.status === 'success'"
                      name="CheckCircle2"
                      :size="16"
                      class="text-green-600"
                    />
                    <SafeIcon
                      v-else-if="file.status === 'error'"
                      name="XCircle"
                      :size="16"
                      class="text-destructive"
                    />
                  </div>
                </div>

                <!-- 进度条 -->
                <div v-if="file.status === 'uploading'" class="mt-2">
                  <Progress :value="file.progress" class="h-1" />
                  <p class="text-xs text-muted-foreground mt-1">{{ Math.round(file.progress) }}%</p>
                </div>

                <!-- 错误信息 -->
                <div v-if="file.status === 'error' && file.error" class="mt-2">
                  <p class="text-xs text-destructive">{{ file.error }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态提示 -->
        <div v-if="uploadingFiles.length === 0 && !isClient" class="text-center py-4 text-sm text-muted-foreground">
          还未选择文件
        </div>
      </div>

      <DialogFooter>
        <Button
          variant="outline"
          @click="() => emit('update:open', false)"
          :disabled="isUploading"
        >
          取消
        </Button>
        <Button
          @click="handleConfirmUpload"
          :disabled="successCount === 0 || isUploading"
        >
          <SafeIcon v-if="isUploading" name="Loader2" :size="16" class="mr-2 animate-spin" />
          {{ isUploading ? '上传中...' : `确认上传 (${successCount})` }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<style scoped>
/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--muted-foreground));
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--foreground));
}
</style>
