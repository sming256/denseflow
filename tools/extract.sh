# multi gpu
# echo "Environment PATH: $PATH\n"

SRC_FOLDER="/data/video/"
OUT_FOLDER="/data/flow/"
NUM_GPU="4"

echo "Extracting optical flow from videos in folder:   ${SRC_FOLDER}"
echo "Saving path:   ${OUT_FOLDER}"
echo "NOTICE: Using $NUM_GPU GPUs\n"
python multi_gpu_extract.py ${SRC_FOLDER} ${OUT_FOLDER} --num_gpu=${NUM_GPU} --new_width=224 --new_height=224
# python multi_gpu_extract.py ${SRC_FOLDER} ${OUT_FOLDER} --num_gpu=${NUM_GPU} --new_width=224 --new_height=224 --flow_type=rgb