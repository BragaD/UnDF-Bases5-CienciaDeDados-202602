// Contas e formatação partilhadas pelos componentes interativos.
export const sig = (z) => 1 / (1 + Math.exp(-z))
export const degrau = (z) => (z >= 0 ? 1 : 0)

// número em pt-BR: vírgula decimal e sinal de menos tipográfico
export function n(v, d = 3) {
  if (!Number.isFinite(v)) return v > 0 ? '∞' : '−∞'
  let s = Math.abs(v).toFixed(d)
  const neg = v < 0 && Number(s) !== 0
  return (neg ? '−' : '') + s.replace('.', ',')
}
export const par = (v, d = 3) => (v < 0 ? `(${n(v, d)})` : n(v, d))

export const X4 = [[0, 0], [0, 1], [1, 0], [1, 1]]
export const PORTAS = { E: [0, 0, 0, 1], OU: [0, 1, 1, 1], XOR: [0, 1, 1, 0] }

// gerador com semente (mulberry32) e normal por Box-Muller
export function sorteio(semente) {
  let a = semente >>> 0
  const u = () => {
    a = (a + 0x6d2b79f5) >>> 0
    let t = a
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
  return () => Math.sqrt(-2 * Math.log(1 - u())) * Math.cos(2 * Math.PI * u())
}
