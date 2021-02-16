# shares

### ubuntu 下 python 安装talib 包
```shell
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz # 下载
tar -zxvf ta-lib-0.4.0-src.tar.gz  # 解压
cd ta-lib/
sudo ./configure --prefix=/usr
sudo make
sudo make install
ls /usr/lib
```
将编译好的文件复制到python 库目录下
我这里python3 库目录为：/usr/lib/python3/dist-packages ，具体以自己的为主
```shell
sudo ls /usr/lib
sudo cp /usr/lib/libta_lib*.* /usr/lib/python3/dist-packages/
 
# 如果是anaconda
 
sudo cp /usr/lib/libta_lib*.* /home/username/anaconda3/lib/

```

## pip安装
```bash
pip3 install sklearn ta-lib tushare numpy pandas tkinter

sudo apt-get install python3-tk
```