# 1999-Auto
### 本项目只是突发奇想做的一个小项目，我只是提供一个思路，现在是测试版，另外有人有想法的话可以提供issue或者直接提供pull request到decisions目录下。
### 本项目的制作只是本人学习python的一个途径，并非要制作成一个长期支持的软件。（听说maa已经在做1999了）  
### 本项目的制作只是本人学习python的一个途径，并非要制作成一个长期支持的软件。（听说maa已经在做1999了）[MAA1999](https://github.com/MaaAssistantArknights/MAA1999)  

我的python并不是很精通，毕竟是一个oi选手关于如何做这种程序化的项目不太熟悉。所以都是东拼西凑的东西，也欢迎大佬指点，欢迎大佬fork我的项目进行改进。
QQ群:[707816032](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=Htwi2RJhZZqG41c_8loRfOq3z-ZIViqw&authKey=hFwGqmoCiaqcm2Gi7cfVUYizrqFlV4Yboo81hbPcgJWLXj3ejsEpBwS989jZ3rLr&noverify=0&group_code=707816032)


## 免责声明
@@ -26,13 +27,15 @@
# 使用说明
得到本项目之后你需要保证你的电脑拥有以下的程序:
- Python3
- adb

在运行之前需要使用adb与模拟器链接具体代码在main.py,并且拥有以下的库：
- opencv-python
- cnocr

在安装结束之后，运行main.py即可
在安装结束之后，请配置`config.json`  
如果不是蓝叠模拟器hyper-v版，请直接将adb连接地址填入adb_adress中。  
如果是蓝叠模拟器hyper-v版的话，请仿照[MAA的指南](https://maa.plus/docs/1.2-%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.html#%E8%93%9D%E5%8F%A0%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%AF%8F%E6%AC%A1%E5%90%AF%E5%8A%A8%E7%AB%AF%E5%8F%A3%E5%8F%B7%E9%83%BD%E4%B8%8D%E4%B8%80%E6%A0%B7-hyper-v)，将转义后的***bluestacks.conf***路径填入  `bluestacks_conf_path`，将***"bst.instance.模拟器编号.status.adb_port"*** 填入`bluestacks_adb_port_keys`  
然后运行main.py即可(main.py现已自带adb初始化)  
在main.py中 调用active.Auto_Active(active.关卡名, active.第几关（这里还没有写滑动寻找关卡）, active.（复现次数）)