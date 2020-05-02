import sys
import argparse
from yolo import YOLO, detect_video
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageFont,ImageDraw,ImageTk
import numpy as np
from timeit import default_timer as timer
import time
def detect_img(yolo):
    while True:
        img = input('Input image filename:')
        try:
            image = Image.open('./'+img)
        except:
            print('Open Error! Try again!')
            break
        else:
            r_image = yolo.detect_image(image)
            r_image.show()
    yolo.close_session()

FLAGS = None
class App:
    def __init__(self,master,yolo):
        self.master=master
        self.initWidgets()
        self.yolo=yolo
        
    def initWidgets(self):
        topF=Frame(self.master)
        topF.pack(side=TOP,fill=BOTH)
        self.cv=Canvas(topF,background='white',width=450,height=450)
        self.cv.pack(side=LEFT,fill=BOTH,expand=YES)
        
        
        
        
        ttk.Button(topF,text='打开图片文件',command=self.open_file).pack(side=RIGHT,fill=Y,expand=YES,anchor=CENTER)
        ttk.Button(topF,text='打开MP4视频文件',command=self.open_video).pack(side=RIGHT,fill=Y,expand=YES,anchor=CENTER)
        self.yolo_result=StringVar()
        topF3=Frame(self.master)
        topF3.pack(side=BOTTOM,fill=BOTH)
        ttk.Label(topF3,text='检测结果',padding=20).pack(side=TOP,fill=X,expand=YES)
        self.lb=Listbox(topF3,listvariable=self.yolo_result,selectmode='single')
        self.lb.pack(side=BOTTOM,fill=X,expand=YES)
        self.lb.bind("<ButtonRelease-1>",self.click)
        
        
        
        self.yolo_result_store=[]
        self.class_names=[]
        self.colors=[]
        
        
    def click(self,event):
        index_temp=self.lb.curselection()
        index_temp2=index_temp[0]
        yolo_result_click=self.yolo_result_store[index_temp2]
        wdawdaw=self.yolo_result_store
        predicted_class_click=yolo_result_click[0]
        score_click=yolo_result_click[1]
        box_click=yolo_result_click[2]
        thickness_click=yolo_result_click[3]
        c_click=yolo_result_click[4]
        
        
        
        image_click=self.image.crop()
        predicted_class=predicted_class_click
        box=box_click
        score=score_click
        
        label='{} {:.2f}'.format(predicted_class,score)
        draw=ImageDraw.Draw(image_click)
        label_size=draw.textsize(label,self.font)
        
        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(self.image.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(self.image.size[0], np.floor(right + 0.5).astype('int32'))

        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
        for i in range(thickness_click):
            draw.rectangle(
                [left + i, top + i, right - i, bottom - i],
                outline=self.colors[c_click])
        draw.rectangle(
            [tuple(text_origin), tuple(text_origin + label_size)],
            fill=self.colors[c_click])
        draw.text(text_origin, label, fill=(0, 0, 0), font=self.font)
        del draw
        image_click=image_click.resize((416,416))
        size0=image_click.size[0]
        size1=image_click.size[1]
        self.cv.bm=ImageTk.PhotoImage(image_click)
        self.cv.create_image(size0/2+17,size1/2+17,image=self.cv.bm)
    def open_file(self):
        self.yolo_result.set('')
        self.yolo_result_store.clear()
        img=filedialog.askopenfilename(title='打开单个文件',filetypes=[("JPEG图像","*.jpg"),("JPEG图像","*.jpeg"),('PNG图像','*.png')],initialdir='F:/')
        print(img)
        print(type(img))
        try:
            self.image=Image.open(img)
        except:    
            print('Open Error! Try again!')
            
        else:
           r_image,out_boxes,out_scores,out_classes,self.font,thickness,calculate_time,self.class_names,self.colors = self.yolo.detect_image(self.image) 
        image_main=self.image.crop()
        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image_main)
            label_size = draw.textsize(label, self.font)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(self.image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(self.image.size[0], np.floor(right + 0.5).astype('int32'))
            print(label, (left, top), (right, bottom))

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=self.colors[c])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=self.colors[c])
            draw.text(text_origin, label, fill=(0, 0, 0), font=self.font)
            del draw
            
            self.yolo_result_store.append((predicted_class,score,box,thickness,c))
            
            self.lb.insert(END,str(predicted_class)+' -->'+'    score:   '+str(score)+'    position:    '+str(box))
        image_main=image_main.resize((416,416))
        size0=image_main.size[0]
        size1=image_main.size[1]
        self.cv.bm=ImageTk.PhotoImage(image_main)
        self.cv.create_image(size0/2+17,size1/2+17,image=self.cv.bm)
        
    def open_video(self):
        
        video_path=filedialog.askopenfilename(title='打开单个文件',filetypes=[("视频文件","*.mp4")],initialdir='F:/')

        detect_video(self.yolo,video_path)            
        
    def detect_img(self):
        while True:
            img=input('Input image filename:')
            try:
                image=Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = yolo.detect_image(image)
                r_image.show()
            #self.yolo.close_session()    
            
if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', required=False, type=str, default="dayu.avi",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()
    #if FLAGS.image:
    root=Tk()
    root.title('YOLO图形识别')
        
        
        
        
        
    App_inst=App(root,YOLO(**vars(FLAGS)))
    root.resizable(width=True,height=True)
    root.mainloop()
