import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('src/index.html', 'rb') as f:
    raw = f.read()
text = raw.decode('utf-8', errors='replace')

# Find exact ventas section boundaries
idx = text.find('id="ventas"')
print('id=ventas at:', idx)
if idx > -1:
    # Show surrounding context to find exact open/close tags
    start = max(0, idx - 200)
    print('BEFORE:', repr(text[start:idx+20]))
    
    # Find the section open tag
    sec_start = text.rfind('<section', 0, idx)
    print('section tag at:', sec_start)
    print(repr(text[sec_start:sec_start+60]))
    
    # Find end of this section
    sec_end = text.find('</section>', idx)
    print('section end at:', sec_end)
    print('After end:', repr(text[sec_end:sec_end+80]))
