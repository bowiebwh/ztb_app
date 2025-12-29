
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { cn } from '@/lib/utils'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { Progress } from '@/components/ui/progress'

interface Props {
  isUploading?: boolean
  progress?: number
}

const props = withDefaults(defineProps<Props>(), {
  isUploading: false,
  progress: 0,
})

const emit = defineEmits<{
  upload: [files: File[]]
}>()

const isDragOver = ref(false)
const isClient = ref(true)

onMounted(() => {
  isClient.value = false
  setTimeout(() => {
    isClient.value = true
  }, 0)
})

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragOver.value = true
}

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragOver.value = false
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragOver.value = false

  const files = Array.from(e.dataTransfer?.files || [])
  if (files.length > 0) {
    emit('upload', files)
  }
}

const handleFileInput = (e: Event) => {
  const input = e.target as HTMLInputElement
  const files = Array.from(input.files || [])
  if (files.length > 0) {
    emit('upload', files)
  }
  // Reset input
  input.value = ''
}

const handleClick = () => {
  const input = document.getElementById('file-input') as HTMLInputElement
  input?.click()
}
</script>

<template>
  <div class="space-y-4">
    <!-- Upload Area -->
    <div
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
      @click="handleClick"
      :class="cn(
        'relative border-2 border-dashed rounded-lg p-8 transition-all cursor-pointer',
        isDragOver && 'border-primary bg-primary/5',
        !isDragOver && 'border-border hover:border-primary/50 hover:bg-muted/50',
        isUploading && 'pointer-events-none opacity-60'
      )"
    >
      <input
        id="file-input"
        type="file"
        multiple
        class="hidden"
        accept=".pdf,.doc,.docx,.xls,.xlsx"
        @change="handleFileInput"
      />

      <div class="flex flex-col items-center justify-center gap-4">
        <div
          :class="cn(
            'w-16 h-16 rounded-full flex items-center justify-center transition-colors',
            isDragOver ? 'bg-primary/20 text-primary' : 'bg-muted text-muted-foreground'
          )"
        >
          <SafeIcon
            :name="isDragOver ? 'Upload' : 'Cloud'"
            :size="32"
          />
        </div>

        <div class="text-center">
          <p class="font-semibold text-foreground">
            {{ isDragOver ? '释放鼠标上传文件' : '拖拽文件到此处或点击选择' }}
          </p>
          <p class="text-sm text-muted-foreground mt-1">
            支持 PDF、Word、Excel 等格式
          </p>
        </div>
      </div>
    </div>

    <!-- Upload Progress -->
    <div v-if="isUploading || isClient" class="space-y-2">
      <div class="flex items-center justify-between">
        <span class="text-sm font-medium">上传进度</span>
        <span class="text-sm text-muted-foreground">{{ Math.round(progress) }}%</span>
      </div>
      <Progress :value="progress" class="h-2" />
    </div>
  </div>
</template>
