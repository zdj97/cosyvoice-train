import csv
import os
import random
import torchaudio
def tsv_to_kaldi_files(tsv_path, output_dir, audio_base_path=""):
    """
    将TSV文件转换为Kaldi格式的wav.scp, text, utt2spk, spk2utt文件
    
    参数:
        tsv_path: TSV文件路径
        output_dir: 输出目录
        audio_base_path: 音频文件基础路径，默认为空
    """
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化数据存储
    wav_scp_data = []
    text_data = []
    utt2spk_data = []
    spk2utt_dict = {}
    out_list = []
    # 读取TSV文件[9,10](@ref)
    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        # print(len(list(reader)))
        for row_num, row in enumerate(reader):
            if len(row) < 2:
                print(f"警告: 第{row_num+1}行格式不正确，已跳过")
                continue
                
            # 提取ID和文本
            audio_id = row[0].strip()
            text_content = row[1].strip()
            
            # 假设说话人ID可以从音频ID中提取（根据实际情况调整）
            # 这里假设音频ID格式为"speaker001_utterance01"
            if '-' in audio_id:
                speaker_id = audio_id.split('-')[0]
            else:
                # 如果没有下划线，使用前几位作为说话人ID
                speaker_id = audio_id[:6]  # 根据实际情况调整
            
            # 构建音频文件路径（根据实际情况调整路径格式）
            # 假设音频文件扩展名为.wav，位于audio_base_path目录下
            tmp1,tmp2,tmp3=audio_id.split('-')
            
            audio_path = os.path.join(audio_base_path, f"{tmp1}/{tmp2}/{audio_id}.wav")
            
            # 添加到各数据列表
            wav_scp_data.append(f"{audio_id}\t{audio_path}\n")
            text_data.append(f"{audio_id}\t{text_content}\n")
            utt2spk_data.append(f"{audio_id}\t{speaker_id}\n")
            out_list.append(f"{speaker_id}|{audio_path}|{text_content}\n")
            # 更新spk2utt字典
            if speaker_id not in spk2utt_dict:
                spk2utt_dict[speaker_id] = []
            spk2utt_dict[speaker_id].append(audio_id)
    print(len(wav_scp_data))
    # 写入文件
    with open(os.path.join(output_dir, 'wav.scp'), 'w', encoding='utf-8') as f:
        f.writelines(wav_scp_data)
    
    with open(os.path.join(output_dir, 'text'), 'w', encoding='utf-8') as f:
        f.writelines(text_data)
    
    with open(os.path.join(output_dir, 'utt2spk'), 'w', encoding='utf-8') as f:
        f.writelines(utt2spk_data)
    
    with open(os.path.join(output_dir, 'thai_data.tsv'), 'w', encoding='utf-8') as f:
        f.writelines(out_list)   

    # 生成spk2utt文件[1](@ref)
    with open(os.path.join(output_dir, 'spk2utt'), 'w', encoding='utf-8') as f:
        for speaker_id, audio_ids in spk2utt_dict.items():
            f.write(f"{speaker_id}\t{' '.join(audio_ids)}\n")
    
    print(f"转换完成！共处理 {len(wav_scp_data)} 条数据")
    print(f"输出文件位于: {output_dir}")



