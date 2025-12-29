
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { MaterialModel } from '@/data/materials'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import SafeIcon from '@/components/common/SafeIcon.vue'
import MaterialItem from './MaterialItem.vue'

interface Props {
  materials: MaterialModel[]
  draggedMaterial: string | null
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'material-drag-start': [materialId: string]
  'material-drag-end': []
}>()

const searchQuery = ref('')
const selectedType = ref<'all' | 'Image' | 'PDF' | 'Word' | 'Excel'>('all')

const filteredMaterials = computed(() => {
  return props.materials.filter(material => {
    const matchesSearch = material.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesType = selectedType.value === 'all' || material.type === selectedType.value
    return matchesSearch && matchesType
  })
})

const materialsByType = computed(() => {
  const types = ['Image', 'PDF', 'Word', 'Excel'] as const
  return types.map(type => ({
    type,
    count: props.materials.filter(m => m.type === type).length,
  }))
})
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- 标题 -->
    <div class="border-b bg-card p-4">
      <h3 class="text-sm font-semibold text-sidebar-foreground flex items-center gap-2">
        <SafeIcon name="Library" :size="16" />
        材料库
      </h3>
    </div>

    <!-- 搜索和上传 -->
    <div class="border-b bg-card p-3 space-y-2">
      <Input
        v-model="searchQuery"
        placeholder="搜索材料..."
        class="h-8 text-sm"
      />
      <Button size="sm" class="w-full" variant="outline">
        <SafeIcon name="Upload" :size="14" />
        上传文件
      </Button>
    </div>

    <!-- 分类标签 -->
    <div class="border-b bg-card p-3">
      <Tabs v-model="selectedType" class="w-full">
        <TabsList class="grid w-full grid-cols-5 h-8">
          <TabsTrigger value="all" class="text-xs">全部</TabsTrigger>
          <TabsTrigger value="Image" class="text-xs">图片</TabsTrigger>
          <TabsTrigger value="PDF" class="text-xs">PDF</TabsTrigger>
          <TabsTrigger value="Word" class="text-xs">Word</TabsTrigger>
          <TabsTrigger value="Excel" class="text-xs">Excel</TabsTrigger>
        </TabsList>
      </Tabs>
    </div>

    <!-- 材料列表 -->
    <ScrollArea class="flex-1">
      <div class="p-3 space-y-2">
        <template v-if="filteredMaterials.length > 0">
          <MaterialItem
            v-for="material in filteredMaterials"
            :key="material.materialId"
            :material="material"
            :is-dragging="draggedMaterial === material.materialId"
            @drag-start="emit('material-drag-start', material.materialId)"
            @drag-end="emit('material-drag-end')"
          />
        </template>
        <div v-else class="flex flex-col items-center justify-center py-8 text-center">
          <SafeIcon name="Inbox" :size="24" class="text-muted-foreground mb-2" />
          <p class="text-xs text-muted-foreground">暂无材料</p>
        </div>
      </div>
    </ScrollArea>
  </div>
</template>
