# Denseflow

Extracting dense flow field given a video.

### Features

- support multiple optical flow algorithms
- support single video (or a frame folder) / a list of videos (or a list of frame folders) as input
- support multiple output types (image, hdf5)
- faster, 40% faster (by parallelize IO & computation)
- record the progress when extract a list of videos (Note: restart from the recent "done video",
  that is, the recent "approximately done video" may not actually done)


### Install

#### Dependencies:

- OpenCV:
[opencv3](https://www.learnopencv.com/install-opencv3-on-ubuntu/) |
[opencv4](https://www.learnopencv.com/install-opencv-4-on-ubuntu-16-04/)
- CUDA (driver version > 400)
- Boost
- HDF5 (Optional)

```bash
git clone https://github.com/sming256/denseflow
mkdir build && cd build
cmake ..
make -j
sudo make install
```

### Usage

#### Extract optical flow of a single video

```bash
denseflow_gpu test.avi -b=20 -a=tvl1 -s=1 -v
```

- `test.avi`: input video / videolist.txt
- `tmp`: folder containing RGB images and optical flow images
- `dir`: output generated images to folder.
- `tvl1`: optical flow algorithm
- `v`: verbose
- `s`: step, extract frames only when step=0

#### Extract optical flow of a list of videos

* resize
* class folder
* input image

```bash
denseflow_gpu videolist.txt -b=20 -a=tvl1 -s=1 -v
```

- `videolist.txt`: input video / videolist.txt
- `tmp`: folder containing RGB images and optical flow images
- `dir`: output generated images to folder.
- `tvl1`: optical flow algorithm
- `v`: verbose
- `s`: step, extract frames only when step=0

### Credits

Modified based on [yuanjun's fork of dense_flow](https://github.com/yjxiong/dense_flow).

#### Main Authors:

Shiguang Wang, Zhizhong Li
