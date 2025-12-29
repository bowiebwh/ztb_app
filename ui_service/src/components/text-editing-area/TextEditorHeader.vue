
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  title: string
  viewMode: 'edit' | 'preview'
}

const emit = defineEmits<{
  'update:view-mode': [value: 'edit' | 'preview']
  back: []
}>()
</script>

<template>
  <div class="border-b bg-background px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-4">
      <Button
        variant="ghost"
        size="icon"
        @click="emit('back')"
        class="hover:bg-muted"
      >
        <SafeIcon name="ArrowLeft" :size="20" />
      </Button>
      <div>
        <h2 class="text-lg font-semibold">{{ title }}</h2>
        <p class="text-xs text-muted-foreground">结构化文本编辑</p>
      </div>
    </div>

    <Tabs :value="viewMode" @update:value="emit('update:view-mode', $event as 'edit' | 'preview')">
      <TabsList class="grid w-full grid-cols-2">
        <TabsTrigger value="edit" class="flex items-center gap-2">
          <SafeIcon name="Edit" :size="16" />
          编辑
        </TabsTrigger>
        <TabsTrigger value="preview" class="flex items-center gap-2">
          <SafeIcon name="Eye" :size="16" />
          预览
        </TabsTrigger>
      </TabsList>
    </Tabs>
  </div>
</template>
