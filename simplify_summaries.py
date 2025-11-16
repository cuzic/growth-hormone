#!/usr/bin/env python3
"""
各章のまとめセクションを簡素化するスクリプト
"""
import re
from pathlib import Path

book_dir = Path('/home/cuzic/成長ホルモン治療/book')

def simplify_summary(content):
    """まとめセクションを簡素化"""

    # まとめセクションを見つける
    pattern = re.compile(
        r'(## (?:第\d+章の)?まとめ.*?\n)(.*?)(?=\n##|\n---|\Z)',
        re.DOTALL
    )

    def replace_summary(match):
        header = match.group(1)
        body = match.group(2)

        # 既に簡潔な場合はそのまま
        if len(body) < 500:
            return match.group(0)

        # 箇条書きのみを抽出
        bullet_points = []
        for line in body.split('\n'):
            stripped = line.strip()
            # 「**」で始まる重要ポイントを保持
            if stripped.startswith('**') or stripped.startswith('- **') or stripped.startswith('1. **'):
                bullet_points.append(line)
            # 通常の箇条書き（「-」「1.」で始まる）も保持（ただし長すぎる説明は除外）
            elif (stripped.startswith('- ') or re.match(r'^\d+\.', stripped)) and len(stripped) < 200:
                # 「次の章では」「ぜひ」などの励ましは削除
                if not any(word in stripped for word in ['次の章', 'ぜひ', 'お疲れ', '頑張', 'できます', '一緒に']):
                    bullet_points.append(line)

        # 励ましメッセージを削除（段落全体）
        # 「あなた」「お母さん」「できます」「頑張」などを含む段落を削除
        encouragement_keywords = [
            'あなたは',
            'お母さん',
            'できます',
            '頑張',
            '大丈夫',
            '一緒に',
            'ぜひ',
            '応援',
            '素晴らしい',
        ]

        # 簡潔なまとめを生成
        if bullet_points:
            simplified_body = '\n'.join(bullet_points)
            return f"{header}\n{simplified_body}\n"
        else:
            # 箇条書きが見つからない場合は、重要な情報のみ抽出
            lines = [l for l in body.split('\n') if l.strip() and not any(kw in l for kw in encouragement_keywords)]
            simplified_body = '\n'.join(lines[:10])  # 最大10行
            return f"{header}\n{simplified_body}\n"

    return pattern.sub(replace_summary, content)

# 各ファイルを処理
chapters_to_process = [
    '01_第1章.md',
    '02_第2章.md',
    '03_第3章.md',
    '04_第4章.md',
    '05_第5章.md',
    '06_第6章.md',
    '07_第7章.md',
    '08_第8章.md',
    '09_第9章.md',
    '10_第10章.md',
    '11_第11章.md',
]

stats = []
for filename in chapters_to_process:
    filepath = book_dir / filename
    if not filepath.exists():
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    # まとめセクションのサイズを測定（before）
    summary_pattern = re.compile(r'## (?:第\d+章の)?まとめ.*?\n(.*?)(?=\n##|\n---|\Z)', re.DOTALL)
    match = summary_pattern.search(original)
    original_summary_len = len(match.group(1)) if match else 0

    # 簡素化
    simplified = simplify_summary(original)

    # まとめセクションのサイズを測定（after）
    match_after = summary_pattern.search(simplified)
    new_summary_len = len(match_after.group(1)) if match_after else 0

    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(simplified)

    if original_summary_len > 0:
        reduction = ((original_summary_len - new_summary_len) / original_summary_len) * 100
        stats.append((filename, original_summary_len, new_summary_len, reduction))
        print(f"✓ {filename:25s} {original_summary_len:4d}文字 → {new_summary_len:4d}文字 ({reduction:.0f}%削減)")

print()
print("=" * 70)
total_original = sum(s[1] for s in stats)
total_new = sum(s[2] for s in stats)
total_reduction = ((total_original - total_new) / total_original) * 100 if total_original > 0 else 0
print(f"合計: {total_original}文字 → {total_new}文字 ({total_reduction:.0f}%削減)")
print("=" * 70)
