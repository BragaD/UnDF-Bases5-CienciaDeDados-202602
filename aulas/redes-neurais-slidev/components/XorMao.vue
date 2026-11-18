<script setup>
// A rede de três perceptrons que resolve o XOR, com os pesos escolhidos à mão.
import { ref, computed } from 'vue'
import { degrau, X4, PORTAS } from '../utils/conta.js'

const x1 = ref(0), x2 = ref(1)
const h1 = computed(() => degrau(x1.value + x2.value - 1))
const h2 = computed(() => degrau(-x1.value - x2.value + 1))
const s = computed(() => degrau(h1.value + h2.value - 2))
const idx = computed(() => x1.value * 2 + x2.value)
const oculto = X4.map((x, i) => ({ x: degrau(x[0] + x[1] - 1), y: degrau(-x[0] - x[1] + 1), c: PORTAS.XOR[i] }))
</script>

<template>
  <div class="w tres">
    <div class="w-painel">
      <Rede
        :camadas="[2, 2, 1]" :largura="400" :altura="250" :margem="50" fortes
        :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
        :pesos="{ '0-0-0': '1', '0-1-0': '1', '0-0-1': '−1', '0-1-1': '−1', '1-0-0': '1', '1-1-0': '1' }"
        :fora="{ '0-0': String(x1), '0-1': String(x2), '1-0': 'OU = ' + h1, '1-1': 'NÃO-E = ' + h2, '2-0': '= ' + s }"
      />
      <div class="w-linha"><span class="w-rot">x₁</span><button :class="{ ativo: x1 === 0 }" @click="x1 = 0">0</button><button :class="{ ativo: x1 === 1 }" @click="x1 = 1">1</button>
        <span class="w-rot">x₂</span><button :class="{ ativo: x2 === 0 }" @click="x2 = 0">0</button><button :class="{ ativo: x2 === 1 }" @click="x2 = 1">1</button></div>
      <div class="mono">h₁ = degrau({{ x1 }} + {{ x2 }} − 1) = {{ h1 }}<br />h₂ = degrau(−{{ x1 }} − {{ x2 }} + 1) = {{ h2 }}<br />ŷ = degrau({{ h1 }} + {{ h2 }} − 2) = <b>{{ s }}</b> · XOR = {{ PORTAS.XOR[idx] }}</div>
    </div>
    <Plano porta="XOR" :destaque="idx" :tam="205" titulo="o que a rede recebe" />
    <Plano :pts="oculto" :reta="[1, 1, -1.5]" :destaque="idx" :tam="205" rx="h₁" ry="h₂" titulo="o que a saída recebe" />
  </div>
</template>
