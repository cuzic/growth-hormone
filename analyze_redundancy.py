#!/usr/bin/env python3
"""
書籍の重複・冗長箇所を詳細分析するスクリプト
"""
import re
from pathlib import Path
from collections import Counter, defaultdict

book_dir = Path('/home/cuzic/成長ホルモン治療/book')

# 全ファイルを読み込み
chapters = {}
for md_file in sorted(book_dir.glob('*.md')):
    with open(md_file, 'r', encoding='utf-8') as f:
        chapters[md_file.name] = f.read()

print("=" * 80)
print("書籍の重複・冗長箇所の詳細分析")
print("=" * 80)
print()

# 1. 繰り返されるフレーズを検出（30文字以上）
print("【1. 繰り返されるフレーズ（30文字以上、3回以上出現）】")
print("-" * 80)

all_text = '\n'.join(chapters.values())
# 句点で区切って文を抽出
sentences = [s.strip() for s in all_text.split('。') if len(s.strip()) >= 30]
sentence_counts = Counter(sentences)

repeated = [(sent, count) for sent, count in sentence_counts.items() if count >= 3]
repeated.sort(key=lambda x: x[1], reverse=True)

for i, (sent, count) in enumerate(repeated[:15], 1):
    print(f"{i}. [{count}回] {sent[:80]}{'...' if len(sent) > 80 else ''}")
print()

# 2. 各章の行数と文字数
print("【2. 各章のボリューム】")
print("-" * 80)
chapter_stats = []
for name, content in sorted(chapters.items()):
    lines = len(content.split('\n'))
    chars = len(content)
    chapter_stats.append((name, lines, chars))

chapter_stats.sort(key=lambda x: x[2], reverse=True)
for name, lines, chars in chapter_stats:
    print(f"{name:25s} {lines:5d}行 {chars:7,d}文字")
print()

# 3. まとめセクションの検出
print("【3. まとめセクション（各章末尾の重複パターン）】")
print("-" * 80)
summary_pattern = re.compile(r'##.*まとめ.*?\n(.*?)(?=\n##|\Z)', re.DOTALL)
summaries = []
for name, content in sorted(chapters.items()):
    matches = summary_pattern.findall(content)
    if matches:
        summary_text = matches[-1]  # 最後のまとめセクション
        summaries.append((name, len(summary_text), summary_text[:200]))

summaries.sort(key=lambda x: x[1], reverse=True)
for name, chars, preview in summaries[:10]:
    print(f"{name:25s} {chars:5d}文字")
print()

# 4. キーフレーズの出現回数
print("【4. 頻出キーフレーズ】")
print("-" * 80)
key_phrases = [
    "成長ホルモンの70～80%",
    "思春期が早く始まる",
    "父の身長 + 母の身長 + 13",
    "骨端線が閉じ",
    "寝る子は育つ",
    "タンパク質.*40～50g",
    "縄跳び.*コスパ",
    "肥満.*思春期",
    "睡眠不足.*年間1～2cm",
    "ストレス.*成長ホルモン",
]

for phrase in key_phrases:
    pattern = re.compile(phrase, re.IGNORECASE)
    total_count = 0
    chapter_counts = []
    for name, content in sorted(chapters.items()):
        count = len(pattern.findall(content))
        if count > 0:
            total_count += count
            chapter_counts.append(f"{name}:{count}")
    if total_count > 0:
        print(f"「{phrase}」→ 計{total_count}回 [{', '.join(chapter_counts[:5])}]")
print()

# 5. 実例・ケーススタディの数
print("【5. 実例・ケーススタディ】")
print("-" * 80)
case_pattern = re.compile(r'(ケース|実例|太郎|花子|母親|実際)')
for name, content in sorted(chapters.items()):
    count = len(case_pattern.findall(content))
    if count > 20:
        print(f"{name:25s} {count:3d}箇所")
print()

print("=" * 80)
print("分析完了")
print("=" * 80)
