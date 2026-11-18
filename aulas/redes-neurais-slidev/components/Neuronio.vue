<script setup>
// As seis peças de um neurônio, uma por clique: <Neuronio :passo="$clicks" />
defineProps({
  passo: { type: Number, default: 99 },
  xs: { type: Array, default: () => ['x₁', 'x₂'] },
  ws: { type: Array, default: () => ['w₁', 'w₂'] },
  b: { type: String, default: 'b' },
  z: { type: String, default: 'Σ' },
  ativ: { type: String, default: 'g' },
  saida: { type: String, default: 'ŷ' },
  legendas: { type: Boolean, default: true },
  largura: { type: Number, default: 820 },
})
</script>

<template>
  <svg class="des" :width="largura" :height="largura / 3" viewBox="0 0 900 300">
    <defs>
      <marker id="s-n" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2264AF" /></marker>
    </defs>
    <g :class="{ some: passo < 1 }">
      <circle class="no ent" cx="90" cy="90" r="28" /><text class="dentro" x="90" y="90">{{ xs[0] }}</text>
      <circle class="no ent" cx="90" cy="215" r="28" /><text class="dentro" x="90" y="215">{{ xs[1] }}</text>
      <text v-if="legendas" class="leg" x="90" y="268">entradas</text>
    </g>
    <g :class="{ some: passo < 2 }">
      <line class="ar forte" x1="118" y1="97" x2="352" y2="140" marker-end="url(#s-n)" />
      <line class="ar forte" x1="118" y1="208" x2="352" y2="164" marker-end="url(#s-n)" />
      <text class="peso" x="225" y="104">{{ ws[0] }}</text>
      <text class="peso" x="225" y="200">{{ ws[1] }}</text>
      <text v-if="legendas" class="leg" x="225" y="268">pesos</text>
    </g>
    <g :class="{ some: passo < 3 }">
      <line class="ar forte" x1="400" y1="52" x2="400" y2="102" marker-end="url(#s-n)" />
      <text class="peso" x="400" y="36">{{ b }}</text>
      <text v-if="legendas" class="leg esq" x="424" y="36">viés</text>
    </g>
    <g :class="{ some: passo < 4 }">
      <circle class="no" cx="400" cy="152" r="48" /><text class="dentro" x="400" y="152" :style="{ fontSize: z.length > 2 ? '17px' : '30px' }">{{ z }}</text>
      <text v-if="legendas" class="leg" x="400" y="268">soma ponderada z</text>
    </g>
    <g :class="{ some: passo < 5 }">
      <line class="ar forte" x1="448" y1="152" x2="548" y2="152" marker-end="url(#s-n)" />
      <rect class="cx" x="550" y="112" width="100" height="80" rx="8" /><text class="dentro" x="600" y="152" style="font-size: 26px">{{ ativ }}</text>
      <text v-if="legendas" class="leg" x="600" y="268">função de ativação</text>
    </g>
    <g :class="{ some: passo < 6 }">
      <line class="ar forte" x1="650" y1="152" x2="760" y2="152" marker-end="url(#s-n)" />
      <text class="dentro" x="800" y="152" style="font-size: 26px; fill: #27316E">{{ saida }}</text>
      <text v-if="legendas" class="leg" x="800" y="268">saída</text>
    </g>
  </svg>
</template>
