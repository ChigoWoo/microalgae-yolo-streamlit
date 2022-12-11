from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import detect
import os
import sys
import argparse
import pandas as pd
from PIL import Image


def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)

import base64

# def set_bg(main_bg):
#     st.markdown(
#         f"""
#          <style>
#          .stApp {{
#              background: url(data:image/png;base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
#              background-size: contain
#          }}

#          </style>
#          """,
#         unsafe_allow_html=True
#     )


if __name__ == '__main__':

    st.set_page_config(
        page_title="微藻智能化在线检测平台",
        page_icon="page.ico",   # page_icon="🧊"
        layout="wide",
   initial_sidebar_state="expanded",         # 设置网页的图标和标题
)
    
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)      # 隐藏网页右上角主菜单按钮

    st.sidebar.image("logo.png")
    st.sidebar.title("设置")
    
    st.subheader('')
       
    img_url = 'https://s1.ax1x.com/2022/12/11/zhpMLR.png'   # 设置网页背景图片
    st.markdown('''<style>.css-fg4pbf{background-image:url(''' + img_url + ''');
    background-size:100% 100%;background-attachment:fixed; color:rgb(255 255 255);}</style>
    ''', unsafe_allow_html=True) 

    st.markdown('''<style>.css-10trblm.e16nr0p30{margin-left:calc(3rem);
    scroll-margin-top: 2rem;color:rgb(255 255 255);text-align:center;}</style>''', unsafe_allow_html=True)    # 设置网页title和header居中

    st.markdown('''<style>.css-18ni7ap.e8zbici2{position: fixed;
    top: 0px;
    left: 0px;
    right: 0px;
    height: 0rem;
    background: rgba(4, 72, 117, 0.9);
    outline: none;
    z-index: 999990;
    display: block;}</style>''', unsafe_allow_html=True)   #设置网页顶部菜单栏样式

    st.markdown('''<style>.css-6qob1r.e1fqkh3o3{background:rgba(4, 72, 117, 0.9);}</style>''', unsafe_allow_html=True)  # 设置左侧边栏背景颜色为蓝色，跟页面背景颜色保持一致

    st.markdown('''<style>.css-184tjsw p{color:rgb(255 255 255);}</style>''', unsafe_allow_html=True)  # 设置左侧边栏p（即各设置模块标题为白色）

    st.markdown('''<style>.css-1629p8f h1{color:rgb(255 255 255);scroll-margin-top: 1rem;}</style>''', unsafe_allow_html=True)  # 设置左侧边栏h1（即“设置”两字为白色）

    st.markdown('''<style>.css-fblp2m{color:rgb(255 255 255);}</style>''', unsafe_allow_html=True)  # 设置侧边栏左上角按钮颜色为白色

    st.markdown('''<style>.css-qri22k.egzxvld0{color:rgba(4, 72, 117, 0);}</style>''', unsafe_allow_html=True)  # 设置底部footer样式,使Made with隐身
    st.markdown('''<style>.css-1vbd788.egzxvld1{color:rgba(4, 72, 117, 0);}</style>''', unsafe_allow_html=True)  # 设置底部footer样式,使Streamlit隐身

    st.markdown('''<style>.css-629wbf.edgvbvh10{background:rgba(127, 127, 127, 0.3);}</style>''', unsafe_allow_html=True)  # 设置“开始检测”按钮背景颜色
    st.markdown('''<style>.css-1offfwp p{color:rgb(255 255 255);}</style>''', unsafe_allow_html=True)  # 设置“检测完成”样式为白色
    st.markdown('''<style>.st-c7{background: rgba(255, 255, 255, 0);}</style>''', unsafe_allow_html=True)  # 设置“tab”样式为透明
    st.markdown('''<style>.css-1x8cf1d.edgvbvh10{background: rgba(127, 127, 127, 0.2);}</style>''', unsafe_allow_html=True)  # 设置“tab”样式为透明

    # st.markdown('''<style>.css-s1jz82f8{text-align:center;}</style>''', unsafe_allow_html=True)

    source1 = ("microalgae detection.pt", "microalgae detection-enhanced.pt", "coco detection.pt")
    source1_index = st.sidebar.selectbox("模型选择", ["microalgae detection.pt", "microalgae detection-enhanced.pt", "coco detection.pt"])

    values1 = st.sidebar.slider('置信度阈值',0.0, 1.0, 0.35, help="object confidence threshold")
    st.sidebar.write('Confidence:', values1)

    values2 = st.sidebar.slider('IoU阈值',0.0, 1.0, 0.45, help="IOU threshold for NMS")
    st.sidebar.write('IoU:', values2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("📋微藻数据集")
        tab1, tab2, tab3 = st.tabs(["📈 Data informaton", "🧊 Data samples", "🔬 Data preprocess"])

        dataframe=pd.DataFrame({
            '微藻种类': ['纤维藻', '小球藻', '腔球藻', '裸藻', '多芒藻', '异极藻', '束球藻', '微囊藻', '舟形藻', '盘星藻', '席藻', '栅藻', '螺旋藻', '针杆藻'],
            '英文名': ['Ankistrodesmus', 'Chlorella', 'Coelosphaerium', 'Euglena', 'Golenkinia', 'Gomphonema', 'Gomphosphaeria', 'Microcystis', 'Navicula', 'Pediastrum', 'Phormidium', 'Scenedesmus', 'Spirogyra', 'Synedra'],
            '所属门': ['绿藻门', '绿藻门', '蓝藻门', '裸藻门', '绿藻门', '硅藻门', '蓝藻门', '蓝藻门', '硅藻门', '绿藻门', '蓝藻门', '绿藻门', '蓝藻门', '硅藻门'],
            '所属科': ['小球藻科', '小球藻科', '色球藻科', '裸藻科', '绿球藻科', '异极藻科', '真囊球藻科', '色球藻科', '舟形藻科', '水网藻科', '席藻科', '栅藻科', '颤藻科', '脆杆藻科'],
            '标签': ['Ank', 'Chl', 'Coe', 'Eug', 'Gol', 'Gon', 'Gos', 'Mic', 'Nav', 'Ped', 'Pho', 'Sce', 'Spi', 'Syn'],
            '数量': [64, 80, 77, 81, 60, 87, 58, 307, 75, 95, 276, 86, 89, 77],
            '备注': ['扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充', '扩充'],
        })
        # tab1.subheader("微藻数据集信息")
        tab1.write(dataframe)

        # tab2.subheader("微藻显微图像样本")
        tab2.write("微藻显微图像样本如图所示：")
        tab2.image("samples.png")

        # tab3.subheader("数据预处理")
        tab3.write("1.数据筛选")
        tab3.write("本项目所使用的数据集来自东北大学提供的环境微生物数据集EMDS-7[https://figshare.com/articles/dataset/EMDS-7_DataSet/16869571 ]。\
            EMDS-7数据集一共包含有2365张微生物显微图像，41个微生物类别。所有显微图像均是在光学显微镜下放大400倍拍摄获取。由于本项目研究对象主要是微生物中的微藻，\
                故在原始数据集的基础上进行进一步的筛选，选出其中14种共计1512张微藻显微图像组成微藻数据集，按照7：1：2的比例划分训练集、验证集、测试集。")
        tab3.write("2.数据标注")
        tab3.write("使用labelImg标注工具对数据集进行标注，每一类微藻标注的标签参见表1。在标注过程中，对显微图像中无法得知的微生物以及一些杂质统一标注为unknown。\
            需要说明的是，由于本项目主要研究对微藻的检测，unknown尽管作为标签之一，但是在计算平均精度均值时不考虑unknown类。最后，获得的标签文件为PASCAL VOC格式的XML文件。")
        expander = tab3.expander("点击展开")
        expander.write("3.数据增强")
        expander.write("由于微藻数据集的数据样本量不足以让模型在训练时达到收敛状态，为了提高模型的识别分类准确率，采用高斯模糊、水平翻转、垂直翻转、非等比例缩放、随机平移、\
            透视变换、随机裁切等数据增强方式随机组合，对训练集进行扩充，最后共计获得15480张训练集样本。部分数据增强样本如图所示。")
        expander.image("data_augmentation.png")



    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str,
                        default="weights/"+source1_index, help='model.pt path(s)')
    parser.add_argument('--source', type=str,
                        default='data/images', help='source')
    parser.add_argument('--img-size', type=int, default=640,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=values1, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
<<<<<<< HEAD
                        default=values2, help='IOU threshold for NMS')
