import { Prolog, load } from 'trealla'

await load()
const pl = new Prolog()

// Queries are async generators.
// You can run multiple queries against the same interpreter simultaneously.

try {
// Read the file asynchronously
  const file = await fetch('./parser.pl').then(res => res.text())
  //   console.log(file)
  await pl.consultText(file)
// Return the file content
}
catch (err) {
  console.error('Error reading file:', err)
  throw err
}

export default async function parse(tokens: string[]) {
  const result = await pl.queryOnce(`parser(Tree, [${tokens}], []).`, { format: 'json', encode: { atoms: 'string' } })
  if (result.status === 'success')
    return result.answer.Tree
  else
    return null
}
