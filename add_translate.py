import glob
import os

snippet = """
<div id="google_translate_element"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}
</script>
<script type="text/javascript" src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
"""

for f in glob.glob('public/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'googleTranslateElementInit' not in content:
        content = content.replace('</body>', snippet)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
