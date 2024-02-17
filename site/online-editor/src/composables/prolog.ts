import { Prolog, load, toJSON } from 'trealla'

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
//   console.log(`parser(Tree, ${tokens}, [])`)
  const result = await pl.queryOnce(`parser(Tree, [${tokens}], [])`, { program: 'prolog' })
  if (result.status === 'success')
    return result.answer.Tree.toString()
    // return JSON.parse(result.answer.Tree.toString())
  else
    return null
}
