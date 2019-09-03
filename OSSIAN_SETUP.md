### Setup Ossian
Install libraries
```shell script
sudo apt install libncurses5-dev
sudo apt-get install clang libsndfile1-dev gsl-bin libgsl0-dev libconfig-dev g++-4.8 g++-4.8
```

Clone and compile
```shell script
git clone https://github.com/CSTR-Edinburgh/Ossian.git
cd Ossian
./scripts/setup_tools.sh mirfan899 Tqveb=Be
```
### Directory Structure
```shell script
mkdir corpus
mkdir corpus/cn
mkdir corpus/cn/speakers
mkdir corpus/cn/speakers/toy_cn_corpus
mkdir corpus/cn/speakers/toy_cn_corpus/txt
mkdir corpus/cn/speakers/toy_cn_corpus/wav
```

### Python dependencies
```shell script
pip install numpy scipy regex argparse lxml scikit-learn regex configobj
```

### Dependencies for merlin
```shell script
pip install bandmat
pip install lxml
pip install matplotlib
```

### Install Python 3 packages.
```shell script
sudo apt-get install python3-dev python3-pip
```

### Python 3.7
```shell script
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
```

### Python 3.5.2
```shell script
curl -O https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
```

### Run training process in background
```shell script
nohup ./run_full_demo > output.log 2>&1 &
```

### GCC
```shell script
sudo add-apt-repository ppa:ubuntu-toolchain-r/ppa
sudo apt-get update
sudo apt-get install g++-4.8 g++-4.8
set gcc-4.8
sudo ln -s /usr/bin/gcc-4.8 /usr/local/cuda/bin/gcc -f
sudo ln -s /usr/bin/g++-4.8 /usr/local/cuda/bin/g++ -f
```

### Set gcc-6
```shell script
sudo ln -s /usr/bin/gcc-6 /usr/local/cuda/bin/gcc -f
sudo ln -s /usr/bin/g++-6 /usr/local/cuda/bin/g++ -f
```

### Get soft links
```shell script
ls -la /usr/bin/gcc
ln -s /usr/bin/gcc-4.8 /usr/bin/gcc
ln -s /usr/bin/g++-4.8 /usr/bin/g++
```

### Add and remove soft link to gcc, g++
https://askubuntu.com/questions/26498/how-to-choose-the-default-gcc-and-g-version
```shell script
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50
```

### connect to gcp SSH
```shell script
gcloud alpha cloud-shell ssh
```
