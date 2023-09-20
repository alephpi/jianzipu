# 解析完整的古琴曲谱篇章
import yaml
import pprint as pp
def parse_file(file_path):
    song_info = {}
    paragraph = []
    with open(file_path, "r", encoding="utf-8") as f:
        
        frontmatter, text  = f.read().split('---')
        song_info = yaml.safe_load(frontmatter.strip())
        for line in text.strip().splitlines():
          paragraph.extend(line.split(' '))
    pp.pprint(song_info)
    pp.pprint(paragraph)