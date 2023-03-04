from io import StringIO
from pathlib import Path
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
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



if __name__ == '__main__':

    st.set_page_config(
        page_title="微藻智能化在线检测平台",
        page_icon="page.ico",   # page_icon="🧊"
        layout="wide",
    initial_sidebar_state="expanded",         # 设置网页的图标和标题
    )

    __login__obj = __login__(auth_token = "pk_prod_JTMKNS6DCXM670NK2M4ZTGN5JFW8", 
                company_name = "SHOU_Chigo",
                width = 200, height = 250, 
                logout_button_name = '退出(Logout)', hide_menu_bool = True, 
                hide_footer_bool = True, 
                lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN = __login__obj.build_login_ui()

    if LOGGED_IN == True:

        hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_menu_style, unsafe_allow_html=True)      # 隐藏网页右上角主菜单按钮

        st.sidebar.image("logo.png")
        st.sidebar.title("设置")
        
        #st.subheader('')
        
        img_url = 'https://s1.ax1x.com/2023/03/03/ppAEACF.jpg'   # 设置网页背景图片
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
        display: block;}</style>''', unsafe_allow_html=True)   #设置网页顶部菜单栏样式(高度设为0)

        st.markdown('''<style>.css-6qob1r.e1fqkh3o3{background:rgba(4, 72, 117, 0.9);}</style>''', unsafe_allow_html=True)  # 设置左侧边栏背景颜色为蓝色，跟页面背景颜色保持一致

        st.markdown('''<style>.css-184tjsw p{color:rgb(255 255 255);}</style>''', unsafe_allow_html=True)  # 设置左侧边栏p（即各设置模块标题为白色）

        st.markdown('''<style>.css-1629p8f h1{color:rgb(255 255 255);scroll-margin-top: 1rem;}</style>''', unsafe_allow_html=True)  # 设置左侧边栏h1（即“设置”两字为白色）

        st.markdown('''<style>.css-fblp2m{color:rgb(255 255 255);}</style>''', unsafe_allow_html=True)  # 设置侧边栏左上角按钮颜色为白色
        st.markdown('''<style>.css-1vq4p4l.e1fqkh3o4{padding-top: 1rem;}</style>''', unsafe_allow_html=True)  # 设置侧边栏padding-top

        st.markdown('''<style>.css-qri22k.egzxvld0{color:rgba(4, 72, 117, 0);}</style>''', unsafe_allow_html=True)  # 设置底部footer样式,使Made with隐身
        st.markdown('''<style>.css-1vbd788.egzxvld1{color:rgba(4, 72, 117, 0);}</style>''', unsafe_allow_html=True)  # 设置底部footer样式,使Streamlit隐身

        st.markdown('''<style>.css-629wbf.edgvbvh10{background:rgba(127, 127, 127, 0.3);}</style>''', unsafe_allow_html=True)  # 设置“开始检测”按钮背景颜色
        st.markdown('''<style>.css-1offfwp p{color:rgb(255 255 255);}</style>''', unsafe_allow_html=True)  # 设置“检测完成”样式为白色
        st.markdown('''<style>.st-c7{background: rgba(255, 255, 255, 0);}</style>''', unsafe_allow_html=True)  # 设置“tab”样式为透明
        st.markdown('''<style>.st-du{background: rgba(255, 255, 255, 0);}</style>''', unsafe_allow_html=True)  # 设置“tab”样式为透明
        st.markdown('''<style>.css-1x8cf1d.edgvbvh10{background: rgba(127, 127, 127, 0.2);}</style>''', unsafe_allow_html=True)  # 设置“保存结果”按钮背景颜色为半透明
        st.markdown('''<style>.st-bx{background-color: rgba(255, 255, 255, 0);}</style>''', unsafe_allow_html=True)  # 设置“模型选择”和“检测方式”框样式为透明
        st.markdown('''<style>.st-eg{background-color: rgba(255, 255, 255, 0);}</style>''', unsafe_allow_html=True)  # 设置“模型选择”和“检测方式”框样式为透明
        st.markdown('''<style>.st-bs{color: rgb(255, 255, 255);}</style>''', unsafe_allow_html=True)  # 设置“tab”字体为白色
        st.markdown('''<style>.st-ct{color: rgb(255, 255, 255);}</style>''', unsafe_allow_html=True)  # 设置“模型选择”和“检测方式”框默认值字体为白色
        st.markdown('''<style>.css-16kzsd9.e1wbw4rs0{color: rgb(255, 255, 255);background: rgba(4, 72, 117, 0.9);}</style>''', unsafe_allow_html=True)  # 设置“模型选择”和“检测方式”下拉框字体为白色，背景色与侧边栏背景色一致
        st.markdown('''<style>.css-bn3168.e1wbw4rs0{color: rgb(255, 255, 255);background: rgba(4, 72, 117, 0.9);}</style>''', unsafe_allow_html=True)  # 设置“模型选择”和“检测方式”下拉框字体为白色，背景色与侧边栏背景色一致
        st.markdown('''<style>.css-1dhfpht.exg6vvm15{color: rgb(255, 255, 255);background-color: rgba(255, 255, 255, 0.1);}</style>''', unsafe_allow_html=True)  # 设置“上传图片”和“上传视频”框样式为半透明
        st.markdown('''<style>.css-slh8gl.ejtjsn20{background: rgba(255, 255, 255, 0);}</style>''', unsafe_allow_html=True)  # 设置“take photo”按钮样式为透明

        source1 = ("microalgae detection.pt", "microalgae detection-enhanced.pt", "coco detection.pt")
        source1_index = st.sidebar.selectbox("模型选择", ["microalgae detection.pt", "microalgae detection-enhanced.pt", "coco detection.pt"])

        values1 = st.sidebar.slider('置信度阈值',0.0, 1.0, 0.35, help="object confidence threshold")
        st.sidebar.write('Confidence:', values1)

        values2 = st.sidebar.slider('IoU阈值',0.0, 1.0, 0.45, help="IOU threshold for NMS")
        st.sidebar.write('IoU:', values2)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("📋微藻数据集")
            tab1, tab2, tab3 = st.tabs(["📈 Data informaton", "🧊 Data samples", "🔬 Data source"])

            df=pd.DataFrame({
                '微藻种类': ['纤维藻', '小球藻', '腔球藻', '裸藻', '多芒藻', '异极藻', '束球藻', '微囊藻', '舟形藻', '盘星藻', '席藻', '栅藻', '螺旋藻', '针杆藻'],
                '英文名': ['Ankistrodesmus', 'Chlorella', 'Coelosphaerium', 'Euglena', 'Golenkinia', 'Gomphonema', 'Gomphosphaeria', 'Microcystis', 'Navicula', 'Pediastrum', 'Phormidium', 'Scenedesmus', 'Spirogyra', 'Synedra'],
                '所属门': ['绿藻门', '绿藻门', '蓝藻门', '裸藻门', '绿藻门', '硅藻门', '蓝藻门', '蓝藻门', '硅藻门', '绿藻门', '蓝藻门', '绿藻门', '蓝藻门', '硅藻门'],
                '所属科': ['小球藻科', '小球藻科', '色球藻科', '裸藻科', '绿球藻科', '异极藻科', '真囊球藻科', '色球藻科', '舟形藻科', '水网藻科', '席藻科', '栅藻科', '颤藻科', '脆杆藻科'],
                '标签': ['Ank', 'Chl', 'Coe', 'Eug', 'Gol', 'Gon', 'Gos', 'Mic', 'Nav', 'Ped', 'Pho', 'Sce', 'Spi', 'Syn'],
            })
            # tab1.subheader("微藻数据集信息")
            tab1.dataframe(df)

            # tab2.subheader("微藻显微图像样本")
            tab2.write("微藻显微图像样本如图所示：")
            tab2.image("samples.png")
            # tab2.markdown("1.纤维藻：植物体单细胞，或2个、4个、8个、16个或更多个细胞聚集成群，浮游，罕为附着在基质上；细胞纺锤形、针形、弓形、镰形或螺旋形等多种形状；\
            #                2.小球藻：植物体为单细胞或为4个或更多的细胞暂时或长期无规则地聚集在一起的群体，浮游；细胞球形、椭圆形、纺锤形、长圆形、新月形、三角形、四角形等多种形状；  \
            #                3.腔球藻：群体微小，略为圆球形或卵形，有时由子群体组成，老群体罕见不规则形，常为自由漂浮；胶被薄，无色，常无明显界线；胶质仅在细胞周边层周边；\
            #                4.裸藻：细胞纺锤形、长纺锤形或圆柱形，前端宽而钝圆，后端锐，无甲鞘。周质体的弹性大小，因种而异。有两根鞭毛，1根由储蓄泡底部经过胞咽和胞口伸出，第二根鞭毛退化，保留在储蓄泡内。细胞核大，圆形。细胞内有许多载色体，分布近于原生质体表面，称边位载色体。少数种的载色体是中轴位，一般为星状，数目较少，只1-2个；\
            #                5.异极藻：壳面呈菱形-披针形，上下两端部不对称，中部较宽向两端逐渐变窄，顶端呈宽钝圆形，底端呈轻微钝圆形；中央区呈菱形，中央区两侧均有短线纹，两侧线纹稍短且在其中一侧短线纹处有1个孤点，孤点远离中央区靠近短线纹处，中央区的线纹呈辐射状排列。中轴区较窄呈横矩形。外壳面观，线纹单列由“C”形的点纹组成，近缝端末端略膨大呈泡状，远缝端呈弧形弯向壳套面，中央区孤点在外壳面开口为圆形，顶孔区由密集的小孔组成，被壳缝分为两部分，与线纹不连续；\
            #                6.多芒藻：单细胞。细胞球形，四周散生出多数不规则排列的纤细刺毛。有时刺毛缠绕在一起，形成暂时的群体。色素体1个，杯状；\
            #                7.束球藻：群体为球形、卵形、椭圆形，带有缢缩，直径达30-40μm；公共胶被均匀，无色透明；\
            #                8.微囊藻：小型的细胞且没有鞘的包覆。细胞常聚集成大至肉眼可见的群落，本为圆形，但随细胞数增多会逐渐出现孔洞并变不规则。其原生质体的颜色为浅蓝绿色，但充满气体的囊泡常会呈暗色；\
            #                9.舟形藻：细胞三轴皆对称，单独生活，也有以胶质营、胶质块形成群体的。壳面多为舟形，也有椭圆形、菱形、棍棒形和长方形等；\
            #                10.盘星藻：植物体由2～128个，但多数是由8～32个细胞构成的定形群体。细胞排列在一个平面上，大体呈辐射状；每个细胞内常有一个周位的盘状的色素体和一个蛋白核，有一个细胞核；细胞壁光滑，或具各种突出物，有的还具各种花纹；\
            #                11.席藻：藻丝单生，能动，或呈蛰状；无鞘或暂时存在，薄或坚硬，顶端开放，鞘内具一条或多条藻丝；几个属有伪分枝；除顶端细胞外其他细胞均能进行细胞分裂；具气囊或缺乏；\
            #                12.栅藻：由2个、4个、8个、16个、32个、64个、128个细胞组成，群体细胞彼此以其细胞壁上的凸起连接形成一定形状的群体，细胞排列在一个平面上呈栅状或四角状排列，或细胞不排列在一个平面上呈辐射状组列或形成多孔的、中空的球体到多角形体；细胞球形、三角形、四角形、纺锤形、长圆形、圆锥形、截顶的角锥形等，细胞壁平滑、具颗粒、刺、齿或隆起线，色素体周生，片状、杯状，1个，有点长成后扩散，几乎充满整个细胞，具1~2个蛋白核；\
            #                13.螺旋藻：藻丝体长200-500μm，宽5-10μm，在显微镜下呈疏松或紧密的有规则的螺旋弯曲状，形如钟表发条而得名。蓝藻类细胞无色素体，色素分布在原生质体外部的色素区，蓝绿色。藻体表面不具胶质鞘，不易被微生物附着，细胞内有气泡，上浮性好。细胞或藻丝顶部常不尖细，横壁常不明显，顶细胞圆形，外壁不增厚；\
            #                14.针杆藻：细胞长线形；单细胞或为放射状群体；壳面线形或长披针形，通常是直的，中部至两端略渐狭或等宽，末端呈头状；具假壳缝；带面长方形，末端截形，具明显的线纹；具2块色素体，位于壳体的两侧。")

            # tab3.subheader("数据来源")
            tab3.markdown("本项目所使用的数据集来自东北大学提供的环境微生物数据集[EMDS-7](https://figshare.com/articles/dataset/EMDS-7_DataSet/16869571)。")

        with  col3:
            st.header("📒使用说明")
            tab6, tab7 = st.tabs(["🖥️ About platform", "🙎 About me"])
            # tab6.subheader("关于平台")
            tab6.write("1.本平台为微藻智能化在线检测平台，可实现对纤维藻、小球藻、腔球藻、裸藻、多芒藻、异极藻、\
                束球藻、微囊藻、舟形藻、盘星藻、席藻、栅藻、螺旋藻、针杆藻等14种微藻的实时高效智能化检测，并对检测结果进行保存；")
            tab6.write("2.本平台的主要功能有：模型选择、置信度阈值、IoU阈值、检测方式；")
            expander = tab6.expander("点击展开")
            expander.write("3.模型选择：可选择的模型为microalgae detection.pt、microalgae detection-enhanced.pt，\
                            前两个模型可供用户检测微藻。最后一个模型可供用户检测如人、小车、杯子等常见目标，具体类别可参考COCO数据集官方介绍；")
            expander.write("4.置信度阈值：用户可自主设置模型检测的置信度阈值，取值范围为0-1之间；")
            expander.write("5.Iou阈值：用户可自主设置模型检测的非极大值抑制中的交并比阈值，取值范围为0-1之间；")
            expander.write("6.检测方式：目前本平台提供的检测方式主要有：图片检测、视频检测和摄像头检测，其中，图片和视频支持批量上传检测，用户可以对检测结果进行下载保存；")
            expander.markdown("7.本平台前后端均基于Streamlit开发，[Streamlit](https://docs.streamlit.io/)是一个可以用于快速搭建Web应用的开源Python库; ")
            expander.markdown("8.在本平台的开发过程中，也参考了[xugaoxiang](https://github.com/xugaoxiang/yolov5-streamlit)的GitHub仓库，特此申明并表示感谢；")
            expander.markdown("9.本平台仅用作学术交流，已在Github上开源，[点击前往](https://github.com/qifengle523/microalgae-yolov-streamlit)，可自由git，\
                但不可用于任何盈利性用途。喜欢的话可以给个star，谢谢~")

            # tab7.subheader("关于作者")
            tab7.write("Chigo，一枚就读于SHOU的理工男，主要研究方向为计算机视觉、目标检测。E-mail：chigowu@foxmail.com")

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
                            default=values2, help='IOU threshold for NMS')
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
            len(source)), format_func=lambda x: source[x], help="图片和视频支持批量上传检测")

        with col2:
            st.header("🗂️检测结果")
            tab4, tab5 = st.tabs(["🚀 Detection result", "🗺️ Original file"])
            expander4 = tab4.expander("点击展开，查看其余检测结果")
            expander5 = tab5.expander("点击展开，查看其余原文件")

        if source_index == 0:
            uploaded_files = st.sidebar.file_uploader(
                "上传图片", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
            if uploaded_files is not None:
                is_valid = True
                button = st.sidebar.button('开始检测')
                with st.spinner(text='图片加载中...'):
                    count = 0
                    for uploaded_file in uploaded_files:
                        count += 1
                        picture = Image.open(uploaded_file)
                        picture = picture.save(f'data/images/{uploaded_file.name}')
                        opt.source = f'data/images/{uploaded_file.name}'
                        # opt.save_txt = True
                        detect(opt)
                        if button:    
                            with st.spinner(text='Preparing Images'):
                                for img in os.listdir(get_detection_folder()):
                                    if count == 1:
                                        tab4.write('After detection: '+img)
                                        tab4.image(str(Path(f'{get_detection_folder()}') / img))
                                        with open(str(Path(f'{get_detection_folder()}') / img), "rb") as file:
                                            tab4.download_button(label="保存结果", data=file, mime="image/jpg", key = str(count))
                                        tab5.write('Before detection: '+img)
                                        tab5.image(uploaded_file)
                                    else:
                                        expander4.write('After detection: '+img)
                                        expander4.image(str(Path(f'{get_detection_folder()}') / img))
                                        with open(str(Path(f'{get_detection_folder()}') / img), "rb") as file:
                                            expander4.download_button(label="保存结果", data=file, mime="image/jpg", key = str(count))
                                        expander5.write('Before detection: '+img)
                                        expander5.image(uploaded_file) 
                                # st.snow()
                                #st.success('检测完成！点击图片右上角，可全屏查看检测结果.', icon="✅")
            else:
                is_valid = False
        
        elif source_index == 1:
            uploaded_files = st.sidebar.file_uploader("上传视频", type=['mp4'], accept_multiple_files=True)
            if uploaded_files is not None:
                is_valid = True
                button = st.sidebar.button('开始检测')
                with st.spinner(text='视频加载中...'):
                    count = 0
                    for uploaded_file in uploaded_files:
                        count += 1
                        with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        opt.source = f'data/videos/{uploaded_file.name}'
                        detect(opt)
                        if button:
                            with st.spinner(text='Preparing Videos'):
                                for vid in os.listdir(get_detection_folder()):
                                    if count == 1:
                                        tab4.write('After detection: '+vid)
                                        tab4.video(str(Path(f'{get_detection_folder()}') / vid))
                                        with open(str(Path(f'{get_detection_folder()}') / vid), "rb") as file:
                                            tab4.download_button(label="保存结果", data=file, mime="video/mp4", key = str(count))
                                        tab5.write('Before detection: '+vid)
                                        tab5.video(uploaded_file)
                                    else:
                                        expander4.write('After detection: '+vid)
                                        expander4.video(str(Path(f'{get_detection_folder()}') / vid))
                                        with open(str(Path(f'{get_detection_folder()}') / vid), "rb") as file:
                                            expander4.download_button(label="保存结果", data=file, mime="video/mp4", key = str(count))
                                        expander5.write('Before detection: '+vid)
                                        expander5.video(uploaded_file)
                                # st.balloons()
                                #st.success('检测完成', icon="✅")
            else:
                is_valid = False

        else:
            with st.spinner(text='正在检测摄像头...'):
                uploaded_file = st.camera_input("打开摄像头")
                if uploaded_file is not None:
                    is_valid = True
                    button = st.sidebar.button('开始检测')
                    picture = Image.open(uploaded_file)
                    picture = picture.save(f'data/images/{uploaded_file.name}')
                    opt.source = f'data/images/{uploaded_file.name}'
                    detect(opt)
                    if button:
                        with st.spinner(text='Preparing Images'):
                            for img in os.listdir(get_detection_folder()):
                                tab4.image(str(Path(f'{get_detection_folder()}') / img))
                                with open(str(Path(f'{get_detection_folder()}') / img), "rb") as file:
                                    tab4.download_button(label="保存结果", data=file, mime="image/jpg")
                                tab5.image(uploaded_file)
                        # st.snow()
                        st.success('检测完成！点击图片右上角，可全屏查看检测结果.', icon="✅")                
                else:
                    is_valid = False
