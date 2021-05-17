# Denseflow

Extracting dense flow field given a video.

### Features

- support multiple optical flow algorithms
- support single video (or a frame folder) / a list of videos (or a list of frame folders) as input
- support multiple output types (image, hdf5)
- faster, 40% faster (by parallelize IO & computation)
- record the progress when extract a list of videos (Note: restart from the recent "done video",
  that is, the recent "approximately done video" may not actually done)
- 105 fps in RTX2080Ti


### Install

#### Dependencies:

- OpenCV:
[opencv3](https://www.learnopencv.com/install-opencv3-on-ubuntu/) ([Install Guide](tools/opencv_install.md))|
[opencv4](https://www.learnopencv.com/install-opencv-4-on-ubuntu-16-04/)
- CUDA (driver version > 400)
- Boost
- HDF5 (Optional)

```bash
git clone https://github.com/sming256/denseflow
cd denseflow
mkdir build && cd build
cmake ..
make -j
sudo make install
```

### Usage
```bash
$ denseflow_gpu -h
GPU optical flow extraction.
Usage: denseflow_gpu [params] input
        -a, --algorithm (value:tvl1)
                optical flow algorithm (nv/tvl1/farn/brox)
        -b, --bound (value:32)
                maximum of optical flow
        --cf, --classFolder
                outputDir/class/video/flow.jpg
        -d, --deviceId (value:0)  # may have bug in CUDA10
                set gpu id
        -h, --help (value:true)
                print help message
        --if, --inputFrames
                inputs are frames
        --newHeight, --nh (value:0)
                new height
        --newShort, --ns (value:0)
                short side length
        --newWidth, --nw (value:0)
                new width
        -o, --outputDir (value:.)
                root dir of output
        -s, --step (value:1)
                right - left (0 for img, non-0 for flow)
        -v, --verbose (value:0)
                verbose
        input
                filename of video or folder of frames or a list.txt of those
```
#### Extract optical flow of a single video

```bash
denseflow_gpu test.avi -b=20 -a=tvl1 -s=1 -v=1
```

- `test.avi`: input video
- `tmp`: folder containing RGB images and optical flow images
- `tvl1`: optical flow algorithm
- `v`: verbose
- `s`: step, extract frames only when step=0

#### Extract optical flow of a list of videos with single GPU

```bash
denseflow_gpu videolist.txt  -b=20 -a=tvl1 -s=1 --nw=224 --nh=224 -v=0 --outputDir=./flow/
```

- `videolist.txt`: input videolist.txt
- `outputDir`: output generated images to folder.

Better to check: resize / class folder / input image

#### Extract optical flow of video folder with multiple GPUs
```bash
cd ./tools
sh extract.sh
```
- `SRC_FOLDER`: folder of video source folder
- `OUT_FOLDER`: flow saving path
- `NUM_GPU`: number of used GPU, which means each GPU runs a subprocess

### Credits

Modified based on [yuanjun's fork of dense_flow](https://github.com/yjxiong/dense_flow).

#### Main Authors:

Shiguang Wang, Zhizhong Li

#### Modified:

Shuming Liu
