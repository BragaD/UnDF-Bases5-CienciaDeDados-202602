<script setup>
// f = (x + y) · z como grafo de contas. passo: 1 q, 2 f | 3 ∂f/∂f, 4 produto, 5 soma.
defineProps({ passo: { type: Number, default: 99 }, largura: { type: Number, default: 760 } })
</script>

<template>
  <svg class="des" :width="largura" :height="(largura * 300) / 860" viewBox="0 0 860 300">
    <defs>
      <marker id="g-f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2264AF" /></marker>
    </defs>
    <text class="dentro" x="50" y="50">x</text><text class="dentro" x="50" y="150">y</text><text class="dentro" x="50" y="260">z</text>
    <line class="ar forte" x1="70" y1="52" x2="296" y2="92" marker-end="url(#g-f)" />
    <line class="ar forte" x1="70" y1="148" x2="296" y2="108" marker-end="url(#g-f)" />
    <line class="ar forte" x1="70" y1="258" x2="536" y2="192" marker-end="url(#g-f)" />
    <circle class="no" cx="330" cy="100" r="30" /><text class="dentro" x="330" y="100" style="font-size: 26px">+</text>
    <line class="ar forte" x1="360" y1="108" x2="536" y2="168" marker-end="url(#g-f)" />
    <circle class="no" cx="570" cy="180" r="30" /><text class="dentro" x="570" y="180" style="font-size: 26px">×</text>
    <line class="ar forte" x1="600" y1="180" x2="770" y2="180" marker-end="url(#g-f)" />
    <text class="dentro" x="800" y="180">f</text>
    <text class="ida" x="170" y="50">−2</text><text class="ida" x="170" y="112">5</text><text class="ida" x="300" y="207">−4</text>
    <text class="ida" :class="{ some: passo < 1 }" x="455" y="116">q = 3</text>
    <text class="ida" :class="{ some: passo < 2 }" x="685" y="162">f = −12</text>
    <text class="volta" :class="{ some: passo < 3 }" x="685" y="200">∂f/∂f = 1</text>
    <text class="volta" :class="{ some: passo < 4 }" x="430" y="162">∂f/∂q = z = −4</text>
    <text class="volta" :class="{ some: passo < 4 }" x="300" y="250">∂f/∂z = q = 3</text>
    <text class="volta" :class="{ some: passo < 5 }" x="170" y="88">∂f/∂x = −4</text>
    <text class="volta" :class="{ some: passo < 5 }" x="170" y="150">∂f/∂y = −4</text>
  </svg>
</template>
