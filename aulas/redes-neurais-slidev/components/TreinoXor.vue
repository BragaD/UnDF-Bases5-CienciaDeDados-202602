<script setup>
// A rede 2-2-1 aprendendo o XOR com backpropagation, um exemplo por vez (η = 0,5).
// O sorteio dos pesos é o desta página, não o do numpy: bate em comportamento, não em número.
import { ref, computed } from 'vue'
import { sig, n, X4, PORTAS, sorteio } from '../utils/conta.js'

const Y = PORTAS.XOR
const semente = ref(1), R = ref(null), custos = ref([])
function recomecar(s) {
  if (s) semente.value = s
  const g = sorteio(semente.value * 7919)
  R.value = { W1: [[g(), g()], [g(), g()]], b1: [0, 0], W2: [g(), g()], b2: 0 }
  custos.value = []
}
recomecar()
const ida = (r, x) => {
  const a = [0, 1].map((j) => sig(r.W1[j][0] * x[0] + r.W1[j][1] * x[1] + r.b1[j]))
  return { a, yh: sig(r.W2[0] * a[0] + r.W2[1] * a[1] + r.b2) }
}
function treinar(vezes) {
  const r = JSON.parse(JSON.stringify(R.value)), eta = 0.5
  for (let e = 0; e < vezes; e++) {
    let c = 0
    X4.forEach((x, i) => {
      const { a, yh } = ida(r, x)
      c += -(Y[i] * Math.log(yh) + (1 - Y[i]) * Math.log(1 - yh))
      const d2 = yh - Y[i]
      const d1 = [0, 1].map((j) => r.W2[j] * d2 * a[j] * (1 - a[j]))
      for (let j = 0; j < 2; j++) {
        r.W2[j] -= eta * d2 * a[j]
        r.W1[j][0] -= eta * d1[j] * x[0]; r.W1[j][1] -= eta * d1[j] * x[1]; r.b1[j] -= eta * d1[j]
      }
      r.b2 -= eta * d2
    })
    custos.value.push(c / 4)
  }
  R.value = r
}
const f = computed(() => (x1, x2) => ida(R.value, [x1, x2]).yh)
const fh = computed(() => (h1, h2) => sig(R.value.W2[0] * h1 + R.value.W2[1] * h2 + R.value.b2))
const casos = computed(() => X4.map((x, i) => ({ x, ...ida(R.value, x), y: Y[i] })))
const oculto = computed(() => casos.value.map((c) => ({ x: c.a[0], y: c.a[1], c: c.y })))
const xmax = computed(() => Math.max(1000, custos.value.length))
</script>

<template>
  <div class="w" style="grid-template-columns: auto auto auto 1fr; gap: 12px">
    <Plano :f="f" porta="XOR" suave :tam="200" titulo="nas entradas" />
    <Plano :f="fh" :pts="oculto" suave :lim="[-0.15, 1.15]" :tam="200" rx="h₁" ry="h₂" titulo="na camada oculta" />
    <Grafico :curvas="[{ pts: custos.map((c, i) => [i, c]) }]" :xlim="[0, xmax]" :ylim="[0, 0.9]" :xt="[0, xmax]" :yt="[0, 0.3, 0.6, 0.9]" rx="época" ry="custo" :w="205" :h="222" />
    <div class="w-painel">
      <div class="w-linha"><button class="q" @click="treinar(100)">+100 épocas</button><button class="q" @click="treinar(1000)">+1000</button></div>
      <div class="w-linha"><button @click="recomecar()">zerar</button><button @click="recomecar(semente + 1)">outro sorteio</button></div>
      <div class="mono">sorteio {{ semente }} · épocas: {{ custos.length }}</div>
      <table>
        <thead><tr><th>x</th><th>XOR</th><th>h₁</th><th>h₂</th><th>ŷ</th></tr></thead>
        <tbody><tr v-for="(c, i) in casos" :key="i"><td>({{ c.x[0] }},{{ c.x[1] }})</td><td>{{ c.y }}</td><td>{{ n(c.a[0], 2) }}</td><td>{{ n(c.a[1], 2) }}</td><td :class="(c.yh >= 0.5 ? 1 : 0) === c.y ? 'ok' : 'er'">{{ n(c.yh, 2) }}</td></tr></tbody>
      </table>
    </div>
  </div>
</template>
