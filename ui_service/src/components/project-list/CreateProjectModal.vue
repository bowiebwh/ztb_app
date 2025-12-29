<script setup lang="ts">
import { ref, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { createProject } from '@/lib/api'

interface Props {
  open: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  close: []
}>()

const isSubmitting = ref(false)

const validationSchema = toTypedSchema(
  z.object({
    projectName: z
      .string()
      .min(1, '项目名称不能为空')
      .min(2, '项目名称至少需要2个字符')
      .max(100, '项目名称不能超过100个字符'),
  })
)

const { handleSubmit, resetForm } = useForm({
  validationSchema,
  initialValues: {
    projectName: '',
  },
})

watch(
  () => props.open,
  (newVal) => {
    if (newVal) {
      resetForm()
    }
  }
)

const onSubmit = handleSubmit(async (formValues) => {
  isSubmitting.value = true
  try {
    await createProject({ projectName: formValues.projectName })
    // 通知全局有新项目创建，用于列表刷新
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('project-created'))
    }
    emit('update:open', false)
    emit('close')
  } finally {
    isSubmitting.value = false
  }
})

const handleOpenChange = (value: boolean) => {
  emit('update:open', value)
}
</script>

<template>
  <Dialog :open="open" @update:open="handleOpenChange">
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>创建新项目</DialogTitle>
        <DialogDescription>
          输入项目名称以创建新的招投标项目
        </DialogDescription>
      </DialogHeader>

      <form @submit="onSubmit" class="space-y-6">
        <FormField v-slot="{ componentField }" name="projectName">
          <FormItem>
            <FormLabel>项目名称</FormLabel>
            <FormControl>
              <Input
                v-bind="componentField"
                placeholder="例如：XX公司招投标项目"
                :disabled="isSubmitting"
                @keydown.enter="onSubmit"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            @click="handleOpenChange(false)"
            :disabled="isSubmitting"
          >
            取消
          </Button>
          <Button
            type="submit"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? '创建中...' : '创建' }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