=======
                        default=0.45, help='IOU threshold for NMS')
>>>>>>> f635ff2ecbb0f065abb3cdb62fe6bc2828ea23a9
    parser.add_argument('--device', default='',
                        help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true',
                        help='display results')
    parser.add_argument('--save-txt', action='store_true',
                        help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true',
                        help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true',
                        help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int,
                        help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true',
                        help='augmented inference')
    parser.add_argument('--update', action='store_true',
                        help='update all models')
    parser.add_argument('--project', default='runs/detect',
                        help='save results to project/name')
    parser.add_argument('--name', default='exp',
                        help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true',
                        help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)
    
    source = ("图片检测", "视频检测", "摄像头检测")
    source_index = st.sidebar.selectbox("检测方式", range(
        len(source)), format_func=lambda x: source[x])

    if source_index == 0:
        uploaded_file = st.sidebar.file_uploader(
            "上传图片", type=['png', 'jpeg', 'jpg'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='图片加载中...'):
                # st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/images/{uploaded_file.name}')
                opt.source = f'data/images/{uploaded_file.name}'
        else:
            is_valid = False
    elif source_index == 1:
        uploaded_file = st.sidebar.file_uploader("上传视频", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='视频加载中...'):
                # st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                opt.source = f'data/videos/{uploaded_file.name}'
        else:
            is_valid = False

    else:
        uploaded_file = st.camera_input("打开摄像头")
        # uploaded_file = st.sidebar.file_uploader("打开摄像头", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='摄像头加载中...'):
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/images/{uploaded_file.name}')
                opt.source = f'data/images/{uploaded_file.name}'
        else:
            is_valid = False

    with  col3:
        st.header("📒使用说明")
        tab6, tab7 = st.tabs(["🖥️ About platform", "🙎 About me"])
        # tab6.subheader("关于平台")
        tab6.write("1.本平台为微藻智能化在线检测平台，可实现对纤维藻、小球藻、腔球藻、裸藻、多芒藻、异极藻、\
            束球藻、微囊藻、舟形藻、盘星藻、席藻、栅藻、螺旋藻、针杆藻等14种微藻的实时高效智能化检测，并对检测结果进行保存；")
        tab6.write("2.本平台的主要功能有：模型选择、置信度阈值、IoU阈值、检测方式；")
        expander = tab6.expander("点击展开")
        expander.write("3.模型选择：可选择的模型为microalgae detection.pt、microalgae detection-enhanced.pt，\
            前者是基于YOLO v7检测算法训练微藻数据集得到，后者是基于改进YOLO v7(YOLO v7-MA)检测算法训练微藻数据集得到。\
                另外，还有一个coco detection.pt模型可供选择，该模型通过训练COCO数据集得到，可供用户检测如人、小车、杯子等\
                    常见目标，具体类别可参考COCO数据集官方介绍；")
        expander.write("4.置信度阈值：用户可自主设置模型检测的置信度阈值，取值范围为0-1之间；")
        expander.write("5.Iou阈值：用户可自主设置模型检测的非极大值抑制中的交并比阈值，取值范围为0-1之间；")
        expander.write("6.检测方式：目前本平台提供的检测方式主要有：图片检测、视频检测和摄像头检测（摄像头检测目前仅支持PC端），用户可以对检测结果进行下载保存；")
        expander.write("7.本平台前后端均基于Streamlit开发，Streamlit是一个可以用于快速搭建Web应用的开源Python库，\
            开发文档参见：https://docs.streamlit.io/ ")
        expander.write("8.在本台的开发过程中，也参考了xugaoxiang的GitHub仓库[https://github.com/xugaoxiang/yolov5-streamlit ]，特此申明并表示感谢；")
        expander.write("9.本平台仅用作学术交流，已在Github上开源[https://github.com/qifengle523/microalgae-yolov-streamlit ]，可自由git，\
            但不可用于任何盈利性用途，违者必究。喜欢的话可以给个star，谢谢~")

        # tab7.subheader("关于作者")
        tab7.write("Chigo，一枚就读于SHOU的理工男，主要研究方向为计算机视觉、目标检测。E-mail：chigowu@foxmail.com")

    with col2:
        st.header("🗂️检测结果")
        tab4, tab5 = st.tabs(["🚀 Detection result", "🗺️ Original file"])


        if is_valid:
            print('valid')
            button = st.sidebar.button('开始检测')
            if button:

                detect(opt)

                if source_index == 0:
                    with st.spinner(text='Preparing Images'):
                        for img in os.listdir(get_detection_folder()):
                            tab4.image(str(Path(f'{get_detection_folder()}') / img))
                            with open(str(Path(f'{get_detection_folder()}') / img), "rb") as file:
                                tab4.download_button(label="保存结果", data=file, mime="image/jpg")
                            tab5.image(uploaded_file)

                        st.snow()
                        st.success('检测完成！点击图片右上角，可全屏查看检测结果.', icon="✅")
                elif source_index == 1:
                    with st.spinner(text='Preparing Videos'):
                        for vid in os.listdir(get_detection_folder()):
                            tab4.video(str(Path(f'{get_detection_folder()}') / vid))
                            with open(str(Path(f'{get_detection_folder()}') / vid), "rb") as file:
                                tab4.download_button(label="保存结果", data=file, mime="video/mp4")
                            tab5.video(uploaded_file)

                        st.balloons()
                        st.success('检测完成', icon="✅")
                else:
                    with st.spinner(text='Preparing Images'):
                        for img in os.listdir(get_detection_folder()):
                            tab4.image(str(Path(f'{get_detection_folder()}') / img))
                            with open(str(Path(f'{get_detection_folder()}') / img), "rb") as file:
                                tab4.download_button(label="保存结果", data=file, mime="image/jpg")
                            tab5.image(uploaded_file)

                        st.snow()
                        st.success('检测完成！点击图片右上角，可全屏查看检测结果.', icon="✅")


    