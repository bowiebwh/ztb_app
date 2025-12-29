
<script setup lang="ts">
import { ref } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { GENERATION_OUTPUT_SCOPES, DEFAULT_GENERATION_CONFIG } from '@/data/config'
import type { GenerationConfigModel, OutputScope, Locale } from '@/data/config'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  visible?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  visible: true,
})

const emit = defineEmits<{
  'start-generation': []
  back: []
}>()

const config = ref<GenerationConfigModel>({ ...DEFAULT_GENERATION_CONFIG })
const isLoading = ref(false)

const languageOptions = [
  { value: 'zh-CN', label: '中文' },
  { value: 'en-US', label: '英文' },
]

const handleStartGeneration = async () => {
  isLoading.value = true
  // 模拟API调用延迟
  setTimeout(() => {
    isLoading.value = false
    emit('start-generation')
  }, 500)
}

const handleBack = () => {
  emit('back')
}
</script>

<template>
  <div v-if="visible" class="space-y-6">
    <!-- 配置卡片 -->
    <Card>
      <CardHeader>
        <CardTitle>生成配置</CardTitle>
        <CardDescription>选择投标书的输出选项</CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <!-- 输出语言 -->
        <div class="space-y-2">
          <Label for="language">输出语言</Label>
          <Select v-model="config.outputLanguage">
            <SelectTrigger id="language">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem
                v-for="lang in languageOptions"
                :key="lang.value"
                :value="lang.value"
              >
                {{ lang.label }}
              </SelectItem>
            </SelectContent>
          </Select>
          <p class="text-xs text-muted-foreground">
            选择投标书的输出语言
          </p>
        </div>

        <!-- 输出范围 -->
        <div class="space-y-2">
          <Label for="scope">输出范围</Label>
          <Select v-model="config.outputScope">
            <SelectTrigger id="scope">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem
                v-for="scope in GENERATION_OUTPUT_SCOPES"
                :key="scope.key"
                :value="scope.key"
              >
                {{ scope.label }}
              </SelectItem>
            </SelectContent>
          </Select>
          <p class="text-xs text-muted-foreground">
            选择要包含在投标书中的内容范围
          </p>
        </div>

        <!-- 输出格式 -->
        <div class="space-y-2">
          <Label for="format">输出格式</Label>
          <div
            id="format"
            class="px-3 py-2 border rounded-md bg-muted text-muted-foreground text-sm"
          >
            Word (.docx)
          </div>
          <p class="text-xs text-muted-foreground">
            目前仅支持Word格式输出
          </p>
        </div>
      </CardContent>
    </Card>

    <!-- 提示信息 -->
    <Card class="border-amber-200 bg-amber-50 dark:border-amber-900/30 dark:bg-amber-900/10">
      <CardContent class="pt-6">
        <div class="flex gap-3">
          <SafeIcon name="AlertCircle" :size="20" class="text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
          <div class="text-sm text-amber-800 dark:text-amber-300">
            <p class="font-medium mb-1">生成前检查清单</p>
            <ul class="list-disc list-inside space-y-1 text-xs">
              <li>所有占位符已绑定素材</li>
              <li>文档内容已完整编辑</li>
              <li>招标文件已成功上传和解析</li>
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- 操作按钮 -->
    <div class="flex gap-3 justify-end">
      <Button
        variant="outline"
        @click="handleBack"
        :disabled="isLoading"
      >
        返回编辑
      </Button>
      <Button
        @click="handleStartGeneration"
        :disabled="isLoading"
      >
        <SafeIcon v-if="isLoading" name="Loader2" :size="16" class="mr-2 animate-spin" />
        {{ isLoading ? '生成中...' : '开始生成投标书' }}
      </Button>
    </div>
  </div>
</template>
