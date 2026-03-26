import codecs
import json
import os
import xml.etree.ElementTree as ET

import fontforge

FONT_PATH = ""
FONT_FILE = ""
# Get the current font, set HOME_PATH and FILE_NAME
# current_font = fontforge.activeFont()
# if current_font is not None:
#     file_path = current_font.path
#     if file_path is not None:
#         HOME_PATH = os.path.dirname(file_path)
#         FILE_NAME = os.path.basename(file_path)
#     else:
#         print("No file is currently open.")
# else:
#     print("No active font found.")

with codecs.open(FONT_PATH + '/charMap.json', 'r', 'utf-8') as dataFile:
    data = dataFile.read()
    obj = data[data.find('{') : data.rfind('}')+1]
    charMap = json.loads(obj)
    
font = fontforge.open(FONT_PATH + '/' + FONT_FILE)
unicodes = []
for layout in charMap:
  if layout == "spacer":
    glyph = font.createChar(charMap[layout]['unicode'])
    glyph.clear()
    glyph.width = 1000
    glyph.glyphname = 'spacer_' + str(charMap[layout]['unicode'])
    continue

  if layout == "spacers":
    for spacer in charMap[layout]:
      glyph = font.createChar(charMap[layout][spacer]['unicode'])
      glyph.clear()
      glyph.width = charMap[layout][spacer]['width']
      glyph.glyphname = 'spacer_' + spacer
    continue

  for area in charMap[layout]['areas']:
    print("======" + area + "======")
    areaObj = charMap[layout]['areas'][area]
    print(str(areaObj['h']) + ', ' + str(areaObj['w']))
    for component in areaObj['components']:
      # print(component) # note: this errors out for some reason
      # check if component is already in font
      if component['unicode'] in unicodes:
        print('Already in font')
        continue

      # handle case of using characters instead of custom unicode
      if area == "character":
        glyph = font.createChar(fontforge.unicodeFromName(component['keys'][0]))
      else:
        glyph = font.createChar(component['unicode'])
      glyph.clear()
      
      if component['filename'] != 'empty':
        # import SVG
        fp = FONT_PATH+'/components/' + component['filename'] + '.svg'
        glyph.importOutlines(fp, scale=False)
        

        # scale to SVG
        svg = ET.parse(fp)
        root = svg.getroot()
        svgWidth = float(root.attrib['width'].replace('px', ''))
        svgHeight = float(root.attrib['height'].replace('px', ''))
        bb = glyph.boundingBox()
        scaleWidth = areaObj['w'] / svgWidth
        scaleHeight = areaObj['h'] / svgHeight
        if 'scale' in component.keys():
          if component['scale'] == 'lockRatio':
            scaleHeight = min(scaleHeight, scaleWidth)
            scaleWidth = min(scaleHeight, scaleWidth)

        scoochY = 800-scaleHeight*800

        # Import, scale, and scooch
        glyph.transform((scaleWidth, 0.0, 0.0, scaleHeight, 0, 0)) # scaleX, skewX, skewY, scaleY, positionX, positionY
        glyph.transform((1, 0.0, 0.0, 1, 0, 800-800*scaleHeight)) 
        glyph.transform((1, 0.0, 0.0, 1, areaObj['x'], -areaObj['y'])) 
        
        # Clean up
        glyph.removeOverlap()
        glyph.addExtrema()

      # Change widths
      if area == "char":
        glyph.width = component['width']
      else:
        glyph.width = component['width']

      # Rename
      if area == "char":
        glyph.glyphname = component['keys'][0]
      else:
        glyph.glyphname = 'u' + str(component['unicode'])
      
      # add to unicodes array
      unicodes.append(component['unicode'])
print('ALL DONE!')