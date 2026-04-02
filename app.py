import streamlit as st
import google.generativeai as genai

# 1. ページ設定
st.set_page_config(page_title="万能AI相談室", page_icon="🤖")

# 2. APIキーの取得
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Keyを入力してください", type="password")

# 3. AIの初期設定
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 最新の安定版モデルを指定
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🌟 万能AI相談室")
        
        genre = st.sidebar.selectbox(
            "相談ジャンルを選んでください",
            ["恋愛相談", "転職相談", "金融相談", "いじめ相談", "保険の約款解説"]
        )

        prompts = {
            "恋愛相談": "あなたは共感力の高い恋愛カウンセラーです。優しく親身にアドバイスしてください。",
            "転職相談": "あなたは経験豊富なキャリアコンサルタントです。論理的で前向きな転職のアドバイスをしてください。",
            "金融相談": "あなたは誠実なファイナンシャルプランナーです。分かりやすく丁寧に答えてください。",
            "いじめ相談": "あなたは学校心理士です。絶対に否定せず、相談者の心のケアを第一に考えてください。",
            "保険の約款解説": "あなたは保険の専門家です。難しい約款を小学生でもわかるように簡単に解説してください。"
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
                    # ここが最新の呼び出し方です
                    full_prompt = f"{prompts[genre]}\n\n相談者：{prompt}"
                    response = model.generate_content(full_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.warning("APIキーを入力してください。")
