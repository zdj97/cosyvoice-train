import torchaudio
import os

def calculate_total_duration(txt_file_path):
    """
    计算txt文件中所有音频文件的总时长
    
    Args:
        txt_file_path (str): 包含wav路径和文本的txt文件路径
    """
    total_duration = 0.0
    processed_files = 0
    missing_files = []
    error_files = []
    
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"找到 {len(lines)} 行数据，开始处理...")
        
        for i, line in enumerate(lines, 1):
            # 清理行内容并分割
            line = line.strip()
            if not line or '|' not in line:
                continue
                
            wav_path = line.split('|')[1].strip()
            
            # 检查文件是否存在
            if not os.path.exists(wav_path):
                missing_files.append(wav_path)
                continue
            
            try:
                # 使用torchaudio.info高效获取元数据，不加载完整音频
                metadata = torchaudio.info(wav_path)
                duration = metadata.num_frames / metadata.sample_rate
                total_duration += duration
                processed_files += 1
                
                # 每处理100个文件显示一次进度
                if i % 100 == 0:
                    print(f"已处理 {i}/{len(lines)} 个文件...")
                    
            except Exception as e:
                error_files.append((wav_path, str(e)))
                continue
        
        # 输出结果
        print("\n" + "="*50)
        print("处理完成！")
        print(f"成功处理文件数: {processed_files}")
        print(f"总音频时长: {total_duration:.2f} 秒")
        print(f"约合 {total_duration/60:.2f} 分钟")
        print(f"约合 {total_duration/3600:.2f} 小时")
        
        if missing_files:
            print(f"\n警告: 以下 {len(missing_files)} 个文件不存在:")
            for f in missing_files[:5]:  # 只显示前5个
                print(f"  - {f}")
            if len(missing_files) > 5:
                print(f"  ... 以及 {len(missing_files)-5} 个其他文件")
                
        if error_files:
            print(f"\n警告: 以下 {len(error_files)} 个文件处理出错:")
            for f, err in error_files[:3]:  # 只显示前3个
                print(f"  - {f}: {err}")
            if len(error_files) > 3:
                print(f"  ... 以及 {len(error_files)-3} 个其他错误")
                
    except FileNotFoundError:
        print(f"错误: 找不到文件 {txt_file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

# 使用示例
if __name__ == "__main__":
    # 替换为你的txt文件路径
    # txt_file = 'train_multi_language/thai.csv'  # 修改为实际文件路径
    txt_file = 'train_multi_language/spanish-zdj.csv'
    calculate_total_duration(txt_file)


# with open('spanish_5w.txt', 'r', encoding='utf-8') as f:
#     lines = [i.strip() for i in f.readlines()]
# wav_scp_data = []
# for line in lines:  
#     wav_path, content = line.split('\t', 2)
#     spk = wav_path.split('/')[-1].split('-')[0]
#     wav_scp_data.append(f"{spk}|{wav_path}|{content}\n")
# with open('train_multi_language/spanish-zdj.csv', 'w', encoding='utf-8') as f:
#     f.writelines(wav_scp_data)
    
# with open('thai_train_5w.tsv', 'r', encoding='utf-8') as f:
#     lines = [i.strip() for i in f.readlines()]
# wav_scp_data = []
# for line in lines:  
#     audio_id, text_content = line.split('\t', 2)
#     if '-' in audio_id:
#         speaker_id = audio_id.split('-')[0]
#     else:
#     # 如果没有下划线，使用前几位作为说话人ID
#         speaker_id = audio_id[:6]  # 根据实际情况调整

#     tmp1,tmp2,tmp3=audio_id.split('-')

#     audio_path = f"/sharedir/nlp/workspace/yuqiangz_living_data/models/gigaspeech2/data/th/train/{tmp1}/{tmp2}/{audio_id}.wav"

#     wav_scp_data.append(f"{speaker_id}|{audio_path}|{text_content}\n")
# with open('train_multi_language/thai.csv', 'w', encoding='utf-8') as f:
#     f.writelines(wav_scp_data)