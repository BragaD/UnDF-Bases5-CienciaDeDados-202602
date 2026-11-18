<script setup>
// A regra do perceptron, um exemplo por clique.
import { ref, computed } from 'vue'
import { degrau, n, X4, PORTAS } from '../utils/conta.js'

const props = defineProps({ porta: { type: String, default: 'E' } })
const p = ref(props.porta)
const w = ref([0, 0]), b = ref(0), i = ref(0), epoca = ref(1), errosEp = ref(0)
const hist = ref([]), errosPorEpoca = ref([]), parou = ref(false)

function recomecar(k) {
  if (k) p.value = k
  w.value = [0, 0]; b.value = 0; i.value = 0; epoca.value = 1; errosEp.value = 0
  hist.value = []; errosPorEpoca.value = []; parou.value = false
}
function passo() {
  if (parou.value || epoca.value > 40) return
  const x = X4[i.value], y = PORTAS[p.value][i.value]
  const z = w.value[0] * x[0] + w.value[1] * x[1] + b.value
  const yh = degrau(z), erro = y - yh
  w.value = [w.value[0] + erro * x[0], w.value[1] + erro * x[1]]
  b.value += erro
  errosEp.value += Math.abs(erro)
  hist.value.push({ ep: epoca.value, x, y, z, yh, erro, w: [...w.value], b: b.value })
  i.value++
  if (i.value === 4) {
    errosPorEpoca.value.push(errosEp.value)
    if (errosEp.value === 0) parou.value = true
    else { epoca.value++; i.value = 0; errosEp.value = 0 }
  }
}
function fimDaEpoca() {
  const e = epoca.value
  do passo(); while (!parou.value && epoca.value === e && epoca.value <= 40)
}
const ultimas = computed(() => hist.value.slice(-7))
</script>

<template>
  <div class="w duas">
    <div class="w-painel">
      <Plano :reta="[w[0], w[1], b]" :porta="p" :destaque="parou ? -1 : i % 4" :tam="270" />
      <div class="mono">w = ({{ n(w[0], 0) }}; {{ n(w[1], 0) }}) · b = {{ n(b, 0) }}</div>
    </div>
    <div class="w-painel">
      <div class="w-linha">
        <span class="w-rot">porta</span>
        <button v-for="k in ['E', 'OU', 'XOR']" :key="k" :class="{ ativo: p === k }" @click="recomecar(k)">{{ k }}</button>
        <button class="q" :disabled="parou" @click="passo">próximo exemplo ▶</button>
        <button class="q" :disabled="parou" @click="fimDaEpoca">até o fim da época</button>
        <button @click="recomecar()">recomeçar</button>
      </div>
      <table>
        <thead><tr><th>época</th><th>x</th><th>y</th><th>z</th><th>ŷ</th><th>erro</th><th>w depois</th><th>b depois</th></tr></thead>
        <tbody>
          <tr v-for="(l, k) in ultimas" :key="k" :class="{ atual: k === ultimas.length - 1 }">
            <td>{{ l.ep }}</td><td>({{ l.x[0] }}, {{ l.x[1] }})</td><td>{{ l.y }}</td><td>{{ n(l.z, 0) }}</td><td>{{ l.yh }}</td>
            <td :class="l.erro ? 'er' : ''">{{ l.erro > 0 ? '+1' : n(l.erro, 0) }}</td><td>({{ n(l.w[0], 0) }}; {{ n(l.w[1], 0) }})</td><td>{{ n(l.b, 0) }}</td>
          </tr>
          <tr v-if="!hist.length"><td colspan="8" style="text-align: left">começo: w = (0; 0), b = 0, η = 1. O anel laranja marca o próximo exemplo.</td></tr>
        </tbody>
      </table>
      <div class="cartao" :class="{ q: !parou }">
        erros por época: <b>{{ errosPorEpoca.join(', ') || '…' }}</b>
        <span v-if="parou"> · época sem erro: o perceptron parou.</span>
      </div>
    </div>
  </div>
</template>
