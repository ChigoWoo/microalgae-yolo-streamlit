# Microalgae Detection Based on Yolo-Streamlit

## 在线体验

微藻智能化在线检测平台: <https://microalgaedetection.streamlit.app/>

__2023.3.4更新__

## 更新内容

1.新增系统登陆、注册、退出等功能。

**登陆界面**

![login page](data/images/login.png)

**退出界面**

![logout page](data/images/logout.jpg)

__2022.12.12更新__

## 更新内容

1.新增批量检测功能，支持图片和视频批量上传检测；\
2.优化界面UI设计。

## 检测界面
**图片检测**

![image detection](data/images/image3.png)

**视频检测**

![video detection](data/images/video3.png)

**摄像头检测**

![video detection](data/images/camera2.png)

------------
__2022.12.11更新__

## 更新内容

1.新增模型选择、置信度阈值、IoU阈值自主设置功能；\
2.新增摄像头检测功能；\
3.新增检测结果保存功能；\
4.新增微藻数据集和使用说明两个板块，检测结果板块支持查看检测结果图和原图；\
5.重新设计界面UI。

## 检测界面
**图片检测**

![image detection](data/images/image2.png)

**视频检测**

![video detection](data/images/video2.png)

**摄像头检测**

![video detection](data/images/camera.png)

------------
__2022.12.09__

## 环境配置

```
pip install -r requirements.txt
```

若在本地安装，请将`opencv-python-headless`改为`opencv-python`\
如果本地或者服务器上有`GPU`配置，可将`torch`替换成`gpu`版本以加速检测\
目前在Streamlit平台部署，暂不支持`gpu`版本的`torch`，直接按照`requirements.txt`默认安装即可

## 启动项目

```
streamlit run main.py
```
## 检测界面
**图片检测**

![image detection](data/images/image.png)

**视频检测**

![video detection](data/images/video.png)

## 在线体验

直接访问: <https://microalgaedetection.streamlit.app/>

## References
[1] <https://docs.streamlit.io/>\
[2] <https://github.com/xugaoxiang/yolov5-streamlit>\
[3] <https://xugaoxiang.com/2021/08/27/yolov5-streamlit/>\
[4] <https://github.com/GauriSP10/streamlit_login_auth_ui>