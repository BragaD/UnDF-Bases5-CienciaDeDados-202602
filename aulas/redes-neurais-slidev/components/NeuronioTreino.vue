<script setup>
// O neurônio sigmoide treinando numa porta lógica, com o gradiente do lote de 4 exemplos.
import { ref, computed } from 'vue'
import { sig, n, X4, PORTAS } from '../utils/conta.js'

const props = defineProps({ porta: { type: String, default: 'E' } })
const p = ref(props.porta), w = ref([0, 0]), b = ref(0), custos = ref([])
function recomecar(k) { if (k) p.value = k; w.value = [0, 0]; b.value = 0; custos.value = [] }
function treinar(vezes) {
  const y = PORTAS[p.value]
  let [w1, w2] = w.value, v = b.value
  for (let e = 0; e < vezes; e++) {
    let g1 = 0, g2 = 0, gb = 0, c = 0
    X4.forEach((x, i) => {
      const yh = sig(w1 * x[0] + w2 * x[1] + v), erro = yh - y[i]
      c += -(y[i] * Math.log(yh) + (1 - y[i]) * Math.log(1 - yh))
      g1 += erro * x[0]; g2 += erro * x[1]; gb += erro
    })
    custos.value.push(c / 4)
    w1 -= g1 / 4; w2 -= g2 / 4; v -= gb / 4
  }
  w.value = [w1, w2]; b.value = v
}
const f = computed(() => (x1, x2) => sig(w.value[0] * x1 + w.value[1] * x2 + b.value))
const prev = computed(() => X4.map((x) => f.value(x[0], x[1])))
const custoAgora = computed(() => {
  const y = PORTAS[p.value]
  return prev.value.reduce((s, yh, i) => s - (y[i] * Math.log(yh) + (1 - y[i]) * Math.log(1 - yh)), 0) / 4
})
const xmax = computed(() => Math.max(200, custos.value.length))
const curvas = computed(() => [
  { f: () => Math.log(2), cor: '#8A99A5', larg: 1.5, trac: '5 4' },
  { pts: custos.value.map((c, i) => [i, c]), cor: p.value === 'XOR' ? '#D9480F' : '#2264AF', larg: 2.5 },
])
</script>

<template>
  <div class="w tres">
    <Plano :f="f" :porta="p" suave :tam="230" />
    <Grafico :curvas="curvas" :xlim="[0, xmax]" :ylim="[0, 0.8]" :xt="[0, xmax / 2, xmax]" :yt="[0, 0.2, 0.4, 0.6, 0.8]" rx="época" ry="custo J (tracejado: 0,693)" :w="290" :h="232" />
    <div class="w-painel">
      <div class="w-linha"><span class="w-rot">porta</span>
        <button v-for="k in ['E', 'OU', 'XOR']" :key="k" :class="{ ativo: p === k }" @click="recomecar(k)">{{ k }}</button></div>
      <div class="w-linha"><button class="q" @click="treinar(1)">+1 época</button><button class="q" @click="treinar(100)">+100</button><button class="q" @click="treinar(1000)">+1000</button><button @click="recomecar()">zerar</button></div>
      <div class="mono">épocas: {{ custos.length }} · η = 1<br />w = ({{ n(w[0], 2) }}; {{ n(w[1], 2) }}) · b = {{ n(b, 2) }}<br />custo: <b>{{ n(custoAgora) }}</b></div>
      <table>
        <thead><tr><th>x</th><th>y</th><th>ŷ</th></tr></thead>
        <tbody><tr v-for="(x, i) in X4" :key="i"><td>({{ x[0] }}, {{ x[1] }})</td><td>{{ PORTAS[p][i] }}</td><td>{{ n(prev[i], 3) }}</td></tr></tbody>
      </table>
    </div>
  </div>
</template>
