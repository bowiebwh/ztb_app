<script setup lang="ts">
import { computed, defineAsyncComponent, h } from 'vue';
import { Circle } from 'lucide-vue-next';

interface Props {
  name: string;
  size?: number | string;
  color?: string;
  strokeWidth?: number | string;
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: 24,
  strokeWidth: 2,
});

// Dynamically import icon, fallback to Circle if not found
const IconComponent = computed(() => {
  try {
    return defineAsyncComponent(() =>
      import('lucide-vue-next')
        .then((module) => {
          const icon = (module as any)[props.name];
          if (!icon) {
            console.warn(`Icon "${props.name}" not found in lucide-vue-next, using fallback`);
            return Circle;
          }
          return icon;
        })
        .catch(() => {
          console.warn(`Failed to load icon "${props.name}", using fallback`);
          return Circle;
        })
    );
  } catch {
    return Circle;
  }
});
</script>

<template>
  <component
    :is="IconComponent"
    :size="size"
    :color="color"
    :stroke-width="strokeWidth"
    :class="props.class"
  />
</template>

