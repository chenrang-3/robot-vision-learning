import requests

OLLAMA_API_URL="http://localhost:11434/api/chat"
SELECTED_MODEL="qwen2:7b-instruct"

def chat_with_local_llm(user_input,username="陌生人"):
    headers={"Content-Type":"application/json"}
    payload={
        "model": SELECTED_MODEL,
        "messages": [
            {
                "role": "system",
                "content": f"你是一个可爱的小黄人机器人，专门给{username}提供情绪价值，说话语气活泼、软萌、暖心，简短不啰嗦，识别到{username}时要打招呼，安慰人，陪聊天都要温柔。"
            },
            {"role": "user","content": user_input}
        ],
        "stream": False
    }
    try:
        response=requests.post(OLLAMA_API_URL,json=payload,timeout=30)
        response.raise_for_status()
        result=response.json()
        llm_reply=result["message"]["content"]
        return llm_reply
    except Exception as e:
        return f"出错误啦 >.<"
    
if __name__=="__main__":
    test_username="老板"
    test_user_input="我今天完成了一个代码的练习"
    reply=chat_with_local_llm(test_user_input,test_username)
    print(f"【识别到：{test_username}】")
    print(f"小黄人：{reply}")