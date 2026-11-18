<script setup>
// A rede 2-2-1 da aula, etapa por etapa: a ida (1 a 5), a volta (6 a 9) e a correção (10).
// Todos os números são calculados aqui, a partir dos pesos mostrados.
import { ref, computed } from 'vue'
import { sig, n, par } from '../utils/conta.js'

const props = defineProps({ max: { type: Number, default: 10 }, inicio: { type: Number, default: 0 } })
const INICIAL = () => ({ W1: [[0.1, 0.3], [-0.2, 0.4]], b1: [0.1, -0.1], W2: [0.5, -0.3], b2: 0.2 })
const P = ref(INICIAL()), x = [0.5, 1], y = ref(1), eta = ref(0.5), etapa = ref(props.inicio), volta = ref(1), hist = ref([])

const c = computed(() => {
  const { W1, b1, W2, b2 } = P.value
  const z1 = [0, 1].map((j) => W1[j][0] * x[0] + W1[j][1] * x[1] + b1[j])
  const a1 = z1.map(sig)
  const z2 = W2[0] * a1[0] + W2[1] * a1[1] + b2
  const yh = sig(z2)
  const L = -Math.log(y.value === 1 ? yh : 1 - yh)
  const d2 = yh - y.value
  const gW2 = a1.map((a) => d2 * a)
  const d1 = [0, 1].map((j) => W2[j] * d2 * a1[j] * (1 - a1[j]))
  const gW1 = d1.map((d) => x.map((xi) => d * xi))
  const e = eta.value
  const novo = {
    W1: W1.map((l, j) => l.map((v, k) => v - e * gW1[j][k])), b1: b1.map((v, j) => v - e * d1[j]),
    W2: W2.map((v, j) => v - e * gW2[j]), b2: b2 - e * d2,
  }
  return { z1, a1, z2, yh, L, d2, gW2, d1, gW1, novo }
})
const texto = computed(() => {
  const { W1, b1, W2, b2 } = P.value, v = c.value
  return [
    { f: 'ida', t: 'A rede antes de qualquer conta', l: ['entrada x = (0,5; 1) · resposta y = ' + y.value, 'sigmoide em todos os neurônios'] },
    { f: 'ida', t: '1 · Camada 1: somas ponderadas', l: [0, 1].map((j) => `z${'₁₂'[j]} = ${n(W1[j][0])} · 0,5 + ${par(W1[j][1])} · 1 + ${par(b1[j])} = ${n(v.z1[j])}`) },
    { f: 'ida', t: '2 · Camada 1: ativações', l: [0, 1].map((j) => `a${'₁₂'[j]} = σ(${n(v.z1[j])}) = ${n(v.a1[j])}`) },
    { f: 'ida', t: '3 · Camada 2: soma ponderada', l: [`z = ${n(W2[0])} · ${n(v.a1[0])} + ${par(W2[1])} · ${n(v.a1[1])} + ${par(b2)} = ${n(v.z2)}`] },
    { f: 'ida', t: '4 · A previsão', l: [`ŷ = σ(${n(v.z2)}) = ${n(v.yh)}`] },
    { f: 'ida', t: '5 · A perda', l: [y.value === 1 ? `L = −ln(ŷ) = −ln(${n(v.yh)}) = ${n(v.L)}` : `L = −ln(1 − ŷ) = −ln(${n(1 - v.yh)}) = ${n(v.L)}`] },
    { f: 'volta', t: '6 · Erro do neurônio de saída', l: [`δ = ŷ − y = ${n(v.yh)} − ${y.value} = ${n(v.d2)}`] },
    { f: 'volta', t: '7 · Gradientes da camada 2: δ de quem recebe × a de quem envia', l: [`∂L/∂w₁ = ${n(v.d2)} · ${n(v.a1[0])} = ${n(v.gW2[0])}`, `∂L/∂w₂ = ${n(v.d2)} · ${n(v.a1[1])} = ${n(v.gW2[1])}`, `∂L/∂b = δ = ${n(v.d2)}`] },
    { f: 'volta', t: '8 · O erro volta pelos pesos: δₕ = w · δ · a(1 − a)', l: [0, 1].map((j) => `δ${'₁₂'[j]} = ${n(W2[j])} · ${par(v.d2)} · ${n(v.a1[j])} · ${n(1 - v.a1[j])} = ${n(v.d1[j])}`) },
    { f: 'volta', t: '9 · Gradientes da camada 1: δₕ × x', l: [0, 1].map((j) => `neurônio h${'₁₂'[j]}: ${n(v.d1[j])} · 0,5 = ${n(v.gW1[j][0])}   e   ${n(v.d1[j])} · 1 = ${n(v.gW1[j][1])}   (viés: ${n(v.d1[j])})`) },
    { f: 'volta', t: `10 · Correção: cada parâmetro anda −η × gradiente (η = ${n(eta.value, 1)})`, l: [`camada 2: w₁ = ${n(W2[0])} − ${n(eta.value, 1)} · ${par(v.gW2[0])} = ${n(v.novo.W2[0])}`, `w₂ = ${n(v.novo.W2[1])} · b = ${n(v.novo.b2)}`, `camada 1: os quatro pesos e os dois vieses, pela mesma conta (no desenho)`] },
  ][etapa.value]
})
function aplicar() {
  hist.value.push({ k: volta.value, yh: c.value.yh, L: c.value.L })
  P.value = c.value.novo; volta.value++; etapa.value = Math.min(5, props.max)
}
function recomecar() { P.value = INICIAL(); etapa.value = props.inicio; volta.value = 1; hist.value = [] }
const NOS = { x1: [70, 90], x2: [70, 240], h1: [290, 90], h2: [290, 240], o: [490, 165] }
const AR = [['x1', 'h1', 0, 0], ['x2', 'h1', 0, 1], ['x1', 'h2', 1, 0], ['x2', 'h2', 1, 1]]
const pt = (a, b, t) => [NOS[a][0] + (NOS[b][0] - NOS[a][0]) * t, NOS[a][1] + (NOS[b][1] - NOS[a][1]) * t]
const pesos = computed(() => (etapa.value >= 10 ? c.value.novo : P.value))
</script>