def tsv_to_kaldi_files_spanish(tsv_path, output_dir, audio_base_path=""):
    """
    将TSV文件转换为Kaldi格式的wav.scp, text, utt2spk, spk2utt文件
    
    参数:
        tsv_path: TSV文件路径
        output_dir: 输出目录
        audio_base_path: 音频文件基础路径，默认为空
    """
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化数据存储
    wav_scp_data = []
    text_data = []
    utt2spk_data = []
    spk2utt_dict = {}
    out_list = []
    # 读取TSV文件[9,10](@ref)
    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        # print(len(list(reader)))
        for row_num, row in enumerate(reader):
            if len(row) < 2:
                print(f"警告: 第{row_num+1}行格式不正确，已跳过")
                continue
                
            # 提取ID和文本
            audio_path = row[0].strip()
            audio_id = audio_path.split('/')[-1]
            text_content = row[1].strip()
            
            # 假设说话人ID可以从音频ID中提取（根据实际情况调整）
            # 这里假设音频ID格式为"speaker001_utterance01"
            if '-' in audio_id:
                speaker_id = audio_id.split('-')[0]
            else:
                # 如果没有下划线，使用前几位作为说话人ID
                speaker_id = audio_id[:6]  # 根据实际情况调整
            
            # 构建音频文件路径（根据实际情况调整路径格式）
            # 假设音频文件扩展名为.wav，位于audio_base_path目录下
          
            # 添加到各数据列表
            wav_scp_data.append(f"{audio_id}\t{audio_path}\n")
            text_data.append(f"{audio_id}\t{text_content}\n")
            utt2spk_data.append(f"{audio_id}\t{speaker_id}\n")
            out_list.append(f"{speaker_id}|{audio_path}|{text_content}\n")
            # 更新spk2utt字典
            if speaker_id not in spk2utt_dict:
                spk2utt_dict[speaker_id] = []
            spk2utt_dict[speaker_id].append(audio_id)
    print(len(wav_scp_data))
    # 写入文件
    with open(os.path.join(output_dir, 'wav.scp'), 'w', encoding='utf-8') as f:
        f.writelines(wav_scp_data)
    
    with open(os.path.join(output_dir, 'text'), 'w', encoding='utf-8') as f:
        f.writelines(text_data)
    
    with open(os.path.join(output_dir, 'utt2spk'), 'w', encoding='utf-8') as f:
        f.writelines(utt2spk_data)
    
    # 生成spk2utt文件[1](@ref)
    with open(os.path.join(output_dir, 'spk2utt'), 'w', encoding='utf-8') as f:
        for speaker_id, audio_ids in spk2utt_dict.items():
            f.write(f"{speaker_id}\t{' '.join(audio_ids)}\n")
    
    with open(os.path.join(output_dir, 'spanish_5w.tsv'), 'w', encoding='utf-8') as f:
        f.writelines(out_list)   

    print(f"转换完成！共处理 {len(wav_scp_data)} 条数据")
    print(f"输出文件位于: {output_dir}")


