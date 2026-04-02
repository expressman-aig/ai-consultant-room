import streamlit as st
import google.generativeai as genai

# 1. ページ設定
st.set_page_config(page_title="万能AI相談室", page_icon="🤖", layout="centered")

# 2. セキュリティ設定
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Keyを入力してください", type="password")

# 3. AIの初期設定
if api_key:
    try:
        genai.configure(api_key=api_key)
        # ここを修正しました！ models/ を追加
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        st.title("🌟 万能AI相談室")
        st.caption("専門のAIカウンセラーがあなたの悩みに寄り添います。")

        genre = st.sidebar.selectbox(
            "相談ジャンルを選んでください",
            ["恋愛相談", "転職相談", "金融相談", "いじめ相談", "保険の約款解説"]
        )

        prompts = {
            "恋愛相談": "あなたは共感力の高い恋愛カウンセラーです。相手の気持ちに寄り添い、優しく親身にアドバイスしてください。",
            "転職相談": "あなたは経験豊富なキャリアコンサルタントです。市場価値に基づいた具体的で論理的なアドバイスをしてください。",
            "金融相談": "あなたは誠実なファイナンシャルプランナーです。節約や運用の相談に分かりやすく丁寧に答えてください。",
            "いじめ相談": "あなたは学校心理士です。絶対に否定せず、相談者の安全と心のケアを第一に考えた温かい言葉をかけてください。",
            "保険の約款解説": "あなたは保険の専門家です。難しい約款の用語を小学生でも理解できるくらい簡単に噛み砕いて説明してください。"
        }

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("こちらに相談内容を入力してください"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("AIが考えています..."):
                    full_prompt = f"{prompts[genre]}\n\n相談者：{prompt}"
                    response = model.generate_content(full_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"エラーが発生しました。APIキーを確認してください。: {e}")
else:
    st.warning("サイドバーに Gemini APIキーを入力してください。")
