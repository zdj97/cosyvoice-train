import sys
sys.path.append('./third_party/Matcha-TTS')
from cosyvoice.cli.cosyvoice import CosyVoice, CosyVoice2,CosyVoice3,AutoModel
from cosyvoice.utils.file_utils import load_wav
import torchaudio
import os


cosyvoice = AutoModel(model_dir='pretrained_models/Fun-CosyVoice3-0.5B')

for i, j in enumerate(cosyvoice.inference_zero_shot('测试音频', '希望你以后能够做的比我还好呦',
                                                    'zero_shot_prompt.wav', stream=False)):
    print(j['tts_speech'].shape)
    torchaudio.save('cosyvoice3.wav', j['tts_speech'], cosyvoice.sample_rate)



## 批量推理多语种的文本
with open("test_multi.txt", 'r', encoding='utf-8') as f:
    lines = [i.strip() for i in f.readlines()]
for line in lines:
    print(line)
    
    parts = line.split('|', 5)
    # if 'ara_ara' in line:
        # continue
        # print(parts)
    wav_path, gen_wav_path, content, gen_text, qwen_txt = parts[0], parts[1], parts[2], parts[3], parts[4]
    if not os.path.exists(wav_path):
        continue
    ##泰语要变一下目录
    # gen_wav_path = gen_wav_path.replace('train_multi_language','train_thai_language')
    out_dir = os.path.dirname(gen_wav_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # if os.path.exists(gen_wav_path):
    #     continue
    for i, j in enumerate(cosyvoice.inference_zero_shot(gen_text, content,
                                                        wav_path, stream=False, text_frontend=False)):
        # print(j['tts_speech'].shape)
        torchaudio.save(gen_wav_path, j['tts_speech'], cosyvoice.sample_rate)
