''''
作者：romtance
时间:2022年11月26日
'''
import tkinter as tk

import statsmodels.api as sm
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('seaborn')
import pmdarima as pm
from tkinter.messagebox import *
import logging


def o_f_plot(x,x_,x_f=[],x__=[]):
    f_plot.clear()
    f_plot.plot(x,'k-.',alpha=0.8)
    f_plot.plot(x_,'r-*')
    print(np.append(x__[-1],x_f))
    le = ['$Origin$', '$GM(1,1) predict$']
   
    if len(x_f)>0:
        le.append(f'Feture {len(x_f)} Days Predict')
        
        f_plot.plot(range(len(x_)-1,len(x_)+len(x_f)),np.append(x__[-1],x_f),'g-')
        
    if len(x__)==0:
        f_plot.set_title('GM(1,1) Model')
        
        f_plot.legend(le)
    else:
        f_plot.plot(x__, 'b-',alpha=0.8)
        f_plot.set_title('ARIMA+GM(1,1) Model')
        le.append('$ARIMA+GM(1,1)$')
        f_plot.legend(le)
        
    f_plot.set_xlabel('Times')
    f_plot.set_ylabel('Values')
    if len(x_)<=5:
        f_plot.set_xticks(range(0, len(x_)+1, 1))
    else:
        f_plot.set_xticks(range(0, len(x_)+1, int(len(x_)/5)))
    canvas.draw()


def GM(x,p=0):
    ## 正规方程求解参数
    n = len(x)
    ago = np.cumsum(x)
    z = (ago[0:-1]+ago[1:])/2
    y = x[1:]
    B = np.c_[-z,np.ones((n-1,1))]
    theta = np.array((np.mat(B.T@B)).I@B.T@y)
    a = np.array(theta)[0][0]
    b = np.array(theta)[0][1]
    ## 得出事件响应式
    x_1 = (x[0]-b/a)*np.exp(-a*np.arange(0,n+p))+b/a
    #累减还原
    x_hat = np.append(x[0],np.diff(x_1))
    x_train = x_hat[:n]
    x_future = x_hat[n:]
    
    logger.info(f'GM(1,1)模型得到参数为:({round(a,4)},{round(b,4)})')
    
    cond['text'] = f'GM(1,1)模型得到参数为:({round(a,4)},{round(b,4)})'

    #返回结果
    return theta,x_train,x_future

def ARIMA(x,beta,p=0):
    x = np.array(x)
    theta, x_train, x_future = GM(x,p)
    print(x,x_train)
    error = x-x_train
    n = len(x)
    error = pd.DataFrame(error,columns=['err'])
    model = sm.tsa.ARIMA(error, order=beta).fit()
    x_f = []
    if p>0:
        x_f = np.array(x_future) + model.forecast(p).values
        print(x_f)
    x__ = x_train+model.fittedvalues.values
    o_f_plot(x, x_train,x_f,x__)
    
    mse1 = np.average(np.abs(x-x_train)/x)
    mse2 = np.average(np.abs(x-x__)/x)
    cond['text'] += '\n'+'GM(1,1)模型平均相对模拟百分误差：'+str(round(mse1,5))+'\n'+'ARIMA模型平均相对模拟百分误差：'+str(round(mse2,5))
                    
    logger.info('ARIMA模型')
    logger.info('GM(1,1)模型拟合数据为：')
    logger.info(x_train)
    logger.info('GM(1,1)+ARIMA模型拟合数据为:')
    logger.info(x__)
    
    logger.info(f'未来{p}天预测数据为')
    logger.info(x_f)
    logger.info('平均相对模拟百分误差：'+str(mse2)+'%')
    logger.info('++++++++OVER!!++++++++++++')

    
def auto_ARIMA(x,p=0):
    x = np.array(x)
    theta, x_train, x_future = GM(x,p)
    print(x_train.tolist())
    error = x-x_train
    n = len(x)
    error = pd.DataFrame(error,columns=['err'])

    model = pm.auto_arima(error,start_p=2, start_q=2, max_p=9, max_q=6, max_d=3,max_order=None,
                         seasonal=False, m=1, test='adf', trace=False,
                         error_action='ignore',  # don't want to know if an order does not work
                         suppress_warnings=True,  # don't want convergence warnings
                         stepwise=True, information_criterion='bic', njob=-1)
    cond['text']+='\nARIMA模型参数为:'+str(model)
    beta = str(model)[7:12].split(',')[:3]
    beta = [int(i) for i in beta]
    print(beta)
    x_f=[]
    model = sm.tsa.ARIMA(error, order=beta).fit()
    if p>0:
        x_f = np.array(x_future) + model.forecast(p).values
        print(x_f)
    x__ = x_train+model.fittedvalues.values
    o_f_plot(x, x_train,x_f,x__)

    mse1 = np.average(np.abs(x-x_train)/x)
    mse2 = np.average(np.abs(x-x__)/x)
    cond['text'] += '\n'+'GM(1,1)模型平均相对模拟百分误差：'+str(round(mse1,5))+'\n'+'ARIMA模型平均相对模拟百分误差：'+str(round(mse2,5))
    
    logger.info('Auto ARIMA模型')
    logger.info('GM(1,1)的拟合数据为：')
    logger.info(x_train)
    logger.info('GM(1,1)+Auto ARIMA模型拟合数据为:')
    logger.info(x__)
    logger.info(f'未来{p}天预测数据为')
    logger.info(x_f)
    logger.info('平均相对模拟百分误差：'+str(mse2)+'%')
    logger.info('++++++++OVER!!++++++++++++')

