<script setup>
// Softmax de três placares, com a perda e o erro para a classe certa escolhida.
import { ref, computed } from 'vue'
import { n } from '../utils/conta.js'

const NOMES = ['gato', 'cachorro', 'pássaro']
const z = ref([2, 1, 0.1]), certa = ref(1)
const e = computed(() => z.value.map(Math.exp))
const soma = computed(() => e.value.reduce((a, b) => a + b, 0))
const p = computed(() => e.value.map((v) => v / soma.value))
</script>

<template>
  <div class="w" style="grid-template-columns: 1fr">
    <table style="width: 100%; font-size: 15px">
      <thead><tr><th style="text-align: left">classe</th><th>placar z</th><th></th><th>e<sup>z</sup></th><th style="text-align: left; width: 300px">probabilidade ŷ</th><th>resposta y</th><th>erro ŷ − y</th></tr></thead>
      <tbody>
        <tr v-for="(nome, k) in NOMES" :key="k">
          <td style="text-align: left">{{ nome }}</td>
          <td><input v-model.number="z[k]" type="range" min="-3" max="6" step="0.1" /></td>
          <td>{{ n(z[k], 1) }}</td><td>{{ n(e[k], 3) }}</td>
          <td style="text-align: left"><span :style="{ display: 'inline-block', height: '15px', width: p[k] * 220 + 'px', background: '#2264AF', borderRadius: '2px', verticalAlign: 'middle' }" /> {{ n(p[k]) }}</td>
          <td><button :class="{ ativo: certa === k }" @click="certa = k">{{ certa === k ? 1 : 0 }}</button></td>
          <td class="er">{{ n(p[k] - (certa === k ? 1 : 0)) }}</td>
        </tr>
        <tr><td style="text-align: left">soma</td><td></td><td></td><td>{{ n(soma, 3) }}</td><td style="text-align: left">1</td><td></td><td>{{ n(0, 3) }}</td></tr>
      </tbody>
    </table>
    <div class="w-linha">
      <div class="cartao">classe certa: <b>{{ NOMES[certa] }}</b> · perda L = −ln({{ n(p[certa]) }}) = <b>{{ n(-Math.log(p[certa])) }}</b></div>
      <button @click="z = [2, 1, 0.1]; certa = 1">voltar ao exemplo</button>
      <button @click="z = z.map((v) => Math.min(6, v + 1))">somar 1 aos três placares</button>
    </div>
  </div>
</template>
