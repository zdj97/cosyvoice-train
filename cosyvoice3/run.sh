#!/bin/bash
# Copyright 2024 Alibaba Inc. All Rights Reserved.
. ./path.sh || exit 1;

stage=1
stop_stage=6

data_url=www.openslr.org/resources/60
data_dir=/mnt/lyuxiang.lx/data/tts/openslr/libritts
pretrained_model_dir=./pretrained_models/Fun-CosyVoice3-0.5B


if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
  tools/extract_embedding.py --dir data_multi/ \
    --onnx_path $pretrained_model_dir/campplus.onnx
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
  tools/extract_speech_token.py --dir data_multi/ \
    --onnx_path $pretrained_model_dir/speech_tokenizer_v3.onnx
fi

if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
  mkdir -p data_multi/parquet
  tools/make_parquet_list.py --num_utts_per_parquet 1000 \
    --num_processes 10 \
    --src_dir data_multi \
    --des_dir data_multi/parquet
fi

# train llm
export CUDA_VISIBLE_DEVICES="0,1,2,3"
num_gpus=$(echo $CUDA_VISIBLE_DEVICES | awk -F "," '{print NF}')
job_id=1986
dist_backend="nccl"
num_workers=4
prefetch=100
train_engine=torch_ddp
if [ ${stage} -le 5 ] && [ ${stop_stage} -ge 5 ]; then
  echo "Run train. We only support llm traning for now"
  if [ $train_engine == 'deepspeed' ]; then
    echo "Notice deepspeed has its own optimizer config. Modify conf/ds_stage2.json if necessary"
  fi
  cat data_multi/parquet/data.list > data_multi/train.data.list
  shuf -n 2 data_multi/train.data.list > data_multi/dev.data.list
  # NOTE will update llm/hift training later
  for model in llm flow; do
  # for model in flow; do
    torchrun --nnodes=1 --nproc_per_node=$num_gpus \
        --rdzv_id=$job_id --rdzv_backend="c10d" --rdzv_endpoint="localhost:1234" \
      cosyvoice/bin/train.py \
      --train_engine $train_engine \
      --config conf/cosyvoice3.yaml \
      --train_data data_multi/train.data.list \
      --cv_data data_multi/dev.data.list \
      --qwen_pretrain_path $pretrained_model_dir/CosyVoice-BlankEN \
      --model $model \
      --checkpoint $pretrained_model_dir/$model.pt \
      --model_path $pretrained_model_dir \
      --model_dir `pwd`/data_multi/cosyvoice3/$model/$train_engine \
      --tensorboard_dir `pwd`/data_multi/tensorboard/cosyvoice3/$model/$train_engine \
      --ddp.dist_backend $dist_backend \
      --num_workers ${num_workers} \
      --prefetch ${prefetch} \
      --pin_memory \
      --use_amp \
      --deepspeed_config ./conf/ds_stage2.json \
      --deepspeed.save_states model+optimizer
  done
fi

# average model
average_num=5
if [ ${stage} -le 6 ] && [ ${stop_stage} -ge 6 ]; then
  for model in llm flow; do
    decode_checkpoint=`pwd`/data_multi/cosyvoice3/$model/$train_engine/${model}.pt
    echo "do model average and final checkpoint is $decode_checkpoint"
    python cosyvoice/bin/average_model.py \
      --dst_model $decode_checkpoint \
      --src_path `pwd`/data_multi/cosyvoice3/$model/$train_engine  \
      --num ${average_num} \
      --val_best
  done
fi

if [ ${stage} -le 7 ] && [ ${stop_stage} -ge 7 ]; then
  echo "Export your model for inference speedup. Remember copy your llm or flow model to model_dir"
  python cosyvoice/bin/export_jit.py --model_dir $pretrained_model_dir
  python cosyvoice/bin/export_onnx.py --model_dir $pretrained_model_dir
fi