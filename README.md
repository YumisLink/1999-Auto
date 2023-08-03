# 1999-Auto
### 本项目只是突发奇想做的一个小项目，我只是提供一个思路，现在是测试版，另外有人有想法的话可以提供issue或者直接提供pull request到decisions目录下。
### 本项目的制作只是本人学习python的一个途径，并非要制作成一个长期支持的软件。（听说maa已经在做1999了）[MAA1999](https://github.com/MaaAssistantArknights/MAA1999)  

我的python并不是很精通，毕竟是一个oi选手关于如何做这种程序化的项目不太熟悉。所以都是东拼西凑的东西，也欢迎大佬指点，欢迎大佬fork我的项目进行改进。
QQ群:[707816032](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=Htwi2RJhZZqG41c_8loRfOq3z-ZIViqw&authKey=hFwGqmoCiaqcm2Gi7cfVUYizrqFlV4Yboo81hbPcgJWLXj3ejsEpBwS989jZ3rLr&noverify=0&group_code=707816032)


## 免责声明
不会对您的任何损失负责，包括但不限于账号异常、收益限制、账号回收等



# 使用说明
得到本项目之后你需要保证你的电脑拥有以下的程序:
- Python3

在运行之前需要使用adb与模拟器链接具体代码在main.py,并且拥有以下的库：
- opencv-python
- loguru
- pyautogui
(在命令行运行 pip install opencv-python loguru pyautogui)

在安装结束之后，请配置`config.json`  
将模拟器分辨率设置为1600*900 240DPI  

如果不是蓝叠模拟器hyper-v版，请直接将adb连接地址填入adb_adress中。 （mumu12：127.0.0.1:16384） （mumu：127.0.0.1:7555）其他的在模拟器中查询。或者去搜索。  
如果是蓝叠模拟器hyper-v版的话，请仿照[MAA的指南](https://maa.plus/docs/1.2-%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.html#%E8%93%9D%E5%8F%A0%E6%A8%A1%E6%8B%9F%E5%99%A8%E6%AF%8F%E6%AC%A1%E5%90%AF%E5%8A%A8%E7%AB%AF%E5%8F%A3%E5%8F%B7%E9%83%BD%E4%B8%8D%E4%B8%80%E6%A0%B7-hyper-v)，将转义后的 `bluestacks.conf` 路径填入  `bluestacks_conf_path`，  
将 `"bst.instance.模拟器编号.status.adb_port"` 填入`bluestacks_adb_port_keys`  
然后运行main.py即可(main.py现已自带adb初始化)  


在main.py中（在下面可以看到一些相关调用的介绍，然后取消注释掉你想要的功能。 不需要用的时候就注释。


## 代码介绍
因为我真的懒得写注释就在这里稍微介绍一下：

目前自动战斗的逻辑如下：

decision_1:
对卡中的卡牌进行优先级排列，对于点击之后能让卡牌更近或者合成的卡基于高优先级，然后其次按照buff—>大招->dps的输出->其他的填充技能 为顺序，自动出卡。

1. 通过下方的卡牌识别，在识别到下方的卡牌是能被识别到的时候，开始任务（这里等待了1.5秒之后再重新识别一次防止对方回合或者一些其他事件）
2. - 识别卡牌：这里用了卡牌的三通道相似度的计算，对照图片来自于bilibiliwiki，我把图片保存在cards文件夹中，分别用角色的名字+123命名3是大招。然后再cards中的aname.py中保存对照出技能名字，在通过下面数组分类。
3. 判断buff和debuff是否需要上，否则就进行攻击。

目前只有这样。

目前对于角色卡牌的识别已经支持以下的角色：

六星：温妮弗雷德（Eternity）、兔毛手袋（MedicinePocket）、新巴别塔（NewBabel）、泥鯭的士（Anan）、新巴别塔（NewBabel）、苏芙比（Sotheby）、槲寄生（Druvis）、远旅（Voyager）、未锈铠（Knight）、红弩箭（Lilya）、星锑（Regulus）、百夫长（Centurion）

五星：柏林以东（Bkornblume）、十四行诗（Sonetto）、夏利（Charlie）、气球派对（BalloonParty）、玛蒂尔达（Matilda）、玛丽莲（Sweetheart）、五色月（Satsuki）、婴儿蓝（BabyBlue）、讣告人（Necrologist）、帕米埃（Dikke）、喀嚓喀嚓（Click）、X（X）、坦南特（Tennant）


# 更新日志

## 2023-06-14  ver0.07
   - 更新了adb初始化，添加了对蓝叠模拟器的支持，使用了PaddleOCR-json替代cnocr
   - 添加了path相关api——支持从模拟器启动开始运行自动进入游戏主界面（前提是180s内能进去）
   - 修复了adb部分的一些bug 
   - 在api里新增了裁屏匹配函数

## 2023-06-12  ver0.06
   - 本次更新了决策一，决策一可以选择目前对于选择卡牌来说最优的做法（无法识别敌人。）

## 2023-06-10  ver0.04
   - 本次更新之后需要拥有cnocr才能运行
   - 增加了圣遗物经验本和基建材料本的识别，并且如果找不到会进行拖动寻找。
   - 增加了基建收材料(但是如果你还没有1%的时候就去收会出事情，不过还是会正常返回就是了)
   - 增加了自动完成任务
   - 修复了有关issue #2的内容     
   在main.py中 调用active.Auto_Active(active.关卡名, active.第几关（这里还没有写滑动寻找关卡）, active.（复现次数）)
## 2023-06-10  ver0.02
   本次更新了自动复现的功能。（视频的话等之后一件完成一起发放。目前支持钱本和经验本。）