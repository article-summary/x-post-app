import streamlit as st
from newspaper import Article
import openai

# ✅ OpenAIクライアント設定
client = openai.OpenAI(
    api_key="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"
)

st.title("🧠 URLからX投稿ジェネレーター")

url = st.text_input("📎 記事のURLを貼ってください")

# オプション選択 UI
style = st.selectbox("🗣️ 投稿スタイル", ["ビジネス寄り", "カジュアル", "皮肉っぽく"])
tone = st.selectbox("🎭 感想トーン", ["ポジティブ", "ネガティブ"])
emoji = st.selectbox("😎 絵文字", ["あり", "なし"])

if url:
    with st.spinner("記事を読み込み中..."):
        # 記事取得
        article = Article(url)
        article.download()
        article.parse()
        title, content = article.title, article.text

        # 🎯 要約＋感想プロンプト
        summary_prompt = f"""
以下はWeb記事のタイトルと本文です。

【タイトル】
{title}

【本文】
{content}

この内容を、わかりやすく2〜3行で要約してください。
その後、30代男性の視点で「{tone}」な感想を1〜2行添えてください。
文体はフラットかつ自然に。
"""

        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.7,
        )
        summary_output = summary_response.choices[0].message.content.strip()

        # 📝 X投稿風プロンプト
        x_post_prompt = f"""
以下はWeb記事のタイトルと本文です。

【タイトル】
{title}

【本文】
{content}

この記事の内容を、30代男性の口調で「X（旧Twitter）」投稿っぽく紹介してください。

- 投稿スタイルは「{style}」
- 感想は「{tone}」
- 絵文字は{"使ってOK" if emoji == "あり" else "使わない"}

ポイントを要約しつつ、軽い感想を添えてください。
自然な改行を入れ、6行以内にまとめてください。
"""

        x_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": x_post_prompt}],
            temperature=0.8,
        )
        x_post_output = x_response.choices[0].message.content.strip()

        # ✅ 出力表示
        st.subheader("📌 要約 + 感想")
        st.write(summary_output)

        st.subheader("📝 X投稿風まとめ")
        st.write(x_post_output)
