<script setup>
// Desenho de uma rede em camadas. Chaves: nó "camada-i"; aresta "camada-i-j"
// (do nó i da camada à esquerda ao nó j da camada seguinte).
import { computed } from 'vue'

const props = defineProps({
  camadas: { type: Array, default: () => [2, 2, 1] },
  textos: { type: Object, default: () => ({}) },
  fora: { type: Object, default: () => ({}) }, // rótulo azul ao lado do nó
  foraQ: { type: Object, default: () => ({}) }, // rótulo laranja
  pesos: { type: Object, default: () => ({}) },
  fortes: { type: [Array, Boolean], default: false },
  quentes: { type: Array, default: () => [] },
  nosQ: { type: Array, default: () => [] },
  soArestas: { type: Array, default: null },
  titulos: { type: Array, default: () => [] },
  visivel: { type: Object, default: () => ({}) }, // {camada: clique em que aparece}
  passo: { type: Number, default: 99 },
  volta: Boolean,
  largura: { type: Number, default: 760 },
  altura: { type: Number, default: 290 },
  r: { type: Number, default: 25 },
  tPeso: { type: Number, default: 0.3 },
  tPesos: { type: Object, default: () => ({}) }, // posição do rótulo de uma aresta, de 0 a 1
  margem: { type: Number, default: 110 },
})
const L = computed(() => props.camadas.length)
const topo = computed(() => (props.titulos.length ? 30 : 6))
const X = (l) => props.margem + (l * (props.largura - 2 * props.margem)) / (L.value - 1)
const Y = (l, i) => {
  const k = props.camadas[l]
  const util = props.altura - topo.value - 16
  const gap = Math.min(110, util / k)
  return topo.value + util / 2 + (i - (k - 1) / 2) * gap
}
// rótulos das camadas do meio: acima do primeiro nó, abaixo do último
const lado = (n) => (props.camadas[n.l] > 1 && n.i === props.camadas[n.l] - 1 ? 1 : -1)
const some = (l) => props.passo < (props.visivel[l] || 0)
const nos = computed(() => {
  const o = []
  props.camadas.forEach((k, l) => {
    for (let i = 0; i < k; i++) o.push({ l, i, ch: `${l}-${i}`, x: X(l), y: Y(l, i) })
  })
  return o
})
const arestas = computed(() => {
  const o = []
  for (let l = 0; l < L.value - 1; l++)
    for (let i = 0; i < props.camadas[l]; i++)
      for (let j = 0; j < props.camadas[l + 1]; j++) {
        const ch = `${l}-${i}-${j}`
        if (props.soArestas && !props.soArestas.includes(ch)) continue
        const x1 = X(l), y1 = Y(l, i), x2 = X(l + 1), y2 = Y(l + 1, j)
        const d = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / d, uy = (y2 - y1) / d
        const q = props.quentes.includes(ch)
        const forte = props.fortes === true || (Array.isArray(props.fortes) && props.fortes.includes(ch))
        const a = { x: x1 + ux * (props.r + 2), y: y1 + uy * (props.r + 2) }
        const b = { x: x2 - ux * (props.r + 9), y: y2 - uy * (props.r + 9) }
        const a2 = { x: x1 + ux * (props.r + 9), y: y1 + uy * (props.r + 9) }
        const b2 = { x: x2 - ux * (props.r + 2), y: y2 - uy * (props.r + 2) }
        const inv = q && props.volta
        o.push({
          ch, l, q, forte, de: inv ? b2 : a, para: inv ? a2 : b,
          tx: x1 + (x2 - x1) * (props.tPesos[ch] ?? props.tPeso), ty: y1 + (y2 - y1) * (props.tPesos[ch] ?? props.tPeso), peso: props.pesos[ch],
        })
      }
  return o
})
</script>

<template>
  <svg class="des" :width="largura" :height="altura" :viewBox="`0 0 ${largura} ${altura}`">
    <defs>
      <marker id="s-c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#9DB7D3" /></marker>
      <marker id="s-f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2264AF" /></marker>
      <marker id="s-q" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#D9480F" /></marker>
    </defs>
    <text v-for="(t, l) in titulos" :key="'t' + l" class="tit" :class="{ some: some(l) }" :x="X(l)" y="12">{{ t }}</text>
    <g v-for="a in arestas" :key="a.ch" :class="{ some: some(a.l + 1) }">
      <line class="ar" :class="{ forte: a.forte, q: a.q }" :x1="a.de.x" :y1="a.de.y" :x2="a.para.x" :y2="a.para.y" :marker-end="`url(#${a.q ? 's-q' : a.forte ? 's-f' : 's-c'})`" />
    </g>
    <g v-for="a in arestas" :key="'p' + a.ch" :class="{ some: some(a.l + 1) }">
      <text v-if="a.peso" class="peso" :class="{ q: a.q }" :x="a.tx" :y="a.ty">{{ a.peso }}</text>
    </g>
    <g v-for="n in nos" :key="n.ch" :class="{ some: some(n.l) }">
      <circle class="no" :class="{ ent: n.l === 0, sai: n.l === L - 1, q: nosQ.includes(n.ch) }" :cx="n.x" :cy="n.y" :r="r" />
      <text class="dentro" :x="n.x" :y="n.y">{{ textos[n.ch] }}</text>
      <template v-if="n.l === 0">
        <text v-if="fora[n.ch]" class="ida dir" :x="n.x - r - 9" :y="n.y">{{ fora[n.ch] }}</text>
        <text v-if="foraQ[n.ch]" class="volta dir" :x="n.x - r - 9" :y="n.y + 20">{{ foraQ[n.ch] }}</text>
      </template>
      <template v-else-if="n.l === L - 1">
        <text v-if="fora[n.ch]" class="ida esq" :x="n.x + r + 9" :y="n.y - (foraQ[n.ch] ? 11 : 0)">{{ fora[n.ch] }}</text>
        <text v-if="foraQ[n.ch]" class="volta esq" :x="n.x + r + 9" :y="n.y + (fora[n.ch] ? 11 : 0)">{{ foraQ[n.ch] }}</text>
      </template>
      <template v-else>
        <text v-if="fora[n.ch]" class="ida" :x="n.x" :y="n.y + lado(n) * (r + 13)">{{ fora[n.ch] }}</text>
        <text v-if="foraQ[n.ch]" class="volta" :x="n.x" :y="n.y + lado(n) * (r + (fora[n.ch] ? 32 : 13))">{{ foraQ[n.ch] }}</text>
      </template>
    </g>
  </svg>
</template>
