<script setup>
// O fator que multiplica o erro depois de atravessar n camadas na volta.
import { ref, computed } from 'vue'
import { n } from '../utils/conta.js'

const k = ref(10)
const fator = computed(() => 0.25 ** k.value)
const sci = (v) => { const e = Math.floor(Math.log10(v)); return `${n(v / 10 ** e, 1)} × 10<sup>${e < 0 ? '−' + -e : e}</sup>` }
const larg = (v) => Math.max(2, (1 + Math.log10(v) / 13) * 380)
</script>

<template>
  <div class="w" style="grid-template-columns: 1fr">
    <div class="w-linha"><span class="w-rot">camadas atravessadas na volta</span><input v-model.number="k" type="range" min="1" max="20" step="1" style="width: 260px" /><span class="val">{{ k }}</span></div>
    <table style="font-size: 15px">
      <tbody>
        <tr><td style="text-align: left">sigmoide: no máximo 0,25<sup>{{ k }}</sup></td><td style="text-align: left; width: 400px"><span :style="{ display: 'inline-block', height: '16px', width: larg(fator) + 'px', background: '#D9480F', borderRadius: '2px' }" /></td><td class="er" v-html="sci(fator)" /></tr>
        <tr><td style="text-align: left">ReLU, neurônio ativo: 1<sup>{{ k }}</sup></td><td style="text-align: left"><span :style="{ display: 'inline-block', height: '16px', width: larg(1) + 'px', background: '#2264AF', borderRadius: '2px' }" /></td><td>1</td></tr>
      </tbody>
    </table>
    <div class="fraco pequeno">A barra está em escala logarítmica: cada 29 pixels a menos é o erro dividido por 10.</div>
  </div>
</template>