def which_model(w,X,beta,p):
    if w==0:
        print(beta)
        ARIMA(X,beta,p)
    else:
        auto_ARIMA(X,p)
    logger.info('++++++++OVER!!++++++++++++')
def cmx1():
	mx1 = showinfo(title='消息提示框',
                       message='Author:曾一鸣 romtance@qq.com\n\n1.点击上传数据\n2.选择ARIMA参数定义方式:\n  a.自适应最优\n  b.输入p,d,q\n3.开始运行')

def upload_file():
    data.set('')
    selectFile = tk.filedialog.askopenfilename()
    input1.insert(0, selectFile)
    file1 = input1.get()
    df = pd.read_excel(file1)
    file1 = df.iloc[:,0].values
    data.set(','.join(map(str,file1.tolist())))
    logger.info('输出原始数据为：')
    logger.info(data.get())
    print('上传的数据为: {}'.format(data.get()))


def window():
    win = tk.Tk()
    global data,input1,logger,cond,f_plot,canvas
    myfont = tkFont.Font(family='华文行楷', size=30, \
                         weight=tkFont.BOLD, slant=tkFont.ITALIC)

    logging.basicConfig(level = logging.INFO,
                         filename = '输出日志.txt',
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()
    logger.info('=====欢迎来到基于ARIMA改进GM(1,1)模型软件2.0==========\n=======================')

    win.title('基于ARIMA改进GM(1,1)模型软件2.0')
    #win.iconphoto(False, tk.PhotoImage(file='need/1.png'))
    win.columnconfigure(0,weight = 1)
    win.rowconfigure(0,weight = 1)
    win.columnconfigure(1,weight = 1)
    win.rowconfigure(1,weight = 1)

    frm = tk.Frame(win)
    frm1 = tk.Frame(win)
    frm2 = tk.Frame(win)

    frm.grid(row=0,columnspan=2)
    frm1.grid(row=1,column=0)
    frm2.grid(row=1,column=1)

    myfont = tkFont.Font(family='华文行楷', size=20, \
                         weight=tkFont.BOLD, slant=tkFont.ITALIC)

    label1 = tk.Label(frm, text='欢迎来到基于ARIMA改进GM(1,1)模型软件',font = myfont,fg = '#000000')
    label1.grid(row=0,columnspan=2, padx=10, pady=10)

    w = tk.IntVar()
    data = tk.StringVar()
    data.set('如:1.2,3.4...\n\n')

    input1 = tk.Entry(frm1,textvariable =data,width=10)

    btn = tk.Button(frm1, text='点击上传数据文件(或直接右侧输入数据)', command=upload_file,borderwidth = 6,relief="ridge",)
    btn.grid(row=0, column=0, ipadx='3', ipady='3', padx='10', pady='20')


    input1.grid(row=0,column=1,rowspan=2, padx=5, pady=5,sticky='WE')

    check1 = tk.Checkbutton(frm1,text='智能调参的ARIMA',bg='pink',variable = w, \
                     onvalue = 1, offvalue = 0)
    check2 = tk.Checkbutton(frm1,text='手动定参的ARIMA',bg='green',variable = w, \
                     onvalue = 0, offvalue = 1,)

    check1.grid(row=2,column=0, padx=5, pady=5)
    check2.grid(row=2,column=1, padx=5, pady=5)

    t = tk.IntVar()
    t.set(0)
    beta = tk.StringVar()
    beta.set('2,2,1')
    label2 = tk.Label(frm1,text='输入ARIMA(p,d,q)\n的参数:p,d,q:',borderwidth = 3,relief="ridge",)
    label2.grid(row=3,column=0)
    input2 = tk.Entry(frm1,textvariable=beta)
    input2.grid(row=3,column=1)

    label3 = tk.Label(frm1,text='Days for Predict',borderwidth = 3,relief="ridge")
    input3 = tk.Entry(frm1,textvariable=t)
    label3.grid(row=4,column=0)
    input3.grid(row=4,column=1)


    cond = tk.Label(frm1,text='欢迎您的使用！\n仅能选择一项进行预测。')
    cond.grid(row=5,columnspan=2)

    butt = tk.Button(frm1,text='开始运行',command=lambda:which_model(w.get(),eval('[' + data.get() + ']'),eval('[' + beta.get() + ']'),t.get()))

    butt.grid(row=7,columnspan=2, padx='10', pady='10')
    tk.Button(frm1, text='Help', command=cmx1,fg='black',bg='yellow').grid(row=6,columnspan=2, padx='10', pady='10')
    f = Figure(figsize=(5, 4), dpi=100)
    f_plot = f.add_subplot(111)

    canvas = FigureCanvasTkAgg(f, frm2)
    canvas.draw()
    canvas.get_tk_widget().pack()
    win.columnconfigure(0,weight = 1)
    win.rowconfigure(0,weight = 1)
    win.columnconfigure(1,weight = 1)
    win.rowconfigure(1,weight = 1)
    frm1.columnconfigure(0,weight = 1)
    frm1.rowconfigure(0,weight = 1)
    frm1.columnconfigure(1,weight = 1)
    frm1.rowconfigure(1,weight = 1)
    win.mainloop()


