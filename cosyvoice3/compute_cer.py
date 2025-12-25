import jiwer
import sys,os
import whisper
from tqdm import tqdm
import shutil
model = whisper.load_model(name="large-v3")


with open("test_multi.txt", 'r', encoding='utf-8') as f:
    lines = [i.strip() for i in f.readlines()]
for line in tqdm(lines):
    # print(line)
    parts = line.split('|', 5)
    # if 'ara_ara' in line:
    #     continue
    wav_path, gen_wav_path, content, gen_text, qwen_txt = parts[0], parts[1], parts[2], parts[3], parts[4]
    ##泰语要变一下目录
    # gen_wav_path = gen_wav_path.replace('train_multi_language','train_thai_language')
    audio = whisper.load_audio(gen_wav_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    ref = gen_text.replace(' ', '').replace(',', '').replace('，', '').replace('?', '').replace('!', '')
    hyp_whisper = result.text.replace(' ', '').replace(',', '').replace('，', '').replace('?', '').replace('!', '')
    hyp_qwen = qwen_txt.replace(' ', '').replace(',', '').replace('，', '').replace('?', '').replace('!', '')
    cer_whisper = jiwer.cer(ref, hyp_whisper)
    cer_qwen = jiwer.cer(ref, hyp_qwen)
    print(f"ori_wav {gen_wav_path}, gen_text, {ref}, whisper_text, {hyp_whisper}, qwen_text, {hyp_qwen}, CER whisper = {cer_whisper:.2%}, CER qwen = {cer_qwen:.2%}")
    print(f"ori_wav {gen_wav_path}, gen_text, {gen_text}, whisper_text, {result.text}, qwen_text, {qwen_txt}, CER whisper = {cer_whisper:.2%}, CER qwen = {cer_qwen:.2%}")