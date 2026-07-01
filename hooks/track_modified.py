"""PostToolUse Hook: 记录最近被文件类工具操作的绝对路径。

写入 ~/.claude/last_modified_file.txt，供 scripts/statusline.py 读取显示。
"""

import json
import os
import sys

STATE_FILE = os.path.expanduser('~/.claude/last_modified_file.txt')

# 只关心这些工具的操作对象
FILE_TOOLS = {'Read', 'Write', 'Edit', 'NotebookEdit', 'MultiEdit'}


def save(path):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            f.write(path)
    except OSError:
        pass


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    tool_name = data.get('tool_name', '')
    if tool_name not in FILE_TOOLS:
        return

    tool_input = data.get('tool_input', {}) or {}
    path = (
        tool_input.get('file_path')
        or tool_input.get('notebook_path')
        or ''
    )
    if not path:
        return

    try:
        save(os.path.abspath(path))
    except (OSError, ValueError):
        pass


if __name__ == '__main__':
    main()
