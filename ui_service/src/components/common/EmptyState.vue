
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import SafeIcon from '@/components/common/SafeIcon.vue'

interface Props {
  icon?: string
  title: string
  description?: string
  actionLabel?: string
  actionHref?: string
}

const props = withDefaults(defineProps<Props>(), {
  icon: 'Inbox',
})

const emit = defineEmits<{
  action: []
}>()

const handleAction = () => {
  if (props.actionHref) {
    if (typeof window !== 'undefined') {
      window.location.href = props.actionHref
    }
  } else {
    emit('action')
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <div class="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-4">
      <SafeIcon :name="icon" :size="32" class="text-muted-foreground" />
    </div>
    
    <h3 class="text-lg font-semibold mb-2">{{ title }}</h3>
    
    <p v-if="description" class="text-sm text-muted-foreground mb-6 max-w-sm">
      {{ description }}
    </p>
    
    <Button
      v-if="actionLabel"
      @click="handleAction"
      size="sm"
    >
      {{ actionLabel }}
    </Button>
  </div>
</template>
