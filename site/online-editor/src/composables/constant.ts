// Assuming you have already included the yaml library in your HTML using a script tag
import yaml from 'js-yaml'

// Relative path to the YAML file
const path = 'kage.yaml'

// Function to load the YAML file asynchronously
const kage_yaml = await fetch(path).then(res => res.text())

// Function to parse the YAML content and process it
const d = yaml.load(kage_yaml) as { [key: string]: { [key: string]: string } }
const HUI_FINGER = sortedKeys(d['徽位指法'])
const XIAN_FINGER = sortedKeys(d['弦序指法'])
const MOVE_FINGER = sortedKeys(d['走位指法'])
const SPECIAL_FINGER = sortedKeys(d['特殊指法'])
const MODIFIER = sortedKeys(d['修饰'])
const BOTH_FINGER = sortedKeys(d['联袂指法'])
const COMPLEX_FINGER = sortedKeys(d['复式指法'])
const MARKER = sortedKeys(d['记号'])

const NUMBER = ['十一', '十二', '十三', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '外', '半']
const HUI_FINGER_ALL = ['大', '食', '中', '名', '跪', '散']
export const ALL = [...HUI_FINGER_ALL, ...XIAN_FINGER, ...MOVE_FINGER, ...SPECIAL_FINGER, ...BOTH_FINGER, ...COMPLEX_FINGER, ...MODIFIER, ...MARKER, ...NUMBER]

// Helper function to sort object keys
function sortedKeys(obj: { [key: string]: any }): string[] {
  return Object.keys(obj).sort((a, b) => b.length - a.length)
}
