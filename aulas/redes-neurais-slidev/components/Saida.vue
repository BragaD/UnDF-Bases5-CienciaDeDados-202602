<script setup>
// Mostra a saída que gerar_saidas.py gravou para um trecho de snippets/.
const props = defineProps({ nome: String })
const arquivos = import.meta.glob('../saidas/*', { query: '?raw', import: 'default', eager: true })
const texto = (arquivos[`../saidas/${props.nome}.txt`] || '').replace(/\n$/, '')
const tabela = arquivos[`../saidas/${props.nome}.html`] || ''
</script>

<template>
  <div class="saida">
    <pre v-if="texto">{{ texto }}</pre>
    <div v-if="tabela" v-html="tabela" />
  </div>
</template>
