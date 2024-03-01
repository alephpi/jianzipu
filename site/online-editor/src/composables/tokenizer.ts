function tokenize(s: string): string[] {
  const sep = /指|徽|分|弦|音/
  const simplified = s.replace(sep, ' ')
  const keepPattern = ALL.join('|')
  const tokens = simplified.split(new RegExp(`(${keepPattern})`))
  const filteredTokens = tokens.filter(x => x.trim() !== '')
  return filteredTokens
}

export function tokenize_paragraph(p: string): string[][] {
  const l = p.split(' ')
  return l.map(tokenize)
}
