<script setup>
// Gráfico de linhas mínimo: curvas dadas por função ou por lista de pontos.
import { computed } from 'vue'
import { n } from '../utils/conta.js'

const props = defineProps({
  curvas: { type: Array, default: () => [] }, // [{f, cor, larg, trac}] ou [{pts: [[x, y]], cor}]
  marcas: { type: Array, default: () => [] }, // [{x, y, cor, rot}]
  xlim: Array,
  ylim: Array,
  xt: { type: Array, default: () => [] },
  yt: { type: Array, default: () => [] },
  rx: { type: String, default: '' },
  ry: { type: String, default: '' },
  w: { type: Number, default: 360 },
  h: { type: Number, default: 240 },
  dx: { type: Number, default: 0 },
  dy: { type: Number, default: 1 },
})
const E = 44, B = 34
const px = (x) => E + ((x - props.xlim[0]) / (props.xlim[1] - props.xlim[0])) * (props.w - E - 8)
const py = (y) => props.h - B - ((Math.max(props.ylim[0], Math.min(props.ylim[1], y)) - props.ylim[0]) / (props.ylim[1] - props.ylim[0])) * (props.h - B - 8)
const caminhos = computed(() =>
  props.curvas.map((c) => {
    let pts = c.pts
    if (!pts) {
      pts = []
      for (let i = 0; i <= 160; i++) {
        const x = props.xlim[0] + (i / 160) * (props.xlim[1] - props.xlim[0])
        pts.push([x, c.f(x)])
      }
    }
    return { d: pts.map((p, i) => `${i ? 'L' : 'M'}${px(p[0]).toFixed(1)},${py(p[1]).toFixed(1)}`).join(''), ...c }
  }),
)
</script>

<template>
  <svg class="des" :width="w" :height="h" :viewBox="`0 0 ${w} ${h}`">
    <line :x1="E" :y1="h - B" :x2="w - 8" :y2="h - B" stroke="#8A99A5" />
    <line :x1="E" y1="8" :x2="E" :y2="h - B" stroke="#8A99A5" />
    <g v-for="t in xt" :key="'x' + t">
      <line :x1="px(t)" :y1="h - B" :x2="px(t)" :y2="h - B + 4" stroke="#8A99A5" />
      <text class="leg" :x="px(t)" :y="h - B + 14">{{ n(t, dx) }}</text>
    </g>
    <g v-for="t in yt" :key="'y' + t">
      <line :x1="E - 4" :y1="py(t)" :x2="w - 8" :y2="py(t)" stroke="#EEF2F6" />
      <text class="leg dir" :x="E - 7" :y="py(t)">{{ n(t, dy) }}</text>
    </g>
    <text class="leg" :x="(w + E) / 2" :y="h - 6">{{ rx }}</text>
    <text class="leg esq" :x="E + 6" y="14">{{ ry }}</text>
    <path v-for="(c, i) in caminhos" :key="i" :d="c.d" fill="none" :stroke="c.cor || '#2264AF'" :stroke-width="c.larg || 2.5" :stroke-dasharray="c.trac || ''" stroke-linejoin="round" />
    <g v-for="(m, i) in marcas" :key="'m' + i">
      <circle :cx="px(m.x)" :cy="py(m.y)" :r="m.r || 6" :fill="m.cor || '#D9480F'" stroke="#fff" stroke-width="1.5" />
      <text v-if="m.rot" class="leg esq" :x="px(m.x) + 10" :y="py(m.y) - 10" :style="{ fill: m.cor || '#D9480F' }">{{ m.rot }}</text>
    </g>
  </svg>
</template>
