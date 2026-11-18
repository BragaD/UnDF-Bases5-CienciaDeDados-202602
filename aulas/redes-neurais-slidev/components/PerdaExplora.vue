<script setup>
// Entropia cruzada binária: a perda para cada previsão, com a resposta 1 ou 0.
import { ref, computed } from 'vue'
import { n } from '../utils/conta.js'

const p = ref(0.574), y = ref(1)
const L = (q) => -Math.log(y.value === 1 ? q : 1 - q)
const curvas = computed(() => [{ f: (q) => L(Math.min(0.999, Math.max(0.001, q))), cor: '#2264AF', larg: 3 }])
</script>

<template>
  <div class="w duas">
    <Grafico :curvas="curvas" :marcas="[{ x: p, y: L(p) }]" :xlim="[0, 1]" :ylim="[0, 4.7]" :xt="[0, 0.25, 0.5, 0.75, 1]" :dx="2" :yt="[0, 1, 2, 3, 4]" :dy="0" rx="previsão ŷ" ry="perda L" :w="430" :h="270" />
    <div class="w-painel">
      <div class="w-linha"><span class="w-rot">resposta y</span><button :class="{ ativo: y === 1 }" @click="y = 1">1</button><button :class="{ ativo: y === 0 }" @click="y = 0">0</button></div>
      <div class="w-linha"><span class="w-rot">previsão ŷ</span><input v-model.number="p" type="range" min="0.01" max="0.99" step="0.001" style="width: 220px" /><span class="val">{{ n(p) }}</span></div>
      <div class="cartao">L = −ln({{ y === 1 ? 'ŷ' : '1 − ŷ' }}) = −ln({{ n(y === 1 ? p : 1 - p) }}) = <b>{{ n(L(p)) }}</b></div>
      <div class="cartao q">probabilidade dada à resposta certa: <b>{{ n((y === 1 ? p : 1 - p) * 100, 1) }}%</b></div>
    </div>
  </div>
</template>
