
<script setup lang="ts">
import { ref } from 'vue'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Card, CardContent } from '@/components/ui/card'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface GenerationConfig {
  language: 'zh' | 'en'
  scope: 'all' | 'technical' | 'commercial'
  format: 'word'
}

const config = ref<GenerationConfig>({
  language: 'zh',
  scope: 'all',
  format: 'word',
})

// 语言选项
const languageOptions = [
  { value: 'zh', label: '中文', description: '生成中文版本的投标书' },
  { value: 'en', label: '英文', description: '生成英文版本的投标书' },
]

// 范围选项
const scopeOptions = [
  { value: 'all', label: '全部', description: '包含技术标和商务标的完整投标书' },
  { value: 'technical', label: '技术标', description: '仅包含技术方案部分' },
  { value: 'commercial', label: '商务标', description: '仅包含商务条款部分' },
]

// 格式选项（当前仅支持 Word）
const formatOptions = [
  { value: 'word', label: 'Word (.docx)', description: '标准 Microsoft Word 格式，可直接提交' },
]
</script>

<template>
  <div class="space-y-8">
    <!-- Language Selection -->
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <SafeIcon name="Globe" :size="18" class="text-primary" />
        <Label class="text-base font-semibold">输出语言</Label>
      </div>
      <RadioGroup v-model="config.language">
        <div class="space-y-3">
          <div
            v-for="option in languageOptions"
            :key="option.value"
            class="flex items-start space-x-3 p-3 rounded-lg border border-transparent hover:border-border hover:bg-muted/50 transition-colors cursor-pointer"
            @click="config.language = option.value as any"
          >
            <RadioGroupItem :value="option.value" :id="`lang-${option.value}`" class="mt-1" />
            <div class="flex-1">
              <Label :for="`lang-${option.value}`" class="font-medium cursor-pointer">
                {{ option.label }}
              </Label>
              <p class="text-sm text-muted-foreground mt-0.5">
                {{ option.description }}
              </p>
            </div>
          </div>
        </div>
      </RadioGroup>
    </div>

    <!-- Scope Selection -->
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <SafeIcon name="FileText" :size="18" class="text-primary" />
        <Label class="text-base font-semibold">输出范围</Label>
      </div>
      <RadioGroup v-model="config.scope">
        <div class="space-y-3">
          <div
            v-for="option in scopeOptions"
            :key="option.value"
            class="flex items-start space-x-3 p-3 rounded-lg border border-transparent hover:border-border hover:bg-muted/50 transition-colors cursor-pointer"
            @click="config.scope = option.value as any"
          >
            <RadioGroupItem :value="option.value" :id="`scope-${option.value}`" class="mt-1" />
            <div class="flex-1">
              <Label :for="`scope-${option.value}`" class="font-medium cursor-pointer">
                {{ option.label }}
              </Label>
              <p class="text-sm text-muted-foreground mt-0.5">
                {{ option.description }}
              </p>
            </div>
          </div>
        </div>
      </RadioGroup>
    </div>

    <!-- Format Selection -->
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <SafeIcon name="Package" :size="18" class="text-primary" />
        <Label class="text-base font-semibold">输出格式</Label>
      </div>
      <RadioGroup v-model="config.format">
        <div class="space-y-3">
          <div
            v-for="option in formatOptions"
            :key="option.value"
            class="flex items-start space-x-3 p-3 rounded-lg border border-transparent hover:border-border hover:bg-muted/50 transition-colors cursor-pointer"
            @click="config.format = option.value as any"
          >
            <RadioGroupItem :value="option.value" :id="`format-${option.value}`" class="mt-1" />
            <div class="flex-1">
              <Label :for="`format-${option.value}`" class="font-medium cursor-pointer">
                {{ option.label }}
              </Label>
              <p class="text-sm text-muted-foreground mt-0.5">
                {{ option.description }}
              </p>
            </div>
          </div>
        </div>
      </RadioGroup>
    </div>

    <!-- Configuration Summary -->
    <Card class="bg-muted/50">
      <CardContent class="pt-6">
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-muted-foreground">输出语言：</span>
            <span class="font-medium">
              {{ languageOptions.find(o => o.value === config.language)?.label }}
            </span>
          </div>
          <div class="flex justify-between">
            <span class="text-muted-foreground">输出范围：</span>
            <span class="font-medium">
              {{ scopeOptions.find(o => o.value === config.scope)?.label }}
            </span>
          </div>
          <div class="flex justify-between">
            <span class="text-muted-foreground">输出格式：</span>
            <span class="font-medium">
              {{ formatOptions.find(o => o.value === config.format)?.label }}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
