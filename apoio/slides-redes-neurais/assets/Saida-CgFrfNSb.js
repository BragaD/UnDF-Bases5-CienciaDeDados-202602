import{B as e,St as t,b as n,vt as r,y as i}from"./modules/shiki-DyaLTTWP.js";import{rt as a}from"./index-BaCsPfGH.js";var o=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>XOR</th>
      <th>h1</th>
      <th>h2</th>
      <th>previsão</th>
    </tr>
    <tr>
      <th>x1</th>
      <th>x2</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">0</th>
      <th>0</th>
      <td>0</td>
      <td>0.019</td>
      <td>0.016</td>
      <td>0.001</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0.967</td>
      <td>0.000</td>
      <td>0.999</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">1</th>
      <th>0</th>
      <td>1</td>
      <td>0.000</td>
      <td>0.972</td>
      <td>0.999</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>0.014</td>
      <td>0.012</td>
      <td>0.001</td>
    </tr>
  </tbody>
</table>`,s=`custo na última época: 0.001
`,c=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>previsão</th>
      <th>perda</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>antes do passo</th>
      <td>0.584</td>
      <td>0.537</td>
    </tr>
    <tr>
      <th>depois do passo</th>
      <td>0.668</td>
      <td>0.404</td>
    </tr>
  </tbody>
</table>`,l=`W1 novo: [[0.112, 0.325], [-0.208, 0.385]] | b1 novo: [ 0.125 -0.115]
W2 novo: [[0.627, -0.186]] | b2 novo: [0.408]
`,u=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>backpropagation</th>
      <th>mexendo no peso</th>
    </tr>
    <tr>
      <th>peso</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>W1[0,0]</th>
      <td>-0.0247</td>
      <td>-0.0247</td>
    </tr>
    <tr>
      <th>W1[0,1]</th>
      <td>-0.0494</td>
      <td>-0.0494</td>
    </tr>
    <tr>
      <th>W1[1,0]</th>
      <td>0.0154</td>
      <td>0.0154</td>
    </tr>
    <tr>
      <th>W1[1,1]</th>
      <td>0.0309</td>
      <td>0.0309</td>
    </tr>
  </tbody>
</table>`,d=`delta2: [-0.416] | delta1: [-0.049  0.031]
grad_W2: [[-0.254 -0.229]]
grad_W1: [[-0.025, -0.049], [0.015, 0.031]]
`,f=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>XOR</th>
      <th>previsão</th>
      <th>erro</th>
      <th>erro · x1</th>
      <th>erro · x2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>(0, 0)</th>
      <td>0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>(0, 1)</th>
      <td>1</td>
      <td>0.5</td>
      <td>-0.5</td>
      <td>0.0</td>
      <td>-0.5</td>
    </tr>
    <tr>
      <th>(1, 0)</th>
      <td>1</td>
      <td>0.5</td>
      <td>-0.5</td>
      <td>-0.5</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>(1, 1)</th>
      <td>0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.5</td>
    </tr>
  </tbody>
</table>`,p=`gradiente dos pesos: [0. 0.] | gradiente do viés: 0.0
`,m=`previsão: 0.574 | perda: 0.554
gradiente dos pesos: [-0.851 -0.426] | do viés: -0.426
pesos novos: [ 0.826 -0.387] | viés novo: 0.313
previsão nova: 0.829
`,h=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>custo final</th>
      <th>pesos</th>
      <th>previsões para (0,0) (0,1) (1,0) (1,1)</th>
    </tr>
    <tr>
      <th>porta</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>E</th>
      <td>0.009</td>
      <td>[8.82, 8.82]</td>
      <td>[0.0, 0.01, 0.01, 0.99]</td>
    </tr>
    <tr>
      <th>OU</th>
      <td>0.005</td>
      <td>[10.08, 10.08]</td>
      <td>[0.01, 1.0, 1.0, 1.0]</td>
    </tr>
    <tr>
      <th>XOR</th>
      <td>0.693</td>
      <td>[0.0, 0.0]</td>
      <td>[0.5, 0.5, 0.5, 0.5]</td>
    </tr>
  </tbody>
