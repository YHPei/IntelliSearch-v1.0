# 🚀 快速启动指南

本指南将帮助您在 5 分钟内启动智能搜索增强应用。

---

## 📋 前置准备

### 1. 获取 API 密钥

#### OpenAI API Key
1. 访问 https://platform.openai.com/api-keys
2. 登录或注册账号
3. 点击 "Create new secret key"
4. 复制并保存您的 API Key

#### SearchCans API Key
1. 访问 https://global.searchcans.com/
2. 注册账号
3. 在 Dashboard 中找到您的 API Key
4. 复制并保存
5. 优势：响应稳定、速度快、价格实惠，支持 Google 和 Bing

---

## ⚡ 快速启动（推荐）

### Windows 用户

#### 1. 启动后端
```cmd
cd backend
start_backend.bat
```

#### 2. 启动前端（新开一个终端）
```cmd
cd frontend
start_frontend.bat
```

### macOS/Linux 用户

#### 1. 启动后端
```bash
cd backend
chmod +x start_backend.sh
./start_backend.sh
```

#### 2. 启动前端（新开一个终端）
```bash
cd frontend
chmod +x start_frontend.sh
./start_frontend.sh
```

---

## 🔧 手动启动

### 后端部署

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
# Windows:
copy env.example .env

# macOS/Linux:
cp env.example .env

# 5. 编辑 .env 文件，填入您的 API 密钥
# OPENAI_API_KEY=sk-your-key-here
# SEARCHCANS_API_KEY=your-key-here

# 6. 启动后端
python main.py
```

✅ 后端现在运行在：http://127.0.0.1:8000

### 前端部署

```bash
# 1. 进入前端目录（新开终端）
cd frontend

# 2. 安装依赖
npm install

# 3. （可选）配置环境变量
# Windows:
copy env.example .env

# macOS/Linux:
cp env.example .env

# 4. 启动前端
npm run dev
```

✅ 前端现在运行在：http://localhost:5173

---

## ✅ 验证部署

### 检查后端
访问：http://127.0.0.1:8000/health

应该看到：
```json
{
  "status": "healthy",
  "services": {
    "openai": "configured",
    "serp": "configured"
  }
}
```

### 检查前端
访问：http://localhost:5173

应该看到智能搜索助手界面。

---

## 🎯 开始使用

1. 选择搜索引擎（Google 或 Bing）
   
2. 在输入框中输入问题，例如：
   - "2024年人工智能最新突破有哪些？"
   
3. 点击"🚀 开始搜索"按钮

4. 等待 3-10 秒

5. 查看 AI 生成的回答和参考来源

---

## ❓ 常见问题

### Q: 后端启动失败
**A:** 检查：
- Python 版本是否 >= 3.8
- 是否正确配置了 `.env` 文件
- API 密钥是否有效（OpenAI 和 SearchCans）

### Q: 前端无法连接后端
**A:** 确保：
- 后端服务正在运行（http://localhost:8000/health 可访问）
- 防火墙没有阻止 8000 端口
- 浏览器控制台没有 CORS 错误

### Q: 搜索返回错误
**A:** 检查：
- OpenAI API 账户余额是否充足
- SearchCans API 密钥是否有效
- 是否选择了正确的搜索引擎（Google 或 Bing）
- 后端日志中的详细错误信息

---

## 📚 更多信息

详细文档请查看：[README.md](README.md)

API 文档：http://127.0.0.1:8000/docs

---

**祝您使用愉快！🎉**

