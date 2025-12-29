
<script setup lang="ts">
import { computed } from 'vue'
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'
import { cn } from '@/lib/utils'

interface UploadedFile {
  id: string
  name: string
  size: number
  type: string
  uploadedAt: string
  status: 'success' | 'uploading' | 'failed'
  progress?: number
}

interface Props {
  files: UploadedFile[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  remove: [fileId: string]
}>()

const getFileIcon = (type: string) => {
  const iconMap: Record<string, string> = {
    pdf: 'FileText',
    doc: 'FileText',
    docx: 'FileText',
    xls: 'FileText',
    xlsx: 'FileText',
    txt: 'FileText',
  }
  return iconMap[type.toLowerCase()] || 'File'
}

const getFileColor = (type: string) => {
  const colorMap: Record<string, string> = {
    pdf: 'text-red-500',
    doc: 'text-blue-500',
    docx: 'text-blue-500',
    xls: 'text-green-500',
    xlsx: 'text-green-500',
    txt: 'text-gray-500',
  }
  return colorMap[type.toLowerCase()] || 'text-gray-500'
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

const getStatusIcon = (status: string) => {
  const iconMap: Record<string, string> = {
    success: 'CheckCircle2',
    uploading: 'Loader2',
    failed: 'XCircle',
  }
  return iconMap[status] || 'File'
}

const getStatusColor = (status: string) => {
  const colorMap: Record<string, string> = {
    success: 'text-green-600',
    uploading: 'text-blue-600 animate-spin',
    failed: 'text-red-600',
  }
  return colorMap[status] || 'text-gray-600'
}
</script>

<template>
  <div class="space-y-2">
    <div
      v-for="file in files"
      :key="file.id"
      class="flex items-center justify-between p-4 rounded-lg border bg-card hover:bg-muted/50 transition-colors group"
    >
      <!-- File Info -->
      <div class="flex items-center gap-3 flex-1 min-w-0">
        <SafeIcon
          :name="getFileIcon(file.type)"
          :size="20"
          :class="getFileColor(file.type)"
        />

        <div class="flex-1 min-w-0">
          <p class="font-medium text-sm truncate">{{ file.name }}</p>
          <p class="text-xs text-muted-foreground">
            {{ formatFileSize(file.size) }} · {{ file.uploadedAt }}
          </p>
        </div>
      </div>

      <!-- Status -->
      <div class="flex items-center gap-3 ml-4">
        <SafeIcon
          :name="getStatusIcon(file.status)"
          :size="18"
          :class="getStatusColor(file.status)"
        />

        <Button
          variant="ghost"
          size="sm"
          @click="emit('remove', file.id)"
          class="opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <SafeIcon name="Trash2" :size="16" />
        </Button>
      </div>
    </div>
  </div>
</template>
