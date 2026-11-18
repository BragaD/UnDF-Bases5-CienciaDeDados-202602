<script setup>
// Gradiente descendente num peso só: J(w) = 0,55·(w − 1,4)² + 0,3.
import { ref, computed } from 'vue'
import { n } from '../utils/conta.js'

const J = (w) => 0.55 * (w - 1.4) ** 2 + 0.3
const dJ = (w) => 1.1 * (w - 1.4)
const eta = ref(0.4), traj = ref([-0.8])
const atual = computed(() => traj.value[traj.value.length - 1])
function passo() { if (Math.abs(atual.value) < 50) traj.value.push(atual.value - eta.value * dJ(atual.value)) }
function recomecar() { traj.value = [-0.8] }
const linhas = computed(() => traj.value.slice(-6).map((w, k) => ({ k: traj.value.length - Math.min(6, traj.value.length) + k, w })))
const curvas = computed(() => [{ f: J, cor: '#2264AF', larg: 3 }, { pts: traj.value.map((w) => [w, J(w)]), cor: '#D9480F', larg: 1.5 }])
const marcas = computed(() => traj.value.filter((w) => w > -1.7 && w < 4.5 && J(w) < 5.6).map((w, i, a) => ({ x: w, y: J(w), r: i === a.length - 1 ? 7 : 4 })))
</script>

<template>
  <div class="w duas">
    <Grafico :curvas="curvas" :marcas="marcas" :xlim="[-1.7, 4.5]" :ylim="[0, 5.6]" :xt="[-1, 0, 1, 2, 3, 4]" :yt="[0, 2, 4]" :dy="0" rx="um peso w" ry="custo J" :w="440" :h="280" />
    <div class="w-painel">
      <div class="w-linha"><span class="w-rot">taxa</span><b>η</b><input v-model.number="eta" type="range" min="0.05" max="2" step="0.05" @input="recomecar" /><span class="val">{{ n(eta, 2) }}</span>
        <button v-for="e in [0.1, 0.4, 1.7, 1.9]" :key="e" @click="eta = e; recomecar()">{{ n(e, 1) }}</button></div>
      <div class="w-linha"><button class="q" @click="passo">dar um passo ▶</button><button @click="recomecar">recomeçar</button></div>
      <table>
        <thead><tr><th>passo</th><th>w</th><th>∂J/∂w</th><th>−η·∂J/∂w</th><th>J</th></tr></thead>
        <tbody>
          <tr v-for="l in linhas" :key="l.k" :class="{ atual: l.k === traj.length - 1 }">
            <td>{{ l.k }}</td><td>{{ n(l.w) }}</td><td>{{ n(dJ(l.w)) }}</td><td>{{ n(-eta * dJ(l.w)) }}</td><td>{{ n(J(l.w)) }}</td>
          </tr>
        </tbody>
      </table>
      <div class="cartao">o próximo w é o w de agora <b>mais</b> a coluna −η·∂J/∂w</div>
    </div>
  </div>
</template>
