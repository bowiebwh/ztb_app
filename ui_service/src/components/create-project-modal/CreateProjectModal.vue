
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { z } from 'zod'
import { toast } from 'vue-sonner'
import { createProject } from '@/lib/api'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

// 表单验证 schema
const createProjectSchema = z.object({
  projectName: z
    .string()
    .min(1, '项目名称不能为空')
    .min(2, '项目名称至少需要 2 个字符')
    .max(100, '项目名称不能超过 100 个字符'),
})

type CreateProjectFormValues = z.infer<typeof createProjectSchema>

const isClient = ref(true)
const isOpen = ref(true)
const isLoading = ref(false)

const { handleSubmit, values } = useForm<CreateProjectFormValues>({
  validationSchema: createProjectSchema,
  initialValues: {
    projectName: '',
  },
})

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  try {
    await createProject({ projectName: values.projectName })
    toast.success(`项目 "${values.projectName}" 创建成功！`)
    isOpen.value = false
    setTimeout(() => {
      if (typeof window !== 'undefined') {
        window.location.href = './project-list.html'
      }
    }, 500)
  } catch (error) {
    console.error('创建项目失败:', error)
    toast.error('创建项目失败，请重试')
  } finally {
    isLoading.value = false
  }
})

const handleCancel = () => {
  isOpen.value = false
  setTimeout(() => {
    if (typeof window !== 'undefined') {
      window.location.href = './project-list.html'
    }
  }, 300)
}

const handleOpenChange = (open: boolean) => {
  if (!open) {
    handleCancel()
  }
}

onMounted(() => {
  // 确保模态框在客户端打开
  isClient.value = true
})
</script>

<template>
  <Dialog :open="isOpen && isClient" @update:open="handleOpenChange">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>创建新项目</DialogTitle>
        <DialogDescription>
          输入项目名称以创建新的招投标项目
        </DialogDescription>
      </DialogHeader>

      <Form @submit="onSubmit" class="space-y-6">
        <FormField v-slot="{ componentField }" name="projectName">
          <FormItem>
            <FormLabel>项目名称</FormLabel>
            <FormControl>
              <Input
                v-bind="componentField"
                placeholder="例如：智捷云招投标系统采购项目"
                :disabled="isLoading"
                @keydown.enter="onSubmit"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <div class="flex gap-3 justify-end">
          <Button
            type="button"
            variant="outline"
            @click="handleCancel"
            :disabled="isLoading"
          >
            取消
          </Button>
          <Button
            type="submit"
            :disabled="isLoading"
            :class="isLoading && 'opacity-70'"
          >
            {{ isLoading ? '创建中...' : '创建' }}
          </Button>
        </div>
      </Form>
    </DialogContent>
  </Dialog>
</template>
