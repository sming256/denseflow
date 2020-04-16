# OpenCV3.4 + Ubuntu + CUDA10
1. Prerequisite：
```bash
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper
```

2. Download file:
```bash
wget https://github.com/opencv/opencv/archive/3.4.4.zip
wget https://codeload.github.com/opencv/opencv_contrib/zip/3.4.4
unzip 3.4.4.zip
unzip 3.4.4
```

3. Compile cmake:
```bash
cd opencv-3.4.4
mkdir build && cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D WITH_TBB=ON \
      -D WITH_CUDA=ON \
      -D ENABLE_PRECOMPILED_HEADERS=OFF \
      -D BUILD_opencv_cudacodec=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.4/modules \
      -D PYTHON_DEFAULT_EXECUTABLE=~/anaconda3/bin/python3 \
      -D BUILD_opencv_python3=ON \
      -D BUILD_opencv_python2=OFF \
      -D PYTHON3_EXCUTABLE=~/anaconda3/bin/python3 \
      -DWITH_CUBLAS=1 ..
make -j   # if not work, use make only
sudo make install
```