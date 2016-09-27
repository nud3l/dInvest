# Dinvest
Repository for distributed autonomous investment banking

## Trading
Tried out [Quantiacs](https://quantiacs.com/Blog/Intro-to-Algorithmic-Trading-with-Heikin-Ashi.aspx) and Quantopian/Zipline. [Zipline](https://github.com/quantopian/zipline) is developed by Quantopian. It gives a stand-alone version to trading based on Python.

## Setup
Install the required Zipline system packages with:
```
sudo apt-get install libatlas-base-dev python-dev gfortran pkg-config libfreetype6-dev
```

Setup virtualenv for Python, if your local Python version < 2.7.9. First install the required system packages.
```
sudo apt-get install -y \
autotools-dev      \
blt-dev            \
bzip2              \
dpkg-dev           \
g++-multilib       \
gcc-multilib       \
libbluetooth-dev   \
libbz2-dev         \
libexpat1-dev      \
libffi-dev         \
libffi6            \
libffi6-dbg        \
libgdbm-dev        \
libgpm2            \
libncursesw5-dev   \
libreadline-dev    \
libsqlite3-dev     \
libssl-dev         \
libtinfo-dev       \
mime-support       \
net-tools          \
netbase            \
python-crypto      \
python-mox3        \
python-pil         \
python-ply         \
quilt              \
tk-dev             \
zlib1g-dev
```
Get Python sources and compile it.
```
wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar xfz Python-2.7.11.tgz
cd Python-2.7.11/
./configure --prefix /usr/local/lib/python2.7.11 --enable-ipv6
make
sudo make install
```

Rough test if the installation worked.
```
/usr/local/lib/python2.7.11/bin/python -V
Python 2.7.11
```
Go into the the trading folder of the project and create the virtual environment.
```
cd  Dinvest/trading
virtualenv --python=/usr/local/lib/python2.7.11/bin/python venv
```

Activate the environment.
```
source venv/bin/activate
```

You can find tthis tutorial for Ubuntu/Mint [here](http://mbless.de/blog/2016/01/09/upgrade-to-python-2711-on-ubuntu-1404-lts.html).

Afterwards install Zipline via pip from your virtual environment.
```
pip install zipline
```
There is a full tutorial on the installation of Zipline also for other OS [here](http://www.zipline.io/install.html).



## TODO
- Value investment criteria
- Value investment algorithm implementation
- Smart contracts to integrate with python
