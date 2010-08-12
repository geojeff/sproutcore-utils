import elementtree.ElementTree as ET
from glob import iglob
import os

PATH = r'/Users/geojeff/Development/sproutcore/vim/sproutcore-tmbundle/Snippets/'

snippet_file = open('sproutcore.snippets', 'w')
for filename in iglob('*.tmSnippet'):
    tree = ET.parse(filename)
    snippet = ET.tostring(tree.find('dict/string'))
    snippet = snippet.replace('<string>', '').replace('</string>', '')
    snippet_file.write('snippet %s\n' % filename[:filename.find('.')])
    for line in snippet.split('\n'):
        snippet_file.write('\t%s\n' % line) 
    
snippet_file.close()

