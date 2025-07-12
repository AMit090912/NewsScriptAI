# 📰 NewsScriptAI

**Automatically extract news, summarize with AI, and generate ready-to-use scripts.**  
Perfect for content creators, YouTubers, or anyone wanting quick, script-ready news updates.

---

## ⚙️ Features

- 🔎 Fetch news from multiple sources (via NewsAPI)
- 📄 Extract full article content using `newspaper3k`
- 🧠 Summarize using `T5` transformer (Hugging Face)
- 📝 Format as YouTube-style script (intro, headlines, outro)

---

## 🚀 How to Use

1. **Install requirements**

```bash
pip install requests newspaper3k transformers torch
```
2. **Extract news**
run python extract_news.py

3. **Summarize and generate script**
run python summarize_script.py

full_news_*.txt → Extracted news
youtube_script_*.txt → Final script
