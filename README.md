# GitHub Auto Liker

自动为 GitHub 仓库点赞的工具，支持定时任务和 Bark 通知，基于https://gitstarhub.com/

## 功能特点

- 🕒 自动每 65 分钟运行一次
- 📱 支持 Bark 通知（可选）
- 🔄 自动处理点赞频率限制（每小时最多 5 次）
- 🔒 通过环境变量安全管理凭据
- 📝 详细的运行日志

## 安装

1. 克隆仓库：
```bash
git clone <repository_url>
cd autostar
```

2. 安装依赖：
```bash
# 使用 poetry（推荐）
poetry install

# 或使用 pip
pip install -e .
```

## 配置

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的凭据：
```ini
# GitHub 账号信息
GITHUB_USERNAME=你的用户名
GITHUB_PASSWORD=你的密码

# Bark 通知密钥（可选）
BARK_KEY=你的bark密钥
```

## 使用方法

### 直接运行

```bash
# 使用 poetry
poetry run auto-star

# 或直接使用 python
python -m auto_star
```

### 后台运行

```bash
# 使用 nohup
nohup python -m auto_star > auto_star.log 2>&1 &

# 查看运行日志
tail -f auto_star.log
```

## 运行说明

- 程序启动后会立即执行一次点赞任务
- 之后每隔 65 分钟自动执行一次
- 每次运行最多点赞 5 个仓库（API 限制）
- 通过 Ctrl+C 可以优雅退出程序

## Bark 通知

如果配置了 Bark 密钥，程序会在以下情况发送通知：
- 登录成功/失败
- 成功点赞仓库
- 达到点赞限制
- 发生错误

## 依赖项

- Python >= 3.8
- requests
- python-dotenv
- apscheduler


## 许可证

MIT License
