"""Create a source + generated-site archive without local dependencies."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'artifacts' / 'digital-buro-refonte.zip'
ROOT_FILES = ['build.py', 'requirements.txt', 'README.md', 'CHANGELOG.md',
              '.gitignore', '.gitattributes', 'PROMPT_CHATGPT.md']
files = [ROOT / name for name in ROOT_FILES if (ROOT / name).is_file()]
for name in ('src', 'public', 'tools', 'artifacts'):
    for path in (ROOT / name).rglob('*'):
        if not path.is_file():
            continue
        if any(part in ('qa-deps', '__pycache__', 'node_modules') for part in path.parts):
            continue
        if path.suffix in ('.zip', '.pyc') or path.name.startswith('test-'):
            continue
        files.append(path)
with zipfile.ZipFile(TARGET, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(set(files)):
        archive.write(path, path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(TARGET) as archive:
    assert archive.testzip() is None
    assert 'public/.htaccess' in archive.namelist()
    assert 'src/templates/partials/fresh-macros.html' in archive.namelist()
print(f'{len(files)} files — {TARGET.stat().st_size / 1024 / 1024:.1f} MB — {TARGET}')
