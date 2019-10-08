### Setup Ossian
Install required libraries for Ossian TTS
```shell script
sudo apt-get install libncurses5-dev
sudo apt-get install clang libsndfile1-dev gsl-bin libgsl0-dev libconfig-dev g++-4.8 g++-4.8
sudo apt-get install software-properties-common python-software-properties build-essential libc-dev python3-virtualenv python3-pip
sudo apt-get install sox curl libicu-dev python python-dev python-pip python-setuptools unzip wget
sudo apt-get install realpath
sudo apt-get install coreutils
sudo apt-get install autotools-dev
sudo apt-get install automake
sudo apt-get install ffmpeg
sudo apt-get update
```

Clone and compile the Ossian TTS with required Python 2.7.* libraries.
```shell script
git clone https://github.com/CSTR-Edinburgh/Ossian.git
cd Ossian
apt install python-virtualenv
virtualenv -p python2 .mytts
source ./mytts/bin/activate
pip install numpy scipy regex argparse lxml scikit-learn regex configobj python-virtualenv
./scripts/setup_tools.sh mirfan899 Tqveb=Be
```

### Directory Structure
Create directory structure for Chinese(Cantonese) TTS.
```shell script
mkdir corpus
mkdir corpus/cn
mkdir corpus/cn/speakers
mkdir corpus/cn/speakers/toy_cn_corpus
mkdir corpus/cn/speakers/toy_cn_corpus/txt
mkdir corpus/cn/speakers/toy_cn_corpus/wav
```

Convert the `.m4a` files to `.wav` files by using following command in `m4a` audio directory.
```shell script
## Convert m4a to wav files.
for entry in *.m4a
do
  filename=$(basename -- "$entry")
  filename="${filename%.*}"
  ffmpeg -i "${entry}" "${filename}.wav";
done

## Create temp directory for storing the converted file and then use it later.
## Convert wav files to 16khz 16 bit wav files
mkdir temp
temp_dir=temp
echo ${temp_dir}
for i in *.wav; do
  ffmpeg -i ${i} -acodec pcm_s16le -ac 1 -ar 16000 ${temp_dir}/${i};
done
```

copy `wav` files from `temp` directory to `corpus/cn/speakers/toy_cn_corpus/wav`.
```shell script
cp temp/*.wav Ossian/corpus/cn/speakers/toy_cn_corpus/wav
```

### Dependencies for merlin
```shell script
pip install bandmat
pip install lxml
pip install matplotlib
```

### Install Python 2.7.* packages.
```shell script
sudo apt-get install python-dev python-pip
```

### Run training process in background
```shell script
nohup ./run_full_demo > output.log 2>&1 &
```

### GCC and G++ <= 5.4.0
GCC and G++ should be 5.4.0 or lower.
```shell script
sudo add-apt-repository ppa:ubuntu-toolchain-r/ppa
sudo apt-get update
sudo apt-get install g++-4.8 g++-4.8
set gcc-4.8
sudo ln -s /usr/bin/gcc-4.8 /usr/local/cuda/bin/gcc -f
sudo ln -s /usr/bin/g++-4.8 /usr/local/cuda/bin/g++ -f
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