</table>`,g=`custo de quem responde 0,5 para tudo: 0.693
`,_=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>resposta</th>
      <th>previsão</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>(0, 0)</th>
      <td>0</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>(0, 1)</th>
      <td>0</td>
      <td>0.010</td>
    </tr>
    <tr>
      <th>(1, 0)</th>
      <td>0</td>
      <td>0.010</td>
    </tr>
    <tr>
      <th>(1, 1)</th>
      <td>1</td>
      <td>0.986</td>
    </tr>
  </tbody>
</table>`,v=`pesos: [8.82 8.82] | viés: -13.4 | custo final: 0.009
`,y=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>preço</th>
      <th>frete</th>
      <th>marketing</th>
      <th>material</th>
      <th>acessível</th>
      <th>conhecida</th>
      <th>qualidade</th>
      <th>P(campeã)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A</th>
      <td>40</td>
      <td>10</td>
      <td>2</td>
      <td>4</td>
      <td>0.82</td>
      <td>0.17</td>
      <td>0.23</td>
      <td>0.21</td>
    </tr>
    <tr>
      <th>B</th>
      <td>150</td>
      <td>20</td>
      <td>30</td>
      <td>9</td>
      <td>0.01</td>
      <td>0.98</td>
      <td>0.97</td>
      <td>0.71</td>
    </tr>
    <tr>
      <th>C</th>
      <td>70</td>
      <td>0</td>
      <td>20</td>
      <td>8</td>
      <td>0.62</td>
      <td>0.88</td>
      <td>0.80</td>
      <td>0.87</td>
    </tr>
  </tbody>
</table>`,b=`z1: [0.45 0.2 ] | a1: [0.611 0.55 ]
z2: [0.34] | previsão: [0.584] | perda: [0.537]
`,x=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>h1 (OU)</th>
      <th>h2 (NÃO-E)</th>
      <th>saída</th>
      <th>XOR</th>
    </tr>
    <tr>
      <th>x1</th>
      <th>x2</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">0</th>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">1</th>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>`,S=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>erros</th>
      <th>w1</th>
      <th>w2</th>
      <th>b</th>
    </tr>
    <tr>
      <th>época</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>-3.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>-3.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>-3.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>-3.0</td>
    </tr>
  </tbody>
