// Lançamento de nota + feedback no AVA (Moodle, mod_assign), pela sessão já logada do professor.
// Rodar com a ferramenta de JavaScript do navegador, numa aba aberta em QUALQUER página
// do ava.undf.edu.br (o M.cfg.sesskey vem da página). Testado em 11/11/2026.
//
// Passo 0 — descobrir userids e ids da tarefa (cmid é o id da URL da tarefa):
//
//   const html = await fetch(`/mod/assign/view.php?id=${cmid}&action=grading&perpage=-1`).then(r => r.text());
//   -> cada linha da tabela tem input[name="selectedusers"] cujo value é o userid.
//   const g = await fetch(`/mod/assign/view.php?id=${cmid}&action=grader&userid=${umUserid}`).then(r => r.text());
//   -> contextid:    g.match(/"contextid":(\d+)/)[1]
//   -> assignmentid: g.match(/data-assignmentid="(\d+)"/)[1]
//
// Atenção: a ferramenta bloqueia saídas que pareçam cookie/query string. Devolva só
// campos curtos (ids, notas, tamanhos), nunca URLs inteiras nem HTML cru.

window.__ajax = async (methodname, args) => {
  const r = await fetch(`/lib/ajax/service.php?sesskey=${M.cfg.sesskey}&info=${methodname}`, {
    method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify([{ index: 0, methodname, args }]),
  });
  const j = await r.json();
  if (j[0].error) throw new Error(JSON.stringify(j[0].exception).slice(0, 300));
  return j[0].data;
};

// Busca o formulário de avaliação do aluno (traz o itemid do editor), preenche e envia.
// e = {u: userid, g: nota, h: feedback em HTML}. Retorno com res: [] significa sucesso.
// O formulário vem com sendstudentnotifications=true: o aluno é notificado.
window.__post = async (contextid, assignmentid, e) => {
  const frag = await window.__ajax('core_get_fragment', {
    component: 'mod_assign', callback: 'gradingpanel', contextid,
    args: [{ name: 'userid', value: String(e.u) }, { name: 'attemptnumber', value: '-1' }, { name: 'jsonformdata', value: '""' }],
  });
  const form = new DOMParser().parseFromString(frag.html, 'text/html').querySelector('form');
  if (!form) return { u: e.u, err: 'sem formulário' };
  const fd = new FormData(form);
  const antes = { nota: fd.get('grade'), fb: (fd.get('assignfeedbackcomments_editor[text]') || '').length };
  fd.set('grade', String(e.g));
  fd.set('assignfeedbackcomments_editor[text]', e.h);
  fd.set('sesskey', M.cfg.sesskey);
  const res = await window.__ajax('mod_assign_submit_grading_form', {
    assignmentid, userid: e.u, jsonformdata: JSON.stringify(new URLSearchParams(fd).toString()),
  });
  return { u: e.u, antes, res };
};

// Uso: primeiro UM aluno, conferir, depois os demais.
//
//   const PAYLOAD = [ ...saída do montar_payload.py... ];
//   const out = [];
//   for (const e of PAYLOAD) {
//     try { const r = await window.__post(CONTEXTID, ASSIGNMENTID, e);
//           out.push(e.u + ':' + (r.err || (r.antes.nota || 'vazio') + '>' + e.g + ' ' + JSON.stringify(r.res))); }
//     catch (x) { out.push(e.u + ':ERR ' + String(x).slice(0, 150)); }
//   }
//   out.join(' | ')
//
// Se `antes.nota` NÃO vier vazio, o aluno já tinha nota: pare e pergunte ao professor
// antes de sobrescrever.
//
// Conferência final: reler a tabela de avaliação (action=grading&perpage=-1) e comparar
// a coluna "Nota final" de cada userid com o JSON de correção.
