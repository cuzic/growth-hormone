#!/usr/bin/env python3
import re
from pathlib import Path

# Read the combined markdown
with open('book_combined.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all image references
pattern = r'\.\./diagrams/(fig\d+_[a-z0-9_]+\.png)'
images = re.findall(pattern, content)
unique_images = sorted(set(images))

print(f"マークダウン中の画像参照: {len(unique_images)}個")
print()

missing = []
for img in unique_images:
    img_path = Path('diagrams') / img
    if img_path.exists():
        print(f"✓ {img}")
    else:
        print(f"✗ MISSING: {img}")
        missing.append(img)

print()
if missing:
    print(f"エラー: {len(missing)}個の画像ファイルが見つかりません")
    for m in missing:
        print(f"  - {m}")
else:
    print("✓ すべての画像ファイルが存在します！")
