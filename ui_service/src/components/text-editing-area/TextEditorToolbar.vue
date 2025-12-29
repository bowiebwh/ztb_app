
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  viewMode: 'edit' | 'preview'
}

const emit = defineEmits<{
  'toggle-structure': []
  save: []
}>()
</script>

<template>
  <div class="border-b bg-muted/30 px-6 py-3 flex items-center gap-2">
    <!-- Structure Toggle -->
    <Button
      variant="ghost"
      size="sm"
      @click="emit('toggle-structure')"
      class="hover:bg-muted"
      title="切换文档结构面板"
    >
      <SafeIcon name="PanelLeft" :size="18" />
    </Button>

    <Separator orientation="vertical" class="h-6" />

    <!-- Text Formatting (only in edit mode) -->
    <template v-if="viewMode === 'edit'">
      <Button
        variant="ghost"
        size="sm"
        class="hover:bg-muted"
        title="加粗"
      >
        <SafeIcon name="Bold" :size="18" />
      </Button>
      <Button
        variant="ghost"
        size="sm"
        class="hover:bg-muted"
        title="斜体"
      >
        <SafeIcon name="Italic" :size="18" />
      </Button>
      <Button
        variant="ghost"
        size="sm"
        class="hover:bg-muted"
        title="下划线"
      >
        <SafeIcon name="Underline" :size="18" />
      </Button>

      <Separator orientation="vertical" class="h-6" />

      <Button
        variant="ghost"
        size="sm"
        class="hover:bg-muted"
        title="项目符号列表"
      >
        <SafeIcon name="List" :size="18" />
      </Button>
      <Button
        variant="ghost"
        size="sm"
        class="hover:bg-muted"
        title="编号列表"
      >
        <SafeIcon name="ListOrdered" :size="18" />
      </Button>
    </template>

    <div class="flex-1" />

    <!-- Save Button -->
    <Button
      size="sm"
      @click="emit('save')"
      class="gap-2"
    >
      <SafeIcon name="Save" :size="16" />
      保存
    </Button>
  </div>
</template>
