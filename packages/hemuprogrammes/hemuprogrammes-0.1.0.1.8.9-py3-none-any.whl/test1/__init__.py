from tkinter import *
import tkinter.filedialog as fd
from subprocess import *
from threading import *
class test:
    def te(self):    
        cha1='';cha2='';fnam='';fpla='';iconam='';dis1=''
        def pyfile():
            global cha1;global fnam;global fpla;
            ch=fd.askopenfile(title='Select file',filetypes=[('Python Files','*.py')])
            if(ch!=None):
                f1b1['text']='SELECTED'
                f1l5.place_forget()
                f1l1.place_forget()
                f1l2.place_forget()
                f1l3.place_forget()
                f1l4.place_forget()
                ch=str(ch);b=ch.find('=');d=ch.find(" mode='r'");ch=ch[b+1:d];
                cha1=ch
                a=cha1
                c=a.count('/')
                b=0
                for i in range(len(a)):
                    if(a[i]=='/'):
                        b+=1
                        if(b==c):
                            fnam=a[i+1:len(a)-1]
                            fpla=a[1:i+1]
        def icofile():
            global cha2;global iconam
            ch=fd.askopenfile(title='Select file',filetypes=[('ICON Files','*.ico')])
            if(ch!=None):
                ch=str(ch);b=ch.find('=');d=ch.find(" mode='r'");ch=ch[b+1:d]
                cha2=ch
                f1l5.place_forget()
                f1l1.place_forget()
                f1l2.place_forget()
                f1l3.place_forget()
                f1l4.place_forget()
                f1b2['text']='SELECTED'
                a=cha2
                c=a.count('/')
                b=0
                for i in range(len(a)):
                    if(a[i]=='/'):
                        b+=1
                        if(b==c):
                            iconam=a[i+1:len(a)-1]
        def conv():
            if(fnam!=''):
                f1l4.place_forget()
                f1l1.place_forget()
                f1l2.place_forget()
                f1l5.place_forget()
                f1l3.place(x=130,y=340)
                Thread(target=conv1).start()
            else:
                f1l4.place_forget()
                f1l1.place_forget()
                f1l2.place_forget()
                f1l3.place_forget()
                f1l5.place(x=50,y=340)
                
        def conv1():
            global cha1;global fnam;global fpla;global iconam;global dis1
            dis=fpla[:2]
            if(iconam!=''):
                cmd=dis+' & cd '+fpla+' & pyinstaller --onefile -w -i '+iconam+' '+fnam
            else:
                cmd=dis+' & cd '+fpla+' & pyinstaller --onefile -w '+fnam
            te=Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
            out,err=te.communicate()
            out=out.decode('utf-8')
            err=err.decode('utf-8')
            dis1=out+'\n'+err
            te1=dis1.find('Building EXE from EXE-00.toc completed successfully.')
            if(te1!=-1):
                f1l3.place_forget()
                f1l2.place_forget()
                f1l5.place_forget()
                f1l1.place(x=60,y=380)
                f1l4.place(x=30,y=500)
                f1b1['text']=' SELECT '
                f1b2['text']=' SELECT '
            else:
                f1l5.place_forget()
                f1l3.place_forget()
                f1l1.place_forget()
                f1l2.place(x=60,y=380)
                f1l4.place(x=30,y=500)
                f1b1['text']=' SELECT '
                f1b2['text']=' SELECT '
        root=Tk()
        root.title('PytoEXE')
        root.minsize(width=360,height=580)
        root.maxsize(width=360,height=580)
        #frame1
        frame1=Frame(root,width=360,height=580,bg='black')
        frame1.pack()
        Label(frame1,text='PY TO EXE',bg='black',fg='yellow',font=('Arieal',18,'bold')).place(x=103,y=5)
        Label(frame1,text='Requires Internet for First Conversion only',bg='black',fg='red',font=('Arieal',10,'bold')).place(x=45,y=40)
        Label(frame1,text='Please Insert Your Python File',bg='black',fg='white',font=('Arieal',14,'bold')).place(x=35,y=60)
        f1b1=Button(frame1,text=' SELECT ',command=pyfile,font=('Arieal',10,'bold'))
        f1b1.place(x=130,y=90)
        Label(frame1,text='Add Icon for your Exe file',bg='black',fg='white',font=('Arieal',15,'bold')).place(x=55,y=130)
        f1b2=Button(frame1,text=' SELECT ',command=icofile,font=('Arieal',10,'bold'))
        f1b2.place(x=130,y=170)
        Label(frame1,text='* Icon Image in ico formate',bg='black',fg='red',font=('Arieal',13,'bold')).place(x=65,y=210)
        Button(frame1,text='CONVERT',command=conv,font=('Arieal',10,'bold')).place(x=130,y=250)
        Label(frame1,text='* Icon and python file must be in\n same folder',bg='black',fg='red',font=('Arieal',11,'bold')).place(x=65,y=290)
        f1l1=Label(frame1,text='Py File is Succussfully conveted\ncheck at dist folder near your\nPython File',bg='black',fg='blue',font=('Arieal',12,'bold'))
        f1l2=Label(frame1,text='Py File is Not Converted Succussfully',bg='black',fg='blue',font=('Arieal',12,'bold'))
        f1l3=Label(frame1,text='Converting...',bg='black',fg='white',font=('Arieal',12,'bold'))
        f1l4=Label(frame1,text='***THANK YOU FOR USING OUR APP***',bg='black',fg='white',font=('Arieal',12,'bold'))
        f1l5=Label(frame1,text='Please Select Python File',bg='black',fg='red',font=('Arieal',16,'bold'))

        root.mainloop()

#a=test()
#a.te()
