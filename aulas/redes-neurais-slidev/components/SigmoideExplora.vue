<script setup>
// Degrau contra sigmoide: o que acontece com a saída quando z anda um pouquinho.
import { ref, computed } from 'vue'
import { sig, degrau, n } from '../utils/conta.js'

const z = ref(-1)
const s = computed(() => sig(z.value))
const curvas = [
  { pts: [[-6, 0], [0, 0], [0, 1], [6, 1]], cor: '#8A99A5', larg: 2 },
  { f: sig, cor: '#2264AF', larg: 3 },
]
</script>

<template>
  <div class="w duas">
    <Grafico :curvas="curvas" :marcas="[{ x: z, y: s }, { x: z, y: degrau(z), cor: '#8A99A5' }]" :xlim="[-6, 6]" :ylim="[-0.05, 1.05]" :xt="[-6, -3, 0, 3, 6]" :yt="[0, 0.5, 1]" rx="z" ry="saída" :w="430" :h="270" />
    <div class="w-painel">
      <div class="w-linha"><span class="w-rot">z</span><input v-model.number="z" type="range" min="-6" max="6" step="0.1" style="width: 230px" /><span class="val">{{ n(z, 1) }}</span></div>
      <div class="cartao">sigmoide: σ(z) = <b>{{ n(s) }}</b><br />se z subir 0,1, a saída muda <b>{{ n(sig(z + 0.1) - s, 4) }}</b></div>
      <div class="cartao">degrau: saída = <b>{{ degrau(z) }}</b><br />se z subir 0,1, a saída muda <b>{{ degrau(z + 0.1) - degrau(z) }}</b></div>
      <div class="cartao q">inclinação da sigmoide aqui: σ′(z) = σ(z)·(1 − σ(z)) = <b>{{ n(s * (1 - s)) }}</b></div>
    </div>
  </div>
</template>
