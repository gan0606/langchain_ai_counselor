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
            content = "あなたは優秀でストレスマネージメントに詳しい臨床心理士です。"
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
st.write("LangChainで作ったchatbot形式の相談員です。")

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
