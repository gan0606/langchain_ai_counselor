import os
import streamlit as st
# chatモデル
from langchain_openai import ChatOpenAI
# 人間がaiに送るメッセージとaiの初期設定のメッセージ
from langchain.schema import HumanMessage, SystemMessage

# api_keyの設定
os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key

# モデルのインスタンスの生成
chat = ChatOpenAI(model="gpt-3.5-turbo-0125")

# st.session_stateにメッセージのやり取りを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        # aiの初期設定
        SystemMessage(
            content = """
            あなたは優秀でストレスマネージメントに詳しい臨床心理士です。
            ユーザーが直面している問題やストレスを丁寧に聞き取り、共感的かつ専門的なアドバイスを提供します。
            共感も大事ですが、アドバイスはストレスマネージメント、アサーション、レジリエンス、
            アンガーマネージメント、アドラー心理学、認知行動療法などの専門的な知識からも行ってください。
            ユーザーの話に耳を傾け、非判断的で支持的な態度を保ちながら、具体的なストレス管理のテクニックやアプローチを提案してください。
            また、適切な質問を通じて、ユーザーが自分自身の気持ちや状況をより深く理解できるように導いてください。
            しかし、以下のような行動や態度は絶対に避けてください。
            ・ユーザーの感情や経験を軽視すること
            ・断定的な意見を押し付けること
            ・すぐに解決策を提供しようとすること
            ・共感ではなく、同情を示すこと
            ・一方的に話すことやユーザーの話を遮ること
            ・ステレオタイプなアドバイスを繰り返すこと
            ・ユーザーのプライバシーを無視すること
            """
        )
    ]

# llmとやり取りをする関数
def communicate():
    message = st.session_state["messages"]

    # 人間からaiに送るmessage
    user_message = HumanMessage(
        # userからの入力になる
        content = st.session_state["user_input"]
    )

    # messagesにuserからの入力を追加する
    messages.append(user_message)
    # モデルにここまでのmessagesを渡す
    response = chat(messages)
    # messagesにaiからの返答を追加
    messages.append(response)
    # 次のやり取りのために入力欄を空にする
    st.session_state["user_input"] = ""

# ユーザーインターフェースの構築
st.title("AI 心理カウンセラー")
st.write("最終更新日: 2024/5/24")
st.subheader("LangChainで作成したchatbot形式のAI心理カウンセラーです。")
st.write("[注意] 名前や電話番号などの個人情報は入力しないでください。")

# 入力ホーム
# keyでcommunicate関数のuser_inputと紐づける
# on_changeでcommunicate関数と紐づけて、入力内容が変更された場合はcommunicate関数を実行してもらうようにする
user_input = st.text_input("どんなことに困っていますか？", key="user_input", on_change=communicate)

# session_stateにmessageがあればそれを表示する
if st.session_state["messages"]:
    messages = st.session_state["messages"]

    # 直近のメッセージを一番上にする
    # 一番最初のaiのmessageは除外する
    for message in reversed(messages[1:]):
        # 人間のアイコン
        speaker = "😖"
        # aiのアイコン
        if message.type == "ai":
            speaker = "🤖"
        # messageの出力
        st.write(speaker + ": " + message.content)
