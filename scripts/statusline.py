"""Claude Code 状态栏脚本

从 stdin 读取 CLI 传入的 JSON，输出一行状态栏文本：
    上下文: xx% | 模型: xxx | 📝 <最近修改的文件完整路径>
"""

import json
import os
import sys


data = json.load(sys.stdin)

pct = data.get('context_window', {}).get('used_percentage')
model = data.get('model', {}).get('display_name', '')

# 最近修改文件由 hooks/track_modified.py 写入
last_modified_file = os.path.expanduser('~/.claude/last_modified_file.txt')
modified_file = ''
try:
    with open(last_modified_file, 'r', encoding='utf-8') as f:
        modified_file = f.read().strip()
except (FileNotFoundError, OSError):
    pass

parts = []
if pct:
    parts.append(f'上下文: {int(pct)}%')
if model:
    parts.append(f'模型: {model}')
if modified_file:
    parts.append(f'📝 {modified_file}')

print(' | '.join(parts))
