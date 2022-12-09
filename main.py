from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import detect
import os
import sys
import argparse
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

def set_bg(main_bg):

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/png;base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: contain
         }}

         </style>
         """,
        unsafe_allow_html=True
    )

# button_css = '''<style>
# #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-1v3fvcr.egzxvld3 > div > div:nth-child(1) > div > div:nth-child(8) > div > button:focus{box-shadow:none;border-color:transparent};
# </style>
# <style>
# #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-1v3fvcr.egzxvld3 > div > div:nth-child(1) > div > div:nth-child(8) > div > button{
#   background-color:rgb(255 75 75);
#   color: rgb(255 255 255);
  
# };
# </style>
# <style>
# #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-1v3fvcr.egzxvld3 > div > div:nth-child(1) > div > div:nth-child(8) > div > button:active{background-color:rgb(231 105 105);
# barder-color:rgb(231 105 105);
# color:rgb(2 2 2);
  
# };
# </style>'''
# st.markdown(button_css,unsafe_allow_html=True)

if __name__ == '__main__':

    # st.title('微藻智能化在线检测平台')

    set_bg('bg.png')

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str,
                        default='weights/best.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str,
                        default='data/images', help='source')
    parser.add_argument('--img-size', type=int, default=640,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.35, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.45, help='IOU threshold for NMS')
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

    source = ("图片检测", "视频检测")
    source_index = st.sidebar.selectbox("检测方式", range(
        len(source)), format_func=lambda x: source[x])

    if source_index == 0:
        uploaded_file = st.sidebar.file_uploader(
            "上传图片", type=['png', 'jpeg', 'jpg'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='图片加载中...'):
                st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/images/{uploaded_file.name}')
                opt.source = f'data/images/{uploaded_file.name}'
        # if st.button('开始检测'):
        #     detect(opt)
        #     with st.spinner(text='Preparing Images'):
        #             for img in os.listdir(get_detection_folder()):
        #                 st.image(str(Path(f'{get_detection_folder()}') / img))
        #             st.balloons()
        else:
            is_valid = False
    else:
        uploaded_file = st.sidebar.file_uploader("上传视频", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='视频加载中...'):
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                opt.source = f'data/videos/{uploaded_file.name}'
        # if st.button('开始检测'):
        #     detect(opt)
        #     with st.spinner(text='Preparing Videos'):
        #             for vid in os.listdir(get_detection_folder()):
        #                 st.video(str(Path(f'{get_detection_folder()}') / vid))
        #             st.balloons()
        else:
            is_valid = False

    if is_valid:
        print('valid')
        button = st.button('开始检测')
        if button:

            detect(opt)

            if source_index == 0:
                with st.spinner(text='Preparing Images'):
                    for img in os.listdir(get_detection_folder()):
                        st.image(str(Path(f'{get_detection_folder()}') / img))

                    st.balloons()
            else:
                with st.spinner(text='Preparing Videos'):
                    for vid in os.listdir(get_detection_folder()):
                        st.video(str(Path(f'{get_detection_folder()}') / vid))

                    st.balloons()
