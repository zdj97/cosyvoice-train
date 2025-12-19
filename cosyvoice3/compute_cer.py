import jiwer
import sys,os
import whisper
from tqdm import tqdm
import shutil
model = whisper.load_model(name="large-v3")

# def process_file_with_jiwer(file_path, output_dir):
#     """
#     使用jiwer库处理文件
#     """
#     references = []
#     hypotheses = []
#     wav_scp_data = []
#     with open(file_path, 'r', encoding='utf-8') as f:
#         lines = [i.strip() for i in f.readlines()]
#         # for line_num, line in enumerate(f, 1):
#     # print(lines)
#     for line in tqdm(lines[:100]):
#         line = line.strip()
#         if not line:
#             continue  
#         parts = line.split(' ', 4)
#         if len(parts) < 2:
#             continue
#         # print(parts)
#         spk_id, wav_path, content, tgt_path, gen_text = parts[0], parts[1], parts[2], parts[3], parts[4]
#         tgt_path_ori = tgt_path.replace('.wav','_ori.wav')
#         shutil.copy(wav_path, tgt_path_ori)
#         # print(spk_id, wav_path, content, type(tgt_path))
#         if not os.path.exists(tgt_path):
#             continue
#         audio = whisper.load_audio(tgt_path)
#         audio = whisper.pad_or_trim(audio)
#         mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
#         options = whisper.DecodingOptions()
#         result = whisper.decode(model, mel, options)
#         print(f"ori_wav {tgt_path_ori} trg_wav {tgt_path}, result, {result.text}, gen_text, {gen_text}")
#         wav_scp_data.append(f"{spk_id} {wav_path} {content} {tgt_path} {gen_text} {result.text}\n")
#         reference, hypothesis = gen_text, result.text
#         references.append(reference)
#         hypotheses.append(hypothesis)
#     print(len(wav_scp_data))
#     # 写入文件
#     with open(os.path.join(output_dir, 'wav-test-gen.scp'), 'w', encoding='utf-8') as f:
#         f.writelines(wav_scp_data)
 
#     # 计算每行的WER
#     for i, (ref, hyp) in enumerate(zip(references, hypotheses), 1):
#         ref = ref.replace(' ', '')
#         hyp = hyp.replace(' ', '')
#         wer = jiwer.wer(ref, hyp)
#         print(f"行号 {i}: WER = {wer:.2%}")
#     # 计算整体WER
#     overall_wer = jiwer.wer(references, hypotheses)
#     print(f"\n整体WER: {overall_wer:.2%}")

# def com_(output_dir):
#     references = []
#     hypotheses = []    
#     with open(os.path.join(output_dir, 'wav-test-gen.scp'), 'r', encoding='utf-8') as f:
#         lines = [i.strip() for i in f.readlines()]
#     for line in tqdm(lines):
#         parts = line.split(' ', 5)
#         if len(parts) < 6:
#             continue
#         spk_id, wav_path, content, tgt_path, gen_text, result_text = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
#         ref = gen_text.replace(' ', '')
#         hyp = result_text.replace(' ', '')
#         wer = jiwer.cer(ref, hyp)
#         references.append(ref)
#         hypotheses.append(hyp)
#         print(f"ori_wav {wav_path} trg_wav {tgt_path}, gen_text, {gen_text}, result_text, {result_text}, WER = {wer:.2%}")
#     overall_wer = jiwer.cer(references, hypotheses)
#     print(f"\n整体WER: {overall_wer:.2%}")       

# # 使用
# # process_file_with_jiwer("thai_data/wav-test.scp",output_dir="thai_data")
# com_(output_dir="thai_data")


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