<script setup>
// Um neurônio de duas entradas com os botões na mão: pesos, viés e a porta a resolver.
import { ref, computed } from 'vue'
import { sig, degrau, n, X4, PORTAS } from '../utils/conta.js'

const props = defineProps({
  w1: { type: Number, default: 2 }, w2: { type: Number, default: 1 }, b: { type: Number, default: -3 },
  porta: { type: String, default: 'E' }, ativ: { type: String, default: 'degrau' },
})
const a = ref(props.w1), c = ref(props.w2), v = ref(props.b), p = ref(props.porta)
const g = (z) => (props.ativ === 'degrau' ? degrau(z) : sig(z))
const f = computed(() => (x1, x2) => g(a.value * x1 + c.value * x2 + v.value))
const linhas = computed(() =>
  X4.map((x, i) => {
    const z = a.value * x[0] + c.value * x[1] + v.value
    const s = g(z)
    return { x, y: PORTAS[p.value][i], z, s, ok: (s >= 0.5 ? 1 : 0) === PORTAS[p.value][i] }
  }),
)
const acertos = computed(() => linhas.value.filter((l) => l.ok).length)
</script>

<template>
  <div class="w duas">
    <Plano :f="f" :porta="p" :suave="ativ !== 'degrau'" :tam="290" />
    <div class="w-painel">
      <div class="w-linha">
        <span class="w-rot">porta</span>
        <button v-for="k in ['E', 'OU', 'XOR']" :key="k" :class="{ ativo: p === k }" @click="p = k">{{ k }}</button>
      </div>
      <div class="w-linha"><span class="w-rot">w₁</span><input v-model.number="a" type="range" min="-4" max="4" step="0.5" /><span class="val">{{ n(a, 1) }}</span>
        <span class="w-rot">w₂</span><input v-model.number="c" type="range" min="-4" max="4" step="0.5" /><span class="val">{{ n(c, 1) }}</span></div>
      <div class="w-linha"><span class="w-rot">b&nbsp;</span><input v-model.number="v" type="range" min="-5" max="5" step="0.5" /><span class="val">{{ n(v, 1) }}</span></div>
      <table>
        <thead><tr><th>x₁</th><th>x₂</th><th>resposta y</th><th>z = w·x + b</th><th>previsão ŷ</th><th></th></tr></thead>
        <tbody>
          <tr v-for="(l, i) in linhas" :key="i">
            <td>{{ l.x[0] }}</td><td>{{ l.x[1] }}</td><td>{{ l.y }}</td><td>{{ n(l.z, 1) }}</td><td>{{ ativ === 'degrau' ? l.s : n(l.s, 2) }}</td>
            <td :class="l.ok ? 'ok' : 'er'">{{ l.ok ? 'certo' : 'errado' }}</td>
          </tr>
        </tbody>
      </table>
      <div class="cartao" :class="{ q: acertos < 4 }">acertos: <b>{{ acertos }} de 4</b> · região azul: ŷ = 1</div>
    </div>
  </div>
</template>
