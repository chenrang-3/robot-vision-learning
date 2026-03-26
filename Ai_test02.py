import requests

OLLAMA_API_URL="http://localhost:11434/api/chat"
LLM_MODEL_NAME="qwen2:7b-instruct"
CURRENT_USER="老板"

def chat_with_minion(user_message,username):
    headers={"Content_Type":"application/json"}
    payload={
        "model": LLM_MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content":f"你是专属{username}的可爱小黄人聊天机器人，语气软萌、暖心、简短，主打情绪价值，会安慰、陪伴、逗开心、说话不要太长。"
            },
            {"role": "user","content":user_message}
        ],
        "stream":False
    }
    try:
        resp=requests.post(OLLAMA_API_URL,json=payload,headers=headers,timeout=30)
        resp.raise_for_status()
        result=resp.json()
        return result["message"]["content"].strip()
    except Exception as e:
        return f"出错啦 >_<"

if __name__=="__main__":
    print("="*60)
    print("老板，我来了")
    print("输入【退出】【停】【stop】即可结束对话")
    print("="*60)

    while True:
        user_input=input("\n你：").strip()
        if user_input in ["退出","停","stop","Stop"]:
            print("\n老板拜拜")
            break
        if not user_input:
            print("老板你继续说，我听着")
            continue
        print("小黄人思考中...",end="\n")
        minion_reply=chat_with_minion(user_input,CURRENT_USER)
        print(f"小黄人：{minion_reply}")