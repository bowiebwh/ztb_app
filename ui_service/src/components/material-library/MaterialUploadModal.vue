
<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import SafeIcon from '@/components/common/SafeIcon.vue'
import type { MaterialModel, MaterialType } from '@/src/data/materials'

interface Props {
  open: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'upload-success': [material: MaterialModel]
}>()

const fileInput = ref<HTMLInputElement>()
const uploadProgress = ref(0)
const isUploading = ref(false)
const uploadedFiles = ref<File[]>([])

const acceptedTypes = '.png,.jpg,.jpeg,.pdf,.doc,.docx,.xls,.xlsx'

const canUpload = computed(() => uploadedFiles.value.length > 0 && !isUploading.value)

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files) {
    uploadedFiles.value = Array.from(target.files)
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  if (e.dataTransfer?.files) {
    uploadedFiles.value = Array.from(e.dataTransfer.files)
  }
}

const getMaterialType = (file: File): MaterialType => {
  const ext = file.name.split('.').pop()?.toLowerCase()
  if (['png', 'jpg', 'jpeg'].includes(ext || '')) return 'Image'
  if (ext === 'pdf') return 'PDF'
  if (['doc', 'docx'].includes(ext || '')) return 'Word'
  if (['xls', 'xlsx'].includes(ext || '')) return 'Excel'
  return 'Image'
}

const handleUpload = async () => {
  if (uploadedFiles.value.length === 0) return

  isUploading.value = true
  uploadProgress.value = 0

  try {
    // Simulate upload progress
    const interval = setInterval(() => {
      uploadProgress.value += Math.random() * 30
      if (uploadProgress.value > 90) {
        uploadProgress.value = 90
      }
    }, 200)

    // Simulate API call delay
    await new Promise((resolve) => setTimeout(resolve, 2000))

    clearInterval(interval)
    uploadProgress.value = 100

    // Create mock material for each uploaded file
    for (const file of uploadedFiles.value) {
      const newMaterial: MaterialModel = {
        materialId: `mat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: getMaterialType(file),
        name: file.name,
        size: file.size,
        uploadTime: new Date().toISOString(),
        url: URL.createObjectURL(file),
        thumbnailUrl: file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined,
        iconName: getMaterialType(file) === 'Image' ? 'Image' : undefined,
      }
      emit('upload-success', newMaterial)
    }

    // Reset state
    setTimeout(() => {
      uploadedFiles.value = []
      uploadProgress.value = 0
      isUploading.value = false
      emit('update:open', false)
    }, 500)
  } catch (error) {
    console.error('Upload failed:', error)
    isUploading.value = false
    uploadProgress.value = 0
  }
}

const handleRemoveFile = (index: number) => {
  uploadedFiles.value.splice(index, 1)
}

const handleOpenChange = (value: boolean) => {
  if (!isUploading.value) {
    uploadedFiles.value = []
    uploadProgress.value = 0
    emit('update:open', value)
  }
}
</script>

<template>
  <Dialog :open="open" @update:open="handleOpenChange">
    <DialogContent class="max-w-md">
      <DialogHeader>
        <DialogTitle>上传文件</DialogTitle>
        <DialogDescription>
          支持上传图片、PDF、Word 和 Excel 文件
        </DialogDescription>
      </DialogHeader>

      <div class="space-y-4">
        <!-- Drop Zone -->
        <div
          class="border-2 border-dashed border-border rounded-lg p-6 text-center cursor-pointer hover:border-primary/50 transition-colors"
          @drop="handleDrop"
          @dragover.prevent
          @dragenter.prevent
          @click="fileInput?.click()"
        >
<SafeIcon name="Upload" :size="32" class="mx-auto mb-2 text-muted-foreground" />
          <p class="text-sm font-medium">拖拽文件到此或点击选择</p>
          <p class="text-xs text-muted-foreground mt-1">
            支持 PNG、JPG、PDF、DOC、XLS 等格式
          </p>
          <input
            ref="fileInput"
            type="file"
            multiple
            :accept="acceptedTypes"
            class="hidden"
            @change="handleFileSelect"
          />
        </div>

        <!-- File List -->
        <div v-if="uploadedFiles.length > 0" class="space-y-2">
          <p class="text-sm font-medium">已选择文件 ({{ uploadedFiles.length }})</p>
          <div class="space-y-1 max-h-40 overflow-y-auto">
            <div
              v-for="(file, index) in uploadedFiles"
              :key="index"
              class="flex items-center justify-between p-2 bg-muted rounded text-sm"
            >
              <div class="flex items-center gap-2 flex-1 min-w-0">
                <SafeIcon name="File" :size="16" class="flex-shrink-0" />
                <span class="truncate">{{ file.name }}</span>
              </div>
              <Button
                v-if="!isUploading"
                variant="ghost"
                size="sm"
                class="h-6 w-6 p-0"
                @click="handleRemoveFile(index)"
              >
                <SafeIcon name="X" :size="14" />
              </Button>
            </div>
          </div>
        </div>

        <!-- Progress -->
        <div v-if="isUploading" class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span>上传中...</span>
            <span class="text-muted-foreground">{{ Math.round(uploadProgress) }}%</span>
          </div>
          <Progress :value="uploadProgress" class="h-2" />
        </div>

        <!-- Actions -->
        <div class="flex gap-2 justify-end">
          <Button
            variant="outline"
            @click="handleOpenChange(false)"
            :disabled="isUploading"
          >
            取消
          </Button>
          <Button
            @click="handleUpload"
            :disabled="!canUpload"
          >
            <SafeIcon v-if="isUploading" name="Loader2" :size="16" class="animate-spin" />
            {{ isUploading ? '上传中' : '上传' }}
          </Button>
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>
