"""Rebuild the static Sites output; set NOBLETON_SITE_ORIGIN for the live host."""
from pathlib import Path
import os, shutil, subprocess, sys

root=Path(__file__).resolve().parent
os.environ.setdefault('NOBLETON_SITE_ORIGIN','https://nobleton.dimagrafov.chatgpt.site')
subprocess.run([sys.executable,str(root/'work/build.py'),'--production'],check=True)
shutil.copytree(root/'outputs/nobleton-production',root/'dist',dirs_exist_ok=True)
for path in (root/'dist').rglob('*.html'):
    source=path.read_text()
    for old,new in [('This preview prepares an email','This form prepares an email'),('How the preview works','How the website works'),('This preview does not load','This website does not load'),('The preview web server may record','The hosting service may record'),('Preview notice ·','Privacy notice ·')]:
        source=source.replace(old,new)
    path.write_text(source)
subprocess.run([sys.executable,str(root/'work/bilingual.py'),str(root/'dist')],check=True)
