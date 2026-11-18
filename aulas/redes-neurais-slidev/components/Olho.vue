<script setup>
// Eyebrow: a qual das quatro perguntas o slide responde. <Olho q="1 3" />
const props = defineProps({ q: { type: String, default: '' } })
const NOMES = { 1: 'Prever', 2: 'Medir', 3: 'Atribuir', 4: 'Corrigir' }
const itens = props.q.split(' ').filter(Boolean).map(Number)
</script>

<template>
  <div class="olho">
    <span v-for="i in itens" :key="i" :class="{ q: i >= 3 }">{{ i }} · {{ NOMES[i] }}</span>
  </div>
</template>
