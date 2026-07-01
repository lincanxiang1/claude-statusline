# claude-statusline

一个 [Claude Code](https://docs.claude.com/en/docs/claude-code) 状态栏插件，在终端底部实时显示：

- 上下文使用率百分比
- 当前使用的模型
- **最近读/写/编辑的文件完整路径**

## 效果

```
上下文: 42% | 模型: claude-sonnet-4-6 | 📝 D:\project\src\main.py
```

📝 会随你每次调用 Read / Write / Edit / MultiEdit / NotebookEdit 自动更新。

## 安装

```bash
# 1. 添加 marketplace（把 <owner> 换成你的 GitHub 用户名或组织名）
/plugin marketplace add <owner>/claude-statusline

# 2. 安装
/plugin install claude-statusline
```

安装后 Claude Code 会自动注入 `statusLine` 配置和 `PostToolUse` Hook，**不需要手动改 settings.json**。

## 前置要求

- Python 3.6+（脚本用了 f-string，绝大多数系统自带）
- Claude Code CLI

Windows 用户注意：脚本已经用 `python -X utf8` 启动，避免中文乱码。

## 工作原理

```
┌─────────────────────┐
│  Claude Code CLI    │
│  (每帧 stdin 传 JSON) │──────┐
└─────────────────────┘      │
        ▲                    ▼
        │           ┌──────────────────────┐
        │           │  scripts/statusline.py │
        │  print    │  读 JSON + 追踪文件    │
        │           │  print 一行文本        │
        │           └──────────────────────┘
        │                    ▲
        │                    │ 读
        │        ~/.claude/last_modified_file.txt
        │                    ▲
        │                    │ 写
        │           ┌──────────────────────┐
        │  每次工具调用 │ hooks/track_modified.py │
        └──────────│  PostToolUse hook      │
                   └──────────────────────┘
```

## 目录结构

```
claude-statusline/
├── .claude-plugin/
│   └── plugin.json           # 插件元数据：注册 statusLine + hooks
├── hooks/
│   └── track_modified.py     # PostToolUse hook，写入最近修改文件
├── scripts/
│   └── statusline.py         # 状态栏主脚本
├── README.md
├── LICENSE
└── .gitignore
```

## 常见问题

### Q1. 状态栏不显示

1. 确认已启用插件：`/plugin list`
2. 手动测试脚本：
   ```bash
   echo '{"model":{"display_name":"test"},"context_window":{"used_percentage":42}}' | python -X utf8 scripts/statusline.py
   ```
   预期输出：`上下文: 42% | 模型: test`

### Q2. 📝 一直显示同一个文件不更新

1. 确认 hook 已注册：`/hooks`
2. 手动检查追踪文件：
   ```bash
   # Windows
   type %USERPROFILE%\.claude\last_modified_file.txt
   # macOS / Linux
   cat ~/.claude/last_modified_file.txt
   ```

### Q3. Windows 中文乱码

插件已用 `python -X utf8` 启动。如果仍乱码，检查终端字体是否支持中文。

### Q4. 想禁用插件

```
/plugin disable claude-statusline
```

或直接卸载：`/plugin uninstall claude-statusline`

## 自定义

想改显示内容？直接编辑 `scripts/statusline.py`。文件很短（约 30 行），随便改。

常见改法：

- **改语言**：把 `上下文` / `模型` 替换成英文即可
- **加目录显示**：把 `data.get('cwd')` 拼进 `parts` 即可
- **加 Git 分支**：调 `git rev-parse --abbrev-ref HEAD` 拼进去

## License

MIT
