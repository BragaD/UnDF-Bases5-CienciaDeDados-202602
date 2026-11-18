<script setup>
// Plano (x1, x2) com os pontos de uma porta lógica e a região em que f >= 0,5.
import { computed } from 'vue'
import { X4, PORTAS } from '../utils/conta.js'

const props = defineProps({
  f: Function, // (x1, x2) -> valor entre 0 e 1
  reta: Array, // [w1, w2, b]: atalho para f = degrau(w·x + b)
  porta: { type: String, default: '' },
  pts: Array, // [{x, y, c}] no lugar da porta
  lim: { type: Array, default: () => [-0.5, 1.5] },
  tam: { type: Number, default: 250 },
  suave: Boolean,
  rx: { type: String, default: 'x₁' },
  ry: { type: String, default: 'x₂' },
  titulo: { type: String, default: '' },
  destaque: { type: Number, default: -1 },
  celulas: { type: Number, default: 40 },
})
const M = 30
const fn = computed(() => {
  if (props.f) return props.f
  if (props.reta) return (a, b) => (props.reta[0] * a + props.reta[1] * b + props.reta[2] >= 0 ? 1 : 0)
  return null
})
const esc = (v) => M + ((v - props.lim[0]) / (props.lim[1] - props.lim[0])) * (props.tam - M - 6)
const px = (v) => esc(v)
const py = (v) => props.tam - M - ((v - props.lim[0]) / (props.lim[1] - props.lim[0])) * (props.tam - M - 6) + 0
const pontos = computed(() => props.pts || X4.map((p, i) => ({ x: p[0], y: p[1], c: (PORTAS[props.porta] || [])[i] })))
const grade = computed(() => {
  if (!fn.value) return []
  const N = props.celulas
  const passo = (props.lim[1] - props.lim[0]) / N
  const lado = (props.tam - M - 6) / N
  const out = []
  for (let i = 0; i < N; i++)
    for (let j = 0; j < N; j++) {
      const v = fn.value(props.lim[0] + (i + 0.5) * passo, props.lim[0] + (j + 0.5) * passo)
      const o = props.suave ? Math.max(0, Math.min(1, v)) * 0.75 : v >= 0.5 ? 0.5 : 0
      if (o > 0.02) out.push({ x: M + i * lado, y: props.tam - M - (j + 1) * lado, l: lado + 0.4, o })
    }
  return out
})
</script>

<template>
  <svg class="des" :width="tam" :height="tam + (titulo ? 20 : 0)" :viewBox="`0 ${titulo ? -20 : 0} ${tam} ${tam + (titulo ? 20 : 0)}`">
    <text v-if="titulo" class="tit" :x="tam / 2 + 10" y="-9">{{ titulo }}</text>
    <rect :x="M" y="6" :width="tam - M - 6" :height="tam - M - 6" fill="#fff" stroke="#DCE5EE" />
    <rect v-for="(c, i) in grade" :key="i" :x="c.x" :y="c.y" :width="c.l" :height="c.l" fill="#8FCEF1" :opacity="c.o" />
    <g v-for="t in [0, 1]" :key="t">
      <text class="leg" :x="px(t)" :y="tam - M + 13">{{ t }}</text>
      <text class="leg" :x="M - 11" :y="py(t)">{{ t }}</text>
    </g>
    <text class="leg" :x="tam / 2 + 12" :y="tam - 5">{{ rx }}</text>
    <text class="leg" x="8" :y="tam / 2 - 12">{{ ry }}</text>
    <g v-for="(p, i) in pontos" :key="'p' + i">
      <circle v-if="i === destaque" :cx="px(p.x)" :cy="py(p.y)" r="15" fill="none" stroke="#D9480F" stroke-width="3" />
      <circle :cx="px(p.x)" :cy="py(p.y)" r="8.5" :fill="p.c ? '#27316E' : '#fff'" stroke="#27316E" stroke-width="2.5" />
    </g>
  </svg>
</template>