def process_multi_speaker_data(output_dir, audio_base_path="", path1=''):
    """
    将TSV文件转换为Kaldi格式的wav.scp, text, utt2spk, spk2utt文件
    
    参数:
        tsv_path: TSV文件路径
        output_dir: 输出目录
        audio_base_path: 音频文件基础路径，默认为空
    """
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化数据存储
    wav_scp_data = []
    text_data = []
    utt2spk_data = []
    spk2utt_dict = {}
    out_list = []
    ## 处理泰语数据，需要加上绝对路径
    with open("thai_5w.tsv", 'r', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        # print(len(list(reader)))
        for row_num, row in enumerate(reader):
            if len(row) < 2:
                print(f"警告: 第{row_num+1}行格式不正确，已跳过")
                continue
                
            # 提取ID和文本
            audio_id = row[0].strip()
            text_content = row[1].strip()
            
            # 假设说话人ID可以从音频ID中提取（根据实际情况调整）
            # 这里假设音频ID格式为"speaker001_utterance01"
            if '-' in audio_id:
                speaker_id = audio_id.split('-')[0]
            else:
                # 如果没有下划线，使用前几位作为说话人ID
                speaker_id = audio_id[:6]  # 根据实际情况调整
            
            # 构建音频文件路径（根据实际情况调整路径格式）
            # 假设音频文件扩展名为.wav，位于audio_base_path目录下
            tmp1,tmp2,tmp3=audio_id.split('-')
            
            audio_path = os.path.join(audio_base_path, f"{tmp1}/{tmp2}/{audio_id}.wav")
            
            # 添加到各数据列表
            wav_scp_data.append(f"{audio_id}\t{audio_path}\n")
            text_data.append(f"{audio_id}\t{text_content}\n")
            utt2spk_data.append(f"{audio_id}\t{speaker_id}\n")
            out_list.append(f"{speaker_id}|{audio_path}|{text_content}")
            # 更新spk2utt字典
            if speaker_id not in spk2utt_dict:
                spk2utt_dict[speaker_id] = []
            spk2utt_dict[speaker_id].append(audio_id)
    
    ## 西班牙语处理
    with open('spanish_5w.txt', 'r', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        # print(len(list(reader)))
        for row_num, row in enumerate(reader):
            if len(row) < 2:
                print(f"警告: 第{row_num+1}行格式不正确，已跳过")
                continue
                
            # 提取ID和文本
            audio_path = row[0].strip()
            audio_id = audio_path.split('/')[-1]
            text_content = row[1].strip()
            
            # 假设说话人ID可以从音频ID中提取（根据实际情况调整）
            # 这里假设音频ID格式为"speaker001_utterance01"
            if '-' in audio_id:
                speaker_id = audio_id.split('-')[0]
            else:
                # 如果没有下划线，使用前几位作为说话人ID
                speaker_id = audio_id[:6]  # 根据实际情况调整
            
            # 构建音频文件路径（根据实际情况调整路径格式）
            # 假设音频文件扩展名为.wav，位于audio_base_path目录下
          
            # 添加到各数据列表
            wav_scp_data.append(f"{audio_id}\t{audio_path}\n")
            text_data.append(f"{audio_id}\t{text_content}\n")
            utt2spk_data.append(f"{audio_id}\t{speaker_id}\n")
            
            # 更新spk2utt字典
            if speaker_id not in spk2utt_dict:
                spk2utt_dict[speaker_id] = []
            spk2utt_dict[speaker_id].append(audio_id)

    for root, dirs, files in os.walk(path1):
        # 获取当前目录的说话人ID（假设目录名为说话人ID）
        # print(root, dirs, files)
        # spk_id = os.path.basename(dirs)
        # print(f"Processing speaker: {spk_id}")
        for spk_id in dirs:
        # 遍历当前目录下的所有文件
            print(f"Processing speaker: {spk_id}")
            speaker_dir = os.path.join(root, spk_id)
            for file in os.listdir(speaker_dir):
                if file.endswith('.wav'):
                    audio_id = file[:-4]  # 去掉.wav后缀作为音频ID
                    text_file = os.path.join(speaker_dir, audio_id + '.txt')
                    if not os.path.exists(text_file):
                        print(f"警告: 文本文件 {text_file} 不存在，已跳过")
                        continue
                    with open(text_file, 'r', encoding='utf-8') as tf:
                        text_content = tf.readline().strip()
                    
                    audio_path = os.path.join(speaker_dir, file)
                    # try:
                    #     audio, sample_rate = torchaudio.load(audio_path)
                    # except:
                    #     print(f"警告: 音频文件 {audio_path} 无法加载，已跳过")
                    #     continue
                    # 添加到各数据列表
                    wav_scp_data.append(f"{audio_id}\t{audio_path}\n")
                    text_data.append(f"{audio_id}\t{text_content}\n")
                    utt2spk_data.append(f"{audio_id}\t{spk_id}\n")
                    
                    # 更新spk2utt字典
                    if spk_id not in spk2utt_dict:
                        spk2utt_dict[spk_id] = []
                    spk2utt_dict[spk_id].append(audio_id)     
    
    print(len(wav_scp_data))
    # 写入文件
    with open(os.path.join(output_dir, 'wav.scp'), 'w', encoding='utf-8') as f:
        f.writelines(wav_scp_data)
    
    with open(os.path.join(output_dir, 'text'), 'w', encoding='utf-8') as f:
        f.writelines(text_data)
    
    with open(os.path.join(output_dir, 'utt2spk'), 'w', encoding='utf-8') as f:
        f.writelines(utt2spk_data)
    
    # 生成spk2utt文件[1](@ref)
    with open(os.path.join(output_dir, 'spk2utt'), 'w', encoding='utf-8') as f:
        for speaker_id, audio_ids in spk2utt_dict.items():
            f.write(f"{speaker_id}\t{' '.join(audio_ids)}\n")
    
    print(f"转换完成！共处理 {len(wav_scp_data)} 条数据")
    print(f"输出文件位于: {output_dir}")


    
# 使用示例
if __name__ == "__main__":
    # 配置参数
    # tsv_file_path = "thai_train_5w.tsv"  # 每行格式：149-149997-21\tดังนั้นเอาไม่อยู่แล้วอ่างมันเอาไม่อยู่；路径示例：path1/149/149997/21/XXX.wav
    # output_directory = "thai_data"   # 输出目录
    # base_audio_path = path1  # 音频文件基础路径
    # os.makedirs(output_directory, exist_ok=True)
    # # 执行转换
    # tsv_to_kaldi_files(tsv_file_path, output_directory, base_audio_path)


    # tsv_file_path = "spanish_5w.txt"  ## 每行格式：XXX/XXX/c0a448c7-545a-42db-a497-6460e9845c66.wav\tpero todo e
    # output_directory = "spanish_data"   # 输出目录
    # base_audio_path = ""  # 音频文件基础路径
    # os.makedirs(output_directory, exist_ok=True)
    # 执行转换
    # tsv_to_kaldi_files_spanish(tsv_file_path, output_directory, base_audio_path)

    
    ## path1的格式：
    # path1/
    #     spk1/
    #         spk-1.wav
    #         spk-1.txt
    #         spk-2.wav
    #         spk-2.txt
    #     spk2/
    #         spk2-1.wav
    #         spk2-1.txt
    ## path2的格式同上边泰语格式
    # output_directory = "arabic_malay_portuguese_singlish_spanish_thai_data"   # 输出目录
    # base_audio_path = path2 # 音频文件基础路径
    # os.makedirs(output_directory, exist_ok=True)
    # # 执行转换
    # process_multi_speaker_data(output_directory, base_audio_path, path1)
