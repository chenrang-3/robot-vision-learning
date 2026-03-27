import requests
import whisper
import edge_tts
import asyncio
import pyaudio
import wave
import threading
import soundfile as sf
import sounddevice as sd

OLLAMA_API_URL="http://localhost:11434/api/chat"
LLM_MODEL_NAME="qwen2:7b-instruct"
CURRENT_USER="老板"

# ASR语音转文字配置
ASR_MODEL=whisper.load_model("base")
# TTS文字转语音配置
TTS_VOICE="zh-CN-XiaoxiaoNeural"
TTS_RATE="+0%"

# 录音参数
CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=16000

def record_audio(output_file="user_voice.wav"):
    p=pyaudio.PyAudio()
    stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    frames=[]
    input("\n 按回车开始说话，说完再按回车结束录音")
    print("正在录音")

    recording=True
    def wait_for_stop():
        nonlocal recording
        input()
        recording=False
    stop_thread=threading.Thread(target=wait_for_stop)
    stop_thread.start()


    while recording:
        data=stream.read(CHUNK)
        frames.append(data)

    # 结束录音+释放资源
    print("录音结束，正在处理")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf=wave.open(output_file,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def speech_to_text(audio_file="user_voice.wav"):
    # 修复3：拼写错误 langague → language
    result=ASR_MODEL.transcribe(audio_file,language="zh")
    text=result["text"].strip()
    print(f"你说的话：{text}")
    return text

def chat_with_minion(user_message,username):
    headers={"Content-Type":"application/json"}
    payload={
        "model":LLM_MODEL_NAME,
        "messages":[
            {"role":"system",
            "content":f"你是专属{username}的可爱小黄人聊天机器人，语气软萌、暖心、简短，主打情绪价值，会安慰、陪伴、逗开心，说话不要太长，用口语话的中文。"
            },
            {"role":"user","content":user_message}
        ],
        "stream":False
    }
    try:
        resp=requests.post(OLLAMA_API_URL,json=payload,headers=headers,timeout=30)
        resp.raise_for_status()
        result=resp.json()
        reply=result["message"]["content"].strip()
        print(f"小黄人：{reply}")
        return reply
    except Exception as e:
        error_msg=f"出错了>_< 错误原因：{str(e)}"
        print(error_msg)
        return error_msg

async def text_to_speech(text,output_file="minion_reply.wav"):
    tts=edge_tts.Communicate(text,TTS_VOICE,rate=TTS_RATE)
    await tts.save(output_file)
    data,fs=sf.read(output_file)
    sd.play(data,fs)
    sd.wait()

if __name__=="__main__":
    print("="*60)
    print("小黄人语音聊天机器人已启动！")
    print(f"当前识别用户：{CURRENT_USER}")
    print("语音说【退出/停止】即可结束对话")
    print("="*60)

    while True:
        # 录音
        record_audio()
        user_text=speech_to_text()

        if user_text in ["退出","停止","结束"]:
            goodbye_text="好的老板，我先休息啦，下次再见~"
            print(f"小黄人：{goodbye_text}")
            asyncio.run(text_to_speech(goodbye_text))
            break

        if not user_text:
            asyncio.run(text_to_speech("我没听清哦，再说一遍吧"))
            continue

        reply = chat_with_minion(user_text, CURRENT_USER)
        asyncio.run(text_to_speech(reply))