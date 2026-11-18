<script setup>
// Caixas ligadas por setas: a ida em azul por cima, a volta em laranja por baixo.
import { computed } from 'vue'

const props = defineProps({
  caixas: Array,
  ida: { type: Array, default: () => [] },
  volta: { type: Array, default: () => [] },
  largura: { type: Number, default: 860 },
  passo: { type: Number, default: 99 },
  revela: { type: String, default: '' }, // 'ida': uma seta por clique; 'volta': da direita para a esquerda
})
const temVolta = computed(() => props.volta.length > 0)
const H = computed(() => (temVolta.value ? 128 : 92))
const cy = computed(() => (temVolta.value ? 58 : 56))
const larg = computed(() => props.caixas.map((t) => Math.max(74, t.length * 10.5 + 30)))
const pos = computed(() => {
  const total = larg.value.reduce((a, b) => a + b, 0)
  const gap = (props.largura - 8 - total) / (props.caixas.length - 1)
  let x = 4
  return larg.value.map((w) => {
    const p = { x, w }
    x += w + gap
    return p
  })
})
const vIda = (i) => props.revela !== 'ida' || props.passo >= i + 1
const vVolta = (i) => props.revela !== 'volta' || props.passo >= props.caixas.length - 1 - i
</script>

<template>
  <svg class="des" :width="largura" :height="H" :viewBox="`0 0 ${largura} ${H}`">
    <defs>
      <marker id="c-f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2264AF" /></marker>
      <marker id="c-q" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#D9480F" /></marker>
    </defs>
    <g v-for="(p, i) in pos" :key="i">
      <g :class="{ some: i > 0 && !vIda(i - 1) }">
        <rect class="cx" :x="p.x" :y="cy - 24" :width="p.w" height="48" rx="8" />
        <text class="dentro" :x="p.x + p.w / 2" :y="cy">{{ caixas[i] }}</text>
      </g>
      <g v-if="i < pos.length - 1">
        <g :class="{ some: !vIda(i) }">
          <line class="ar forte" :x1="p.x + p.w + 4" :y1="cy - (temVolta ? 8 : 0)" :x2="pos[i + 1].x - 5" :y2="cy - (temVolta ? 8 : 0)" marker-end="url(#c-f)" />
          <text class="ida" :x="(p.x + p.w + pos[i + 1].x) / 2" :y="cy - 38">{{ ida[i] }}</text>
        </g>
        <g v-if="temVolta && volta[i] !== ''" :class="{ some: !vVolta(i) }">
          <line class="ar q" :x1="pos[i + 1].x - 4" :y1="cy + 10" :x2="p.x + p.w + 5" :y2="cy + 10" marker-end="url(#c-q)" />
          <text class="volta" :x="(p.x + p.w + pos[i + 1].x) / 2" :y="cy + 42">{{ volta[i] }}</text>
        </g>
      </g>
    </g>
  </svg>
</template>
