<script setup lang="ts">
import parser from '../composables/prolog'

const modelValue = defineModel()
const a = await parser(['散', '勾', '三'])
console.log(a)
</script>

<template>
  <input
    id="input"
    v-model="modelValue"
    type="text"
    v-bind="$attrs"
    p="x-4 y-2"
    w="250px"
    text="center"
    bg="transparent"
    border="~ rounded gray-200 dark:gray-700"
    outline="none active:none"
  >
</template>
