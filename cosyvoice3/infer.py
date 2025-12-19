import sys
sys.path.append('./third_party/Matcha-TTS')
from cosyvoice.cli.cosyvoice import CosyVoice, CosyVoice2,CosyVoice3,AutoModel
from cosyvoice.utils.file_utils import load_wav
import torchaudio
import os

# cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B', load_jit=False, load_trt=False, load_vllm=False, fp16=False)

# cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B-spanish', load_jit=False, load_trt=False, load_vllm=False, fp16=False)

# cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B-multi', load_jit=False, load_trt=False, load_vllm=False, fp16=False)

# cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B-multi-update-1', load_jit=False, load_trt=False, load_vllm=False, fp16=False)


# NOTE if you want to reproduce the results on https://funaudiollm.github.io/cosyvoice2, please add text_frontend=False during inference
# zero_shot usage
# prompt_speech_16k = load_wav('train_multi_language/out-wavs/arabic_day1121_prompt02.wav', 16000)
# for i, j in enumerate(cosyvoice.inference_zero_shot("الفئة الثانية من المقاعد بدركسون إم بعدادها الديجيتال والفل.","بطاقة جمركية لم تستخدم في السعودية بلونها الأسود المثالي.", prompt_speech_16k, stream=False,text_frontend=False)):
#     # print(j)
#     torchaudio.save(f"train_multi_language/out-wavs/ara_ara-2.wav", j['tts_speech'], cosyvoice.sample_rate)

## 批量推理多语种的文本
# with open("test_multi.txt", 'r', encoding='utf-8') as f:
#     lines = [i.strip() for i in f.readlines()]
# for line in lines:
#     print(line)
    
#     parts = line.split('|', 4)
#     if 'ara_ara' in line:
#         # continue
#         print(parts)
#     wav_path, gen_wav_path, content, gen_text = parts[0], parts[1], parts[2], parts[3]
#     ##泰语要变一下目录
#     gen_wav_path = gen_wav_path.replace('train_multi_language','train_thai_language')
#     out_dir = os.path.dirname(gen_wav_path)
#     if not os.path.exists(out_dir):
#         os.makedirs(out_dir)
#     if os.path.exists(gen_wav_path):
#         continue
#     prompt_speech_16k = load_wav(wav_path, 16000)
#     for i, j in enumerate(cosyvoice.inference_zero_shot(gen_text, content, prompt_speech_16k, stream=False,text_frontend=False)):

#         torchaudio.save(gen_wav_path, j['tts_speech'], cosyvoice.sample_rate)

# # save zero_shot spk for future usage
# assert cosyvoice.add_zero_shot_spk('希望你以后能够做的比我还好呦。', prompt_speech_16k, 'my_zero_shot_spk') is True
# for i, j in enumerate(cosyvoice.inference_zero_shot('收到好友从远方寄来的生日礼物，那份意外的惊喜与深深的祝福让我心中充满了甜蜜的快乐，笑容如花儿般绽放。', '', '', zero_shot_spk_id='my_zero_shot_spk', stream=False)):
#     torchaudio.save('zero_shot_{}.wav'.format(i), j['tts_speech'], cosyvoice.sample_rate)
# cosyvoice.save_spkinfo()

# # fine grained control, for supported control, check cosyvoice/tokenizer/tokenizer.py#L248
# for i, j in enumerate(cosyvoice.inference_cross_lingual('在他讲述那个荒诞故事的过程中，他突然[laughter]停下来，因为他自己也被逗笑了[laughter]。', prompt_speech_16k, stream=False)):
#     torchaudio.save('fine_grained_control_{}.wav'.format(i), j['tts_speech'], cosyvoice.sample_rate)

# # instruct usage
# for i, j in enumerate(cosyvoice.inference_instruct2('收到好友从远方寄来的生日礼物，那份意外的惊喜与深深的祝福让我心中充满了甜蜜的快乐，笑容如花儿般绽放。', '用四川话说这句话', prompt_speech_16k, stream=False)):
#     torchaudio.save('instruct_{}.wav'.format(i), j['tts_speech'], cosyvoice.sample_rate)

# bistream usage, you can use generator as input, this is useful when using text llm model as input
# NOTE you should still have some basic sentence split logic because llm can not handle arbitrary sentence length
# def text_generator():
#     yield '收到好友从远方寄来的生日礼物，'
#     yield '那份意外的惊喜与深深的祝福'
#     yield '让我心中充满了甜蜜的快乐，'
#     yield '笑容如花儿般绽放。'
# for i, j in enumerate(cosyvoice.inference_zero_shot(text_generator(), '希望你以后能够做的比我还好呦。', prompt_speech_16k, stream=False)):
#     torchaudio.save('zero_shot_{}.wav'.format(i), j['tts_speech'], cosyvoice.sample_rate)




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