</table>`,C=`z: 0.0 | previsão: 1 | erro: -1
pesos depois: [0. 0.] | viés depois: -1.0
`,w=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>placar z</th>
      <th>probabilidade</th>
      <th>resposta y</th>
      <th>erro</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>gato</th>
      <td>2.0</td>
      <td>0.659</td>
      <td>0</td>
      <td>0.659</td>
    </tr>
    <tr>
      <th>cachorro</th>
      <td>1.0</td>
      <td>0.242</td>
      <td>1</td>
      <td>-0.758</td>
    </tr>
    <tr>
      <th>pássaro</th>
      <td>0.1</td>
      <td>0.099</td>
      <td>0</td>
      <td>0.099</td>
    </tr>
  </tbody>
</table>`,T=`perda: 1.417
`,E=`treino: (1347, 64) | teste: (450, 64)
resposta da 1ª imagem: 7 | em one-hot: [0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]
`,D=`imagens de teste: 450 | erradas: 15
`,O=`formas -> X_lote: (32, 64) | Z1: (32, 32) | P: (32, 10)
probabilidades da 1ª imagem: [0.11 0.08 0.03 0.11 0.03 0.04 0.1  0.31 0.06 0.12]
`,k=`custo do lote antes de treinar: 2.268
formas dos gradientes -> W2: (10, 32) | W1: (32, 64)
`,A=`W1: (32, 64) | b1: (32,) | W2: (10, 32) | b2: (10,)
parâmetros: 2410
`,j=`acurácia no treino: 0.985
acurácia no teste:  0.967
`,M=`<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acurácia no teste</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>nossa rede, em numpy</th>
      <td>0.967</td>
    </tr>
    <tr>
      <th>MLPClassifier</th>
      <td>0.969</td>
    </tr>
  </tbody>
</table>`,N={class:`saida`},P={key:0},F=[`innerHTML`],I={__name:`Saida`,props:{nome:String},setup(I){let{$slidev:L,$nav:R,$clicksContext:z,$clicks:B,$page:V,$renderContext:H,$frontmatter:U}=a(),W=I,G=Object.assign({"../saidas/_b_setup.html":``,"../saidas/_b_setup.txt":``,"../saidas/_b_xor_tabela.html":o,"../saidas/_b_xor_tabela.txt":s,"../saidas/_fig_ativacoes.html":``,"../saidas/_fig_ativacoes.txt":``,"../saidas/_fig_curvas.html":``,"../saidas/_fig_curvas.txt":``,"../saidas/_fig_custo_and.html":``,"../saidas/_fig_custo_and.txt":``,"../saidas/_fig_custo_dig.html":``,"../saidas/_fig_custo_dig.txt":``,"../saidas/_fig_erros.html":``,"../saidas/_fig_erros.txt":``,"../saidas/_fig_portas.html":``,"../saidas/_fig_portas.txt":``,"../saidas/_fig_portas_custo.html":``,"../saidas/_fig_portas_custo.txt":``,"../saidas/_fig_taxas.html":``,"../saidas/_fig_taxas.txt":``,"../saidas/_fig_xor.html":``,"../saidas/_fig_xor.txt":``,"../saidas/_setup.html":``,"../saidas/_setup.txt":``,"../saidas/_t_carregar.html":``,"../saidas/_t_carregar.txt":``,"../saidas/b_conferencia.html":c,"../saidas/b_conferencia.txt":``,"../saidas/b_correcao.html":``,"../saidas/b_correcao.txt":l,"../saidas/b_geral.html":``,"../saidas/b_geral.txt":``,"../saidas/b_numerico.html":u,"../saidas/b_numerico.txt":``,"../saidas/b_volta.html":``,"../saidas/b_volta.txt":d,"../saidas/b_xor.html":``,"../saidas/b_xor.txt":``,"../saidas/g_funcao.html":``,"../saidas/g_funcao.txt":``,"../saidas/g_grad_xor_a.html":f,"../saidas/g_grad_xor_a.txt":``,"../saidas/g_grad_xor_b.html":``,"../saidas/g_grad_xor_b.txt":p,"../saidas/g_passo.html":``,"../saidas/g_passo.txt":m,"../saidas/g_portas.html":h,"../saidas/g_portas.txt":g,"../saidas/g_prev_and.html":_,"../saidas/g_prev_and.txt":``,"../saidas/g_treino_and.html":``,"../saidas/g_treino_and.txt":v,"../saidas/m_camiseta.html":y,"../saidas/m_camiseta.txt":``,"../saidas/m_ida.html":``,"../saidas/m_ida.txt":b,"../saidas/m_xor_mao.html":x,"../saidas/m_xor_mao.txt":``,"../saidas/p1_hist.html":S,"../saidas/p1_hist.txt":``,"../saidas/p1_passo.html":``,"../saidas/p1_passo.txt":C,"../saidas/p1_treinar.html":``,"../saidas/p1_treinar.txt":``,"../saidas/s_softmax.html":w,"../saidas/s_softmax.txt":T,"../saidas/t_dados.html":``,"../saidas/t_dados.txt":E,"../saidas/t_erros_n.html":``,"../saidas/t_erros_n.txt":D,"../saidas/t_lote_ida.html":``,"../saidas/t_lote_ida.txt":O,"../saidas/t_lote_volta.html":``,"../saidas/t_lote_volta.txt":k,"../saidas/t_pecas.html":``,"../saidas/t_pecas.txt":A,"../saidas/t_resultado.html":``,"../saidas/t_resultado.txt":j,"../saidas/t_sklearn.html":M,"../saidas/t_sklearn.txt":``,"../saidas/t_treinar.html":``,"../saidas/t_treinar.txt":``}),K=(G[`../saidas/${W.nome}.txt`]||``).replace(/\n$/,``),q=G[`../saidas/${W.nome}.html`]||``;return(a,o)=>(e(),n(`div`,N,[r(K)?(e(),n(`pre`,P,t(r(K)),1)):i(`v-if`,!0),r(q)?(e(),n(`div`,{key:1,innerHTML:r(q)},null,8,F)):i(`v-if`,!0)]))}};export{I as t};