<template>
  <div class="w duas">
    <svg class="des" width="530" height="302" viewBox="0 0 580 330">
      <defs><marker id="iv" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2264AF" /></marker></defs>
      <g v-for="a in AR" :key="a[0] + a[1]">
        <line class="ar forte" :x1="pt(a[0], a[1], 0.12)[0]" :y1="pt(a[0], a[1], 0.12)[1]" :x2="pt(a[0], a[1], 0.87)[0]" :y2="pt(a[0], a[1], 0.87)[1]" marker-end="url(#iv)" />
        <text class="peso" :class="{ q: etapa >= 10 }" :x="pt(a[0], a[1], 0.27)[0]" :y="pt(a[0], a[1], 0.27)[1]">{{ n(pesos.W1[a[2]][a[3]]) }}</text>
        <text class="volta" :class="{ some: etapa < 9 || etapa >= 10 }" :x="pt(a[0], a[1], 0.7)[0]" :y="pt(a[0], a[1], 0.7)[1] - 11" style="font-size: 15px">∂ {{ n(c.gW1[a[2]][a[3]]) }}</text>
      </g>
      <g v-for="(h, j) in ['h1', 'h2']" :key="h">
        <line class="ar forte" :x1="pt(h, 'o', 0.13)[0]" :y1="pt(h, 'o', 0.13)[1]" :x2="pt(h, 'o', 0.86)[0]" :y2="pt(h, 'o', 0.86)[1]" marker-end="url(#iv)" />
        <text class="peso" :class="{ q: etapa >= 10 }" :x="pt(h, 'o', 0.36)[0]" :y="pt(h, 'o', 0.36)[1]">{{ n(pesos.W2[j]) }}</text>
        <text class="volta" :class="{ some: etapa < 7 || etapa >= 10 }" :x="pt(h, 'o', 0.66)[0] + 4" :y="pt(h, 'o', 0.66)[1] + (j ? 16 : -14)" style="font-size: 15px">∂ {{ n(c.gW2[j]) }}</text>
      </g>
      <circle class="no ent" cx="70" cy="90" r="25" /><text class="dentro" x="70" y="90">x₁</text><text class="ida dir" x="38" y="90">0,5</text>
      <circle class="no ent" cx="70" cy="240" r="25" /><text class="dentro" x="70" y="240">x₂</text><text class="ida dir" x="38" y="240">1</text>
      <g v-for="(h, j) in ['h1', 'h2']" :key="'n' + h">
        <circle class="no" :class="{ q: etapa === 8 }" :cx="NOS[h][0]" :cy="NOS[h][1]" r="25" /><text class="dentro" :x="NOS[h][0]" :y="NOS[h][1]">h{{ '₁₂'[j] }}</text>
        <text class="leg" :x="NOS[h][0]" :y="NOS[h][1] - 58">b = {{ n(pesos.b1[j]) }}</text>
        <text class="ida" :class="{ some: etapa < 1 }" :x="NOS[h][0]" :y="NOS[h][1] - 39">{{ etapa >= 2 ? 'a = ' + n(c.a1[j]) : 'z = ' + n(c.z1[j]) }}</text>
        <text class="volta" :class="{ some: etapa < 8 }" :x="NOS[h][0]" :y="NOS[h][1] + 41">δ = {{ n(c.d1[j]) }}</text>
      </g>
      <circle class="no sai" :class="{ q: etapa === 6 }" cx="490" cy="165" r="25" /><text class="dentro" x="490" y="165">ŷ</text>
      <text class="leg" x="490" y="107">b = {{ n(pesos.b2) }}</text>
      <text class="ida" :class="{ some: etapa < 3 }" x="490" y="126">{{ etapa >= 4 ? 'ŷ = ' + n(c.yh) : 'z = ' + n(c.z2) }}</text>
      <text class="volta" :class="{ some: etapa < 6 }" x="490" y="206">δ = {{ n(c.d2) }}</text>
      <text class="ida" :class="{ some: etapa < 5 }" x="490" y="262" style="fill: #27316E">y = {{ y }} · L = {{ n(c.L) }}</text>
    </svg>
    <div class="w-painel">
      <div class="w-linha">
        <button :disabled="etapa <= 0" @click="etapa--">◀ etapa anterior</button>
        <button class="q" :disabled="etapa >= max" @click="etapa++">próxima etapa ▶</button>
        <span class="w-rot">{{ etapa }} de {{ max }}</span>
      </div>
      <div class="cartao" :class="{ q: texto.f === 'volta' }" style="min-height: 118px">
        <div :class="texto.f" style="margin-bottom: 4px">{{ texto.t }}</div>
        <div v-for="(l, i) in texto.l" :key="i" class="mono" style="white-space: pre-wrap">{{ l }}</div>
      </div>
      <div class="w-linha">
        <span class="w-rot">resposta y</span><button :class="{ ativo: y === 1 }" @click="y = 1">1</button><button :class="{ ativo: y === 0 }" @click="y = 0">0</button>
        <template v-if="max >= 10"><b>η</b><button v-for="e in [0.5, 2]" :key="e" :class="{ ativo: eta === e }" @click="eta = e">{{ n(e, 1) }}</button></template>
      </div>
      <div v-if="max >= 10" class="w-linha">
        <button class="q" :disabled="etapa < 10" @click="aplicar">aplicar a correção e refazer a ida</button><button @click="recomecar">recomeçar</button>
      </div>
      <div v-if="hist.length" class="mono">
        <span v-for="h in hist.slice(-4)" :key="h.k">volta {{ h.k }}: ŷ = {{ n(h.yh) }}, L = {{ n(h.L) }}<br /></span>
        agora (volta {{ volta }}): ŷ = {{ n(c.yh) }}, L = {{ n(c.L) }}
      </div>
    </div>
  </div>
</template>
