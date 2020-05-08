from __future__ import print_function
import os
import glob
import sys
from multiprocessing import Pool, current_process
import multiprocessing as mp
import argparse
import time
import numpy as np


def dump_frames(vid_path):
    import cv2

    video = cv2.VideoCapture(vid_path)
    vid_name = vid_path.split("/")[-1].split(".")[0]
    out_full_path = os.path.join(out_path, vid_name)

    fcount = int(video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    try:
        os.mkdir(out_full_path)
    except OSError:
        pass
    file_list = []
    for i in xrange(fcount):
        ret, frame = video.read()
        assert ret
        cv2.imwrite("{}/{:06d}.jpg".format(out_full_path, i), frame)
        access_path = "{}/{:06d}.jpg".format(vid_name, i)
        file_list.append(access_path)
    print("{} done".format(vid_name))
    sys.stdout.flush()
    return file_list


def run_optical_flow(gpu_id, out_path, flow_type, new_weight, new_hight):
    os.system(
        "export CUDA_VISIBLE_DEVICES=%d;denseflow_gpu ./tmp/video_list_%02d.txt -b=20 -a=%s -s=1 --nw=%d --nh=%d -v=0 -o=%s 1>./tmp/output_%02d.txt"
        % (gpu_id, gpu_id, flow_type, new_weight, new_hight, out_path, gpu_id)
    )
    return True


def run_rgb_frame(gpu_id, out_path, new_weight, new_hight):
    os.system(
        "export CUDA_VISIBLE_DEVICES=%d && denseflow_gpu ./tmp/video_list_%02d.txt -s=0 --nw=%d --nh=%d -v=0 -o=%s 1>./tmp/output_%02d.txt"
        % (gpu_id % 4, gpu_id, new_weight, new_hight, out_path, gpu_id)
    )
    return True


def check_status(out_path, total_num, true_num, start_time):
    done_dir = os.path.join(out_path, ".done")
    if not os.path.exists(done_dir):
        os.makedirs(done_dir)
    while True:
        dir_list = os.listdir(done_dir)
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(done_dir, x)), reverse=True)

        current_time = time.time()
        processed_time = time.strftime("%H:%M:%S", time.gmtime(current_time - start_time))
        eta_time = (
            (current_time - start_time) / (len(dir_list) - total_num + true_num + 0.001) * (total_num - len(dir_list))
        )
        eta_time = time.strftime("%H:%M:%S", time.gmtime(eta_time))
        if len(dir_list) == 0:
            recent = "None"
        else:
            recent = dir_list[0]
        print(
            "\rProcessed %5d/%5d  |||  Recently finished %s  ||| Processed Time: %s  ||| ETA: %s"
            % (len(dir_list), total_num, recent, processed_time, eta_time),
            end="",
            flush=True,
        )
        time.sleep(60)  # check each 1 mins


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="extract optical flows with multi GPUs")
    parser.add_argument("src_dir")
    parser.add_argument("out_dir")
    parser.add_argument("--flow_type", type=str, default="tvl1", choices=["tvl1", "nv", "farn", "brox"])
    parser.add_argument(
        "--ext", type=str, default="mp4", choices=["avi", "mp4", "mkv", "webm"], help="video file extensions"
    )
    parser.add_argument("--new_width", type=int, default=224, help="resize image width")
    parser.add_argument("--new_height", type=int, default=224, help="resize image height")
    parser.add_argument("--num_gpu", type=int, default=4, help="number of GPU")

    args = parser.parse_args()
    out_path = args.out_dir
    src_path = args.src_dir
    flow_type = args.flow_type
    ext = args.ext
    new_weight = args.new_width
    new_hight = args.new_height
    NUM_GPU = args.num_gpu

    if not os.path.isdir(out_path):
        print("creating folder: " + out_path)
        os.makedirs(out_path)
    # print("reading videos from folder: ", src_path)

    print("selected extension of videos: mp4, mkv, webm")
    vid_list = glob.glob(src_path + "/*.mp4")
    vid_list.extend(glob.glob(src_path + "/*/*.mp4"))
    vid_list.extend(glob.glob(src_path + "/*.mkv"))
    vid_list.extend(glob.glob(src_path + "/*/*.mkv"))
    vid_list.extend(glob.glob(src_path + "/*.webm"))
    vid_list.extend(glob.glob(src_path + "/*/*.webm"))
    vid_list.sort()
    print("total number of videos found: ", len(vid_list))

    vid_done_list = []
    if os.path.exists(os.path.join(out_path, ".done")):
        vid_done_list = os.listdir(os.path.join(out_path, ".done"))

    new_vid_list = []
    for i in range(len(vid_list)):
        video_name = vid_list[i].split(".")[-2].split("/")[-1]
        if video_name in vid_done_list:
            continue
        else:
            new_vid_list.append(vid_list[i])
    print("the number of unprocessed videos: ", len(new_vid_list))

    sub_vid_list = [[] for i in range(NUM_GPU)]
    for i in range(len(new_vid_list)):
        sub_vid_list[i % NUM_GPU].append(new_vid_list[i])

    if not os.path.exists("./tmp/"):
        os.mkdir("./tmp/")
    print("\ncreating subset video list")
    for i in range(NUM_GPU):
        with open("./tmp/video_list_%02d.txt" % i, "w", encoding="utf-8") as file:
            for j in range(len(sub_vid_list[i])):
                file.write(sub_vid_list[i][j] + "\n")
        print("./tmp/video_list_%02d.txt has %6d videos" % (i, len(sub_vid_list[i])))
    print("")

    start_time = time.time()
    processes = []
    for i in range(NUM_GPU):
        if flow_type == "rgb":
            p = mp.Process(target=run_rgb_frame, args=(i, out_path, new_weight, new_hight))
        else:
            p = mp.Process(target=run_optical_flow, args=(i, out_path, flow_type, new_weight, new_hight))
        p.start()
        processes.append(p)

    p = mp.Process(target=check_status, args=([out_path, len(vid_list), len(new_vid_list), start_time]))
    p.start()
    p.deamon = True

    for p in processes:
        p.join()

    print("\nFinished!")
