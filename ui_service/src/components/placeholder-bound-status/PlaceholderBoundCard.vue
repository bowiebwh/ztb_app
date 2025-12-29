
<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import SafeIcon from '@/components/common/SafeIcon.vue'
import BoundMaterialPreview from './BoundMaterialPreview.vue'
import { cn } from '@/lib/utils'

interface PlaceholderStatus {
  key: string
  label: string
  type: 'image' | 'table'
  status: 'bound' | 'unbound'
  boundMaterial?: any
  boundNode?: any
}

interface Props {
  placeholder: PlaceholderStatus
  expanded: boolean
  isClient: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'toggle-expand': []
  'unbind': []
  'modify': []
}>()

const statusConfig = computed(() => {
  if (props.placeholder.status === 'bound') {
    return {
      icon: 'CheckCircle2',
      label: '已绑定',
      class: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    }
  }
  return {
    icon: 'AlertCircle',
    label: '未绑定',
    class: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400',
  }
})

const typeConfig = computed(() => {
  if (props.placeholder.type === 'image') {
    return { icon: 'Image', label: '图片' }
  }
  return { icon: 'Table2', label: '表格' }
})
</script>

<template>
  <Card
    :class="cn(
      'cursor-pointer transition-all duration-300',
      expanded && 'ring-2 ring-primary',
      (expanded || isClient) && 'shadow-card'
    )"
    @click="emit('toggle-expand')"
  >
    <!-- 卡片头部 -->
    <div class="p-4 flex items-center justify-between">
      <div class="flex items-center gap-4 flex-1">
        <!-- 类型图标 -->
        <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-muted flex items-center justify-center">
          <SafeIcon :name="typeConfig.icon" :size="20" class="text-muted-foreground" />
        </div>

        <!-- 占位符信息 -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h3 class="font-medium truncate">{{ placeholder.label }}</h3>
            <Badge :class="statusConfig.class" class="flex-shrink-0">
              <SafeIcon :name="statusConfig.icon" :size="12" class="mr-1" />
              {{ statusConfig.label }}
            </Badge>
          </div>
          <p class="text-xs text-muted-foreground">
            Key: {{ placeholder.key }} · 类型: {{ typeConfig.label }}
          </p>
        </div>
      </div>

      <!-- 展开按钮 -->
      <button
        class="flex-shrink-0 ml-2 p-2 hover:bg-muted rounded-lg transition-colors"
        @click.stop="emit('toggle-expand')"
        :aria-expanded="expanded"
      >
        <SafeIcon
          name="ChevronDown"
          :size="20"
          :class="cn(
            'transition-transform duration-300',
            expanded && 'rotate-180'
          )"
        />
      </button>
    </div>

    <!-- 展开内容 -->
    <div
      v-if="expanded || isClient"
      :class="cn(
        'overflow-hidden transition-all duration-300',
        expanded ? 'max-h-96' : 'max-h-0'
      )"
    >
      <div class="border-t px-4 py-4 space-y-4">
        <!-- 绑定材料预览 -->
        <div v-if="placeholder.status === 'bound' && placeholder.boundMaterial">
          <h4 class="text-sm font-medium mb-3">绑定的材料</h4>
          <BoundMaterialPreview
            :material="placeholder.boundMaterial"
            :bound-node="placeholder.boundNode"
          />
        </div>

        <!-- 未绑定提示 -->
        <div v-else class="bg-amber-50 dark:bg-amber-900/20 rounded-lg p-3 border border-amber-200 dark:border-amber-800">
          <div class="flex items-start gap-2">
            <SafeIcon name="AlertCircle" :size="16" class="text-amber-600 dark:text-amber-400 mt-0.5 flex-shrink-0" />
            <div class="text-sm text-amber-800 dark:text-amber-300">
              <p class="font-medium">此占位符尚未绑定材料</p>
              <p class="text-xs mt-1">请从材料库中选择合适的文件进行绑定</p>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-2 pt-2">
          <Button
            v-if="placeholder.status === 'bound'"
            variant="outline"
            size="sm"
            @click.stop="emit('unbind')"
          >
            <SafeIcon name="Trash2" :size="14" class="mr-1" />
            解除绑定
          </Button>
          <Button
            variant="outline"
            size="sm"
            @click.stop="emit('modify')"
          >
            <SafeIcon name="Edit2" :size="14" class="mr-1" />
            {{ placeholder.status === 'bound' ? '修改绑定' : '绑定材料' }}
          </Button>
        </div>
      </div>
    </div>
  </Card>
</template>
