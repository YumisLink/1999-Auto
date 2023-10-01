# 1999-Auto

基于python和adb的1999自动化脚本

## 已实现功能
- [√]日常
   刷关 签到 荒原收菜 邮件 点唱机 
- [○]自动战斗
   能打，但策略不太行
- [ ]掉落识别(画饼ing)
   给[圣洛夫数据部](https://github.com/St-Pavlov-Data-Department)上报掉落！

## 使用说明
得到本项目之后你需要保证你的电脑拥有以下的程序:
- Python3

在运行之前需要使用adb与模拟器链接具体代码在main.py,并且拥有以下的库：
- opencv-python
- loguru
- pyautogui
- requests

(在命令行运行 pip install opencv-python loguru pyautogui requests)

在安装结束之后，请配置`config.json`  
将模拟器分辨率设置为1600*900 240DPI  

如果不是蓝叠模拟器hyper-v版，请直接将adb连接地址填入adb_adress中。 （mumu12：127.0.0.1:16384） （mumu：127.0.0.1:7555）其他的在模拟器中查询。或者去搜索。  
如果是蓝叠模拟器hyper-v版的话，请仿照[MAA的指南](https://maa.plus/docs/1.2-%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.html#%E8%93%9D%E5%8F%A0%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%AF%8F%E6%AC%A1%E5%90%AF%E5%8A%A8%E7%AB%AF%E5%8F%A3%E5%8F%B7%E9%83%BD%E4%B8%8D%E4%B8%80%E6%A0%B7-hyper-v)，将转义后的 `bluestacks.conf` 路径填入  `bluestacks_conf_path`，  
将 `"bst.instance.模拟器编号.status.adb_port"` 填入`bluestacks_adb_port_keys` 

1.单机运行  
   运行main.py即可(main.py现已自带adb初始化)  
   在main.py中（在代码介绍中可以看到一些相关调用的介绍，然后取消注释掉你想要的功能。 不需要用的时候就注释。
   
   如需持续运行请使用daily.py

2.云端部署+本地运行  
   在`config.json`中配置`"server"`然后运行`ea.damon.py`
   服务端搓好了但是还没公开（）

## 代码介绍
   参照[代码介绍（旧）](https://github.com/YumisLink/1999-Auto/blob/main/docs/%E4%BB%A3%E7%A0%81%E4%BB%8B%E7%BB%8D(%E6%97%A7).md)

## QQ群:[707816032](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=Htwi2RJhZZqG41c_8loRfOq3z-ZIViqw&authKey=hFwGqmoCiaqcm2Gi7cfVUYizrqFlV4Yboo81hbPcgJWLXj3ejsEpBwS989jZ3rLr&noverify=0&group_code=707816032)

## 免责声明
不会对您的任何损失负责，包括但不限于账号异常、收益限制、账号回收等

## 致谢
- [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)
   本脚本所使用的ocr识别引擎