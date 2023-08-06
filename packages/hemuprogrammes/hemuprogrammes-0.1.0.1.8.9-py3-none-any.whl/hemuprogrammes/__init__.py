from math import *
import tkinter.messagebox as msb
from random import *
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from subprocess import *
from threading import *
from tkinter import *
from pygame import *
from pickle import *
from mutagen.mp3 import MP3

class Hemu:
    def propose(self):
        root=Tk()
        root.title('')
        root.minsize(width=240,height=240)
        root.maxsize(width=240,height=240)
        root.resizable(width=False,height=False)
        def del1():
            pass
        root.protocol("WM_DELETE_WINDOW",del1)
        def screen1_2():
            frame1.pack_forget()
            frame2.pack()
            root.protocol("WM_DELETE_WINDOW",root.destroy)
        def change(eve):
            l=list(range(130,201,20));l1=list(range(100,201,20))
            x1=choice(l)
            y1=choice(l1)
            f1b1.place_forget()
            f1b2.place(x=x1,y=y1)
            f1b2.bind('<Enter>',cha)
            f1b2.bind('<Button-1>',cha)
        def cha(e):
            l=list(range(150,201,10));l1=list(range(100,201,10))
            x1=choice(l)
            y1=choice(l1)
            f1b1.place_forget()
            f1b2.place(x=x1,y=y1)
            f1b2.bind('<Enter>',change)
            f1b2.bind('<Button-1>',change)
        frame1=Frame(root,bg='black')
        frame1.config(width=240,height=360)
        frame1.pack()
        Label(frame1,text='Do u Love Me?',bg='black',fg='red',font=('Areial',25,'bold')).place(x=3,y=30)
        f1b1=Button(frame1,width=5,text='No',fg='black',font=('Areial',8,'bold'))
        f1b1.bind('<Enter>',change)
        f1b1.place(x=180,y=180)
        f1b2=Button(frame1,width=5,text='NO',fg='black',font=('Areial',8,'bold'))
        f1b2.bind('<Enter>',cha)
        f1b3=Button(frame1,width=5,text='Yes',fg='green',font=('Areial',8,'bold'),command=screen1_2)
        f1b3.place(x=35,y=180)
        frame2=Frame(root,bg='black')
        frame2.config(width=240,height=240)
        Label(frame2,text='I Love U\nToo',bg='black',fg='blue',font=('Areial',25,'bold')).place(x=55,y=80)
        root.mainloop()

    def tictactoe(self):
        self.a=1;self.c=0;self.pla1r1c1=0;self.pla1r1c2=0;self.pla1r1c3=0;self.pla1r2c1=0;self.pla1r2c2=0;self.pla1r2c3=0;self.pla1r3c1=0;self.pla1r3c2=0;self.pla1r3c3=0;
        self.pla2r1c1=0;self.pla2r1c2=0;self.pla2r1c3=0;self.pla2r2c1=0;self.pla2r2c2=0;self.pla2r2c3=0;self.pla2r3c1=0;self.pla2r3c2=0;self.pla2r3c3=0;
        self.l=''
        def start(num):
            b=self.l.find(str(num))
            self.l=self.l+str(num)
            f3l2['text']=str(f2e2.get());f3l1['text']=str(f2e1.get())
            self.c+=1
            if(b==-1):
                if(self.c<=9):
                    if(self.a==0):
                        f3l2.place_forget()
                        f3l1.place(x=30,y=310)
                        self.a=1
                        if(num==1):
                            f3b1['text']='X'
                            f3b1['fg']='blue'
                            self.pla2r1c1=1
                        elif(num==2):
                            f3b2['text']='X'
                            f3b2['fg']='blue'
                            self.pla2r1c2=1
                        elif(num==3):
                            f3b3['text']='X'
                            f3b3['fg']='blue'
                            self.pla2r1c3=1
                        elif(num==4):
                            f3b4['text']='X'
                            f3b4['fg']='blue'
                            self.pla2r2c1=1
                        elif(num==5):
                            f3b5['text']='X'
                            f3b5['fg']='blue'
                            self.pla2r2c2=1
                        elif(num==6):
                            f3b6['text']='X'
                            f3b6['fg']='blue'
                            self.pla2r2c3=1
                        elif(num==7):
                            f3b7['text']='X'
                            f3b7['fg']='blue'
                            self.pla2r3c1=1
                        elif(num==8):
                            f3b8['text']='X'
                            f3b8['fg']='blue'
                            self.pla2r3c2=1
                        elif(num==9):
                            f3b9['text']='X'
                            f3b9['fg']='blue'
                            self.pla2r3c3=1
                    else:
                        f3l1.place_forget()
                        f3l2.place(x=30,y=310)
                        if(num==1):
                            f3b1['text']='O'
                            f3b1['fg']='green'
                            self.pla1r1c1=1
                        elif(num==2):
                            f3b2['text']='O'
                            f3b2['fg']='green'
                            self.pla1r1c2=1
                        elif(num==3):
                            f3b3['text']='O'
                            f3b3['fg']='green'
                            self.pla1r1c3=1
                        elif(num==4):
                            f3b4['text']='O'
                            f3b4['fg']='green'
                            self.pla1r2c1=1
                        elif(num==5):
                            f3b5['text']='O'
                            f3b5['fg']='green'
                            self.pla1r2c2=1
                        elif(num==6):
                            f3b6['text']='O'
                            f3b6['fg']='green'
                            pla1r2c3=1
                        elif(num==7):
                            f3b7['text']='O'
                            f3b7['fg']='green'
                            self.pla1r3c1=1
                        elif(num==8):
                            f3b8['text']='O'
                            f3b8['fg']='green'
                            self.pla1r3c2=1
                        elif(num==9):
                            f3b9['text']='O'
                            f3b9['fg']='green'
                            self.pla1r3c3=1
                        self.a=0
                if(self.c==9):
                    win()
            else:
                self.c-=1
            
        def win():
            wc1=0;wc2=0
            if(self.pla1r1c1==1 and self.pla1r1c2==1 and self.pla1r1c3==1):
                wc1+=1
            elif(self.pla1r2c1==1 and self.pla1r2c2==1 and self.pla1r2c3==1):
                wc1+=1
            elif(self.pla1r3c1==1 and self.pla1r3c2==1 and self.pla1r3c3==1):
                wc1+=1
            elif(self.pla1r1c1==1 and self.pla1r2c1==1 and self.pla1r3c1==1):
                wc1+=1
            elif(self.pla1r1c2==1 and self.pla1r2c2==1 and self.pla1r3c2==1):
                wc1+=1
            elif(self.pla1r1c3==1 and self.pla1r2c3==1 and self.pla1r3c3==1):
                wc1+=1
            elif(self.pla1r1c1==1 and self.pla1r2c2==1 and self.pla1r3c3==1):
                wc1+=1
            elif(self.pla1r1c3==1 and self.pla1r2c2==1 and self.pla1r3c1==1):
                wc1+=1
            if(self.pla2r1c1==1 and self.pla2r1c2==1 and self.pla2r1c3==1):
                wc2+=1
            elif(self.pla2r2c1==1 and self.pla2r2c2==1 and self.pla2r2c3==1):
                wc2+=1
            elif(self.pla2r3c1==1 and self.pla2r3c2==1 and self.pla2r3c3==1):
                wc2+=1
            elif(self.pla2r1c1==1 and self.pla2r2c1==1 and self.pla2r3c1==1):
                wc2+=1
            elif(self.pla2r1c2==1 and self.pla2r2c2==1 and self.pla2r3c2==1):
                wc2+=1
            elif(self.pla2r1c3==1 and self.pla2r2c3==1 and self.pla2r3c3==1):
                wc2+=1
            elif(self.pla2r1c1==1 and self.pla2r2c2==1 and self.pla2r3c3==1):
                wc2+=1
            elif(self.pla2r1c3==1 and self.pla2r2c2==1 and self.pla2r3c1==1):
                wc2+=1
            if(wc1>wc2):
                screen3_4()
                f4l1['text']=str(f2e1.get())+' WON'
            elif(wc1<wc2):
                screen3_4()
                f4l1['text']=str(f2e2.get())+' WON'
            else:
                screen3_4()
                f4l1['text']='       DRAW'
        def cha(e):
            a=f2e1.get();b=f2e2.get()
            if(a=='' or b==''):
                f2b1.place_forget()
                f2b3.place_forget()
                f2b2.place(x=15,y=300)
                f2b2.bind('<Enter>',cha1)
            else:
                f2b1.place_forget()
                f2b2.place_forget()
                f2b3.place(x=130,y=300)

        def cha1(e):
            a=f2e1.get();b=f2e2.get()
            if(a=='' or b==''):
                f2b1.place_forget()
                f2b3.place_forget()
                f2b2.place(x=190,y=300)
                f2b2.bind('<Enter>',cha)
            else:
                f2b1.place_forget()
                f2b2.place_forget()
                f2b3.place(x=130,y=300)
        root=Tk()
        root.minsize(width=300,height=360)
        root.maxsize(width=300,height=360)
        root.title('Tic Tac Toe')
        def screen1_2():
            frame1.pack_forget()
            frame2.pack(fill=BOTH,expand=1)

        def screen2_3():
            frame2.pack_forget()
            frame3.pack(fill=BOTH,expand=1)
            f3l1['text']=str(f2e1.get())
        def screen3_4():
            frame3.pack_forget()
            frame4.pack(fill=BOTH,expand=1)
        #frame1
        frame1=Frame(root,bg='blue')
        frame1.pack(fill='both',expand=1)
        Label(frame1,text='WELCOME  TO\nTIC TAC TOE\nGAME',fg='yellow',font=('Arieal',20,'bold'),bg='blue').place(x=50,y=100)
        Button(frame1,text='NEXT',font=('Arieal',10,'bold'),command=screen1_2).place(x=130,y=300)
        #frame2
        frame2=Frame(root,bg='blue')
        Label(frame2,text='Enter Player 1 Name',font=('Arieal',18,'bold'),bg='blue').place(x=30,y=80)
        f2e1=Entry(frame2,bd=2,width=15,font=('Arieal',14,'bold'))
        f2e1.place(x=60,y=130)
        Label(frame2,text='Enter Player 2 Name',font=('Arieal',18,'bold'),bg='blue').place(x=30,y=180)
        f2e2=Entry(frame2,bd=2,width=15,font=('Arieal',14,'bold'))
        f2e2.place(x=60,y=230)
        f2b1=Button(frame2,text='NEXT',font=('Arieal',10,'bold'))
        f2b1.place(x=200,y=300)
        f2b2=Button(frame2,text='Fill Both Entries',fg='red',font=('Arieal',9,'bold'))
        f2b3=Button(frame2,text='NEXT',fg='green',font=('Arieal',10,'bold'),command=screen2_3)
        f2b1.bind('<Enter>',cha)
        f2b3.bind('<Enter>',cha)
        #frame3
        frame3=Frame(root,bg='blue')
        can=Canvas(frame3,width=260,height=300,bg='red')
        can.pack(pady=2)
        can.create_rectangle(0,97,260,100,fill='black')
        can.create_rectangle(0,197,260,200,fill='black')
        can.create_rectangle(83,0,85,300,fill='black')
        can.create_rectangle(175,0,177,300,fill='black')
        f3b1=Button(can,text='   ',bg='red',bd=0,command=lambda:start(1),font=('Arieal',34,'bold'))
        f3b1.place(x=6,y=6)
        f3b2=Button(can,text='   ',bd=0,bg='red',command=lambda:start(2),font=('Arieal',34,'bold'))
        f3b2.place(x=94,y=6)
        f3b3=Button(can,text='   ',bd=0,bg='red',command=lambda:start(3),font=('Arieal',34,'bold'))
        f3b3.place(x=184,y=6)
        f3b4=Button(can,text='   ',bd=0,bg='red',command=lambda:start(4),font=('Arieal',34,'bold'))
        f3b4.place(x=6,y=106)
        f3b5=Button(can,text='   ',bd=0,bg='red',command=lambda:start(5),font=('Arieal',34,'bold'))
        f3b5.place(x=94,y=106)
        f3b6=Button(can,text='   ',bd=0,bg='red',command=lambda:start(6),font=('Arieal',34,'bold'))
        f3b6.place(x=184,y=106)
        f3b7=Button(can,text='   ',bd=0,bg='red',command=lambda:start(7),font=('Arieal',34,'bold'))
        f3b7.place(x=6,y=206)
        f3b8=Button(can,text='   ',bd=0,bg='red',command=lambda:start(8),font=('Arieal',34,'bold'))
        f3b8.place(x=94,y=206)
        f3b9=Button(can,text='   ',bd=0,bg='red',command=lambda:start(9),font=('Arieal',34,'bold'))
        f3b9.place(x=184,y=206)
        f3l1=Label(frame3,text='Player1',font=('Arieal',18,'bold'),bg='blue')
        f3l1.place(x=30,y=310)
        f3l2=Label(frame3,text='Player2',font=('Arieal',18,'bold'),bg='blue')
        #frame4
        frame4=Frame(root,bg='blue')
        Label(frame4,text='GAME OVER',fg='red',font=('Arieal',18,'bold'),bg='blue').place(x=70,y=70)
        f4l1=Label(frame4,text='',fg='yellow',font=('Arieal',18,'bold'),bg='blue')
        f4l1.place(x=50,y=130)
        root.mainloop()

    def simple_cal_gui(self):
        self.tx=''
        def press(ele):
            if(ele!='='):
                self.tx=self.tx+ele
                v.set(self.tx)
            elif(ele=='='):
                self.tx=self.tx.replace('x','*')
                p=eval(self.tx)
                v.set(p)
                self.tx=str(p)
        def clear():
            self.tx=''
            v.set(self.tx)
        calc=Tk()
        calc.title('Simple Calculator')
        calc.minsize(width=240,height=355)
        calc.maxsize(width=240,height=355)
        calc.config(bg='Black')
        v=StringVar()
        e=Entry(calc,width=240,state='readonly',textvariable=v).pack()
        b1=Button(calc,text='1',width=7,height=5,command=lambda:press('1')).place(x=1,y=22)
        b2=Button(calc,text=2,width=7,height=5,command=lambda:press('2')).place(x=61,y=22)
        b3=Button(calc,text=3,width=7,height=5,command=lambda:press('3')).place(x=121,y=22)
        b4=Button(calc,text=4,width=7,height=5,command=lambda:press('4')).place(x=1,y=109)
        b5=Button(calc,text=5,width=7,height=5,command=lambda:press('5')).place(x=61,y=109)
        b6=Button(calc,text=6,width=7,height=5,command=lambda:press('6')).place(x=121,y=109)
        b7=Button(calc,text=7,width=7,height=5,command=lambda:press('7')).place(x=1,y=196)
        b8=Button(calc,text=8,width=7,height=5,command=lambda:press('8')).place(x=61,y=196)
        b9=Button(calc,text=9,width=7,height=5,command=lambda:press('9')).place(x=121,y=196)
        b0=Button(calc,text=0,width=7,height=4,command=lambda:press('0')).place(x=61,y=283)
        a=Button(calc,text='+',width=7,height=3,command=lambda:press('+')).place(x=180,y=80)
        s=Button(calc,text='-',width=7,height=3,command=lambda:press('-')).place(x=180,y=137)
        m=Button(calc,text='\u00D7',width=7,height=3,command=lambda:press('x')).place(x=180,y=194)
        d=Button(calc,text='/',width=7,height=6,command=lambda:press('/')).place(x=180,y=252)
        g=Button(calc,text='=',width=7,height=4,command=lambda:press('=')).place(x=121,y=283)
        c=Button(calc,text='clear',width=7,height=3,command=clear).place(x=180,y=22)
        d0=Button(calc,text='.',width=7,height=4,command=lambda:press('.')).place(x=1,y=283)
        calc.mainloop()


    def virtualatm(self):
        print('Type card at Insert Card\nPIN:2022')
        self.amt=700000;self.ca=0;self.da=0;self.res=0
        root=Tk()
        root.title('Virtual ATM APP')
        root.geometry('245x360')
        root.minsize(width=245,height=360)
        root.maxsize(width=245,height=360)
        def screen1_2():
            frame1.pack_forget()
            frame2.pack()
            
        def screen2_1():
            frame2.pack_forget()
            frame1.pack()
            
        def screen2_3():
            banknam()
            frame2.pack_forget()
            frame3.pack()

        def screen3_4():
            frame3.pack_forget()
            frame4.pack()

        def screen4_5():
            frame4.pack_forget()
            frame5.pack()

        def screen5_6():
            frame5.pack_forget()
            frame6.pack()

        def screen5_7():
            frame5.pack_forget()
            frame7.pack()

        def screen5_8():
            frame5.pack_forget()
            frame8.pack()

        def screen5_9():
            frame5.pack_forget()
            frame9.pack()

        def screen6_10():
            global amt
            global res
            dra=f6e1.get();
            test=dra.isdigit()
            if(test==True):
                userbank=f2e1.get();userbank=userbank.upper();userbank=userbank.replace(' BANK','')
                if(userbank=='SBI' or userbank=='ICICI' or userbank=='UNION'):
                    dep=int(dra)
                    res=self.amt+dep
                    frame6.pack_forget()
                    frame10.pack()
                    f9l10=Label(frame9,text=f'\u20B9 %.2f /-'%(self.amt+dep),fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
                    f9l10.place(x=30,y=150)
                else:
                    dep=int(dra)
                    res=self.amt+dep
                    frame6.pack_forget()
                    frame10.pack()
                    f9l10=Label(frame9,text=f'\u20B9 %.2f /-'%(self.amt+(dep-(dep*0.03))),fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
                    f9l10.place(x=30,y=150)
                    
            else:
                f6l13=Label(frame6,text='Please Enter Amount',fg='red',bg='#888D8F',font=('Arial',8,'bold')).place(x=55,y=225)    
        def screen7_10():
            global amt
            global res
            dra=f7e1.get();
            test=dra.isdigit()
            if(test==True):
                dra=int(dra);userbank=f2e1.get();userbank=userbank.upper();userbank=userbank.replace(' BANK','')
                if(userbank=='SBI' or userbank=='ICICI' or userbank=='UNION'):
                    if(dra<self.amt):
                        res=self.amt-dra
                        frame7.pack_forget()
                        frame10.pack()
                        f9l10=Label(frame9,text=f'\u20B9 %.2f /-'%(self.amt-dra),fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
                        f9l10.place(x=30,y=150)
                    else:
                        f7l13.place_forget()
                        f7l3.place(x=55,y=225)
                else:
                    if(dra<self.amt):
                        res=self.amt-(dra+(dra*0.03))
                        frame7.pack_forget()
                        frame10.pack()
                        f9l10=Label(frame9,text=f'\u20B9 %.2f /-'%(self.amt-(dra+(dra*0.03))),fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
                        f9l10.place(x=30,y=150)
                    else:
                        f7l13.place_forget()
                        f7l3.place(x=55,y=225)
            else:
                f7l3.place_forget()
                f7l13.place(x=55,y=225)
        def screen8_10():
            frame8.pack_forget()
            frame10.pack()
        def screen9_11():
            frame9.pack_forget()
            frame11.pack()
        def screen10_9():
            frame10.pack_forget()
            frame9.pack()
        def screen10_11():
            frame10.pack_forget()
            frame11.pack()
        def clear():
            cl=f6e1.get()
            f6e1.delete(0,END)
        def clear1():
            cl=f7e1.get()
            f7e1.delete(0,END)
        def clear2():
            cl=f8e1.get()
            f8e1.delete(0,END)    
        def banknam():
            nam=f2e1.get();nam=nam.upper();nam=nam.replace(' BANK','');
            f3l1=Label(frame3,text='{} Bank'.format(nam),fg='blue',bg='#888D8F',font=('Arial',13,'bold'))
            f3l1.place(x=110,y=15)
        def cards():
            global ca
            l=f3e1.get();l=l.upper()
            if(l=='CARD'):
                screen3_4()
            else:
                f3l13.place(x=65,y=200)
        def pin():
            p=f4e1.get();a=p.isdigit();
            if(a==True):
                p=int(p)
                if(p==2022):
                    screen4_5()
                else:
                    f4l13.place(x=60,y=200)
            else:
                f4l13.place(x=60,y=200)
        def nepi():
            np=f8e1.get();l=len(np);dg=np.isdigit()
            if(l!=0):
                if(dg==True):
                    np=int(np)
                    if(np!=2022):
                        screen8_10()
                    else:
                        f8l11.place_forget()
                        f8l10.place(x=55,y=225)
                else:
                    f8l10.place_forget()
                    f8l11.place(x=55,y=225)
            else:
                f8l11.place_forget()
                f8l10.place(x=55,y=225)          
        #frame1
        frame1=Frame(root,bg='#888D8F')
        frame1.pack()
        frame1.config(width=245,height=360)
        root.config(bg='#888D8F')
        lb1=Label(frame1,text='Welcome To ATM',fg='black',bg='#888D8F',font=('Arial',18,'bold'))
        lb1.pack(padx=10,pady=150)
        btn=Button(frame1,text='Next',command=screen1_2)
        btn.place(x=90,y=300)
        #frame2
        frame2=Frame(root,bg='#888D8F')
        frame2.config(width=245,height=360)
        f2b1=Button(frame2,text='Back',command=screen2_1)
        f2b1.place(x=30,y=300)
        f2b2=Button(frame2,text='Next',command=screen2_3)
        f2b2.place(x=180,y=300)
        f2l1=Label(frame2,text='Enter Bank Name',fg='blue',bg='#888D8F',font=('Arial',18,'bold'))
        f2l1.place(x=20,y=120)
        f2e1=Entry(frame2,width=19,bd=3);f2e1.place(x=60,y=155)
        f2l2=Label(frame2,text='Note:',fg='red',bg='#888D8F',font=('Arial',12,'bold')).place(x=15,y=175)
        f2l2=Label(frame2,text='Banks Other than SBI,ICICI,\nUNION BANK Transaction \nCharge is 3% of your\nwithdrawal Amount',fg='black',bg='#888D8F',font=('Arial',10,'bold')).place(x=58,y=178)
        #frame3
        frame3=Frame(root,bg='#888D8F')
        frame3.config(width=245,height=360)
        f3l1=Label(frame3,text='Please Insert Card',fg='blue',bg='#888D8F',font=('Arial',18,'bold'))
        f3l1.place(x=20,y=120)
        f3l13=Label(frame3,text='Please Insert Card \nProperly',fg='red',bg='#888D8F',font=('Arial',9,'bold'))
        f3l1=Label(frame3,text='Welcom to',fg='blue',bg='#888D8F',font=('Arial',13,'bold'))
        f3l1.place(x=20,y=15)
        f3b2=Button(frame3,text='Next',command=cards)   
        f3b2.place(x=100,y=300)
        f3e1=Entry(frame3,width=19,bd=3);f3e1.place(x=60,y=155)  
        #frame4
        frame4=Frame(root,bg='#888D8F')
        frame4.config(width=245,height=360)
        f4l1=Label(frame4,text='Please Enter PIN',fg='blue',bg='#888D8F',font=('Arial',18,'bold'))
        f4l1.place(x=20,y=120)
        f4e1=Entry(frame4,width=19,bd=3,show='*');f4e1.place(x=60,y=155)
        f4l13=Label(frame4,text='Please Enter correct\nPIN',fg='red',bg='#888D8F',font=('Arial',9,'bold'))
        f4b12=Button(frame4,text='Next',command=pin)
        f4b12.place(x=100,y=300)
        #frame5
        frame5=Frame(root,bg='#888D8F')
        frame5.config(width=245,height=360)
        f5l1=Label(frame5,text='Select Transaction',fg='blue',bg='#888D8F',font=('Arial',18,'bold'))
        f5l1.place(x=20,y=15)
        f5b1=Button(frame5,text='DEPOSIT',width=10,command=screen5_6)
        f5b1.place(x=17,y=100)
        f5b2=Button(frame5,text='WITHDRAW',width=10,command=screen5_7)
        f5b2.place(x=145,y=100)
        f5b2=Button(frame5,text='CHANGE PIN',width=10,command=screen5_8)
        f5b2.place(x=17,y=180)
        f5b2=Button(frame5,text='BALANCE ENQUIRY',width=15,command=screen5_9)
        f5b2.place(x=125,y=180)
        #frame6
        frame6=Frame(root,bg='#888D8F')
        frame6.config(width=245,height=360)
        f6l1=Label(frame6,text='Please Enter Amount',fg='blue',bg='#888D8F',font=('Arial',14,'bold'))
        f6l1.place(x=20,y=120)
        f6e1=Entry(frame6,width=19,bd=3,)
        f6e1.place(x=60,y=155)
        f6b1=Button(frame6,text='Yes',width=7,command=screen6_10)
        f6b1.place(x=180,y=200)
        f6b2=Button(frame6,text='No',width=7,command=clear)
        f6b2.place(x=180,y=250)
        #frame7
        frame7=Frame(root,bg='#888D8F')
        frame7.config(width=245,height=360)
        f7l1=Label(frame7,text='Please Enter Amount',fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
        f7l1.place(x=20,y=120)
        f7e1=Entry(frame7,width=19,bd=3,)
        f7e1.place(x=60,y=155)
        f7l13=Label(frame7,text='Please Enter Amount',fg='red',bg='#888D8F',font=('Arial',8,'bold'))
        f7b1=Button(frame7,text='Yes',width=7,command=screen7_10)
        f7b1.place(x=180,y=200)
        f7b2=Button(frame7,text='No',width=7,command=clear1)
        f7b2.place(x=180,y=250)
        f7l3=Label(frame7,text='Withdraw Amount Should be less than Your Balance',fg='red',bg='#888D8F',font=('Arial',8,'bold'))
        #frame8
        frame8=Frame(root,bg='#888D8F')
        frame8.config(width=245,height=360)
        f8l1=Label(frame8,text='Enter New PIN',fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
        f8l1.place(x=50,y=120)
        f8e1=Entry(frame8,width=19,bd=3,show='*')
        f8e1.place(x=60,y=155)
        f8b1=Button(frame8,text='Yes',width=7,command=nepi)
        f8b1.place(x=180,y=200)
        f8b2=Button(frame8,text='No',width=7,command=clear2)
        f8b2.place(x=180,y=250)
        f8l10=Label(frame8,text='Please Enter New PIN',fg='red',bg='#888D8F',font=('Arial',9,'bold'))
        f8l11=Label(frame8,text='Only Numbers are \nAllowed',fg='red',bg='#888D8F',font=('Arial',9,'bold'))
        #frame9
        frame9=Frame(root,bg='#888D8F')
        frame9.config(width=245,height=360)
        f9l1=Label(frame9,text='Your Current Balance',fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
        f9l1.place(x=20,y=120)
        f9l10=Label(frame9,text=f'\u20B9 %.2f /-'%(self.amt),fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
        f9l10.place(x=30,y=150)
        f9b1=Button(frame9,text='Yes',width=7,command=screen9_11)
        f9b1.place(x=180,y=200)

        #frame10
        frame10=Frame(root,bg='#888D8F')
        frame10.config(width=245,height=360)
        f10l1=Label(frame10,text='Transaction Completed',fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
        f10l1.place(x=10,y=15)
        f10l1=Label(frame10,text='Want see Balance ?',fg='blue',bg='#888D8F',font=('Arial',15,'bold'))
        f10l1.place(x=20,y=120)

        f10b1=Button(frame10,text='Yes',width=7,command=screen10_9)
        f10b1.place(x=180,y=200)
        f10b2=Button(frame10,text='No',width=7,command=screen10_11)
        f10b2.place(x=180,y=250)
        #frame11
        frame11=Frame(root,bg='#888D8F')
        frame11.config(width=245,height=360)
        f11l1=Label(frame11,text='THANK YOU',fg='blue',bg='#888D8F',font=('Arial',18,'bold'))
        f11l1.place(x=40,y=150)
        root.mainloop()
    def missinglettersgame(self):
        self.catc=0;self.lel2=0;self.lel3=0;self.lel4=0;self.lel5=0;self.lel6=0;self.lel7=0;self.lel8=0;self.lel9=0;self.lel10=0;self.lel11=0;self.lel12=0;self.lel13=0;self.lel14=0;self.lel15=0;self.lel16=0;self.lel17=0;self.lel18=0;self.lel19=0;self.lel20=0;
        root=Tk()
        root.title('Missing Letters Game')
        root.geometry('245x360')
        root.minsize(width=245,height=360)
        root.maxsize(width=245,height=360)
        def screen1_2():
            frame1.pack_forget()
            frame2.pack()
        def screen2_1():
            frame2.pack_forget()
            frame1.pack()
        def screen2_3():
            f3l500.place_forget()
            frame2.pack_forget()
            frame3.pack()
        def screen3_2():
            frame3.pack_forget()
            frame2.pack()
        def screen2_4():
            f4l500.place_forget()
            frame2.pack_forget()
            frame4.pack()
        def screen4_3():
            f3l500.place_forget()
            frame4.pack_forget()
            frame3.pack()
        def screen5_4():
            f4l500.place_forget()
            frame5.pack_forget()
            frame4.pack()
        def screen2_5():
            f5l500.place_forget()
            frame2.pack_forget()
            frame5.pack()
        def screen6_5():
            f5l500.place_forget()
            frame6.pack_forget()
            frame5.pack()
        def screen2_6():
            f6l500.place_forget()
            frame2.pack_forget()
            frame6.pack()
        def screen7_6():
            f6l500.place_forget()
            frame7.pack_forget()
            frame6.pack()
        def screen2_7():
            f7l500.place_forget()
            frame2.pack_forget()
            frame7.pack()
        def screen8_7():
            f7l500.place_forget()
            frame8.pack_forget()
            frame7.pack()
        def screen2_8():
            f8l500.place_forget()
            frame2.pack_forget()
            frame8.pack()
        def screen9_8():
            f8l500.place_forget()
            frame9.pack_forget()
            frame8.pack()
        def screen2_9():
            f9l500.place_forget()
            frame2.pack_forget()
            frame9.pack()
        def screen10_9():
            f9l500.place_forget()
            frame10.pack_forget()
            frame9.pack()
        def screen2_10():
            f10l500.place_forget()
            frame2.pack_forget()
            frame10.pack()
        def screen11_10():
            f10l500.place_forget()
            frame11.pack_forget()
            frame10.pack()
        def screen2_11():
            f11l500.place_forget()
            frame2.pack_forget()
            frame11.pack()
        def screen12_11():
            f11l500.place_forget()
            frame12.pack_forget()
            frame11.pack()
        def screen2_12():
            f12l500.place_forget()
            frame2.pack_forget()
            frame12.pack()
        def screen13_12():
            f12l500.place_forget()
            frame13.pack_forget()
            frame12.pack()
        def screen2_13():
            f13l500.place_forget()
            frame2.pack_forget()
            frame13.pack()
        def screen14_13():
            f13l500.place_forget()
            frame14.pack_forget()
            frame13.pack()
        def screen2_14():
            f14l500.place_forget()
            frame2.pack_forget()
            frame14.pack()
        def screen15_14():
            f14l500.place_forget()
            frame15.pack_forget()
            frame14.pack()
        def screen2_15():
            f15l500.place_forget()
            frame2.pack_forget()
            frame15.pack()
        def screen16_15():
            f15l500.place_forget()
            frame16.pack_forget()
            frame15.pack()
        def screen2_16():
            f16l500.place_forget()
            frame2.pack_forget()
            frame16.pack()
        def screen17_16():
            f16l500.place_forget()
            frame17.pack_forget()
            frame16.pack()
        def screen2_17():
            f17l500.place_forget()
            frame2.pack_forget()
            frame17.pack()
        def screen18_17():
            f17l500.place_forget()
            frame18.pack_forget()
            frame17.pack()
        def screen2_18():
            f18l500.place_forget()
            frame2.pack_forget()
            frame18.pack()
        def screen19_18():
            f18l500.place_forget()
            frame19.pack_forget()
            frame18.pack()
        def screen2_19():
            f19l500.place_forget()
            frame2.pack_forget()
            frame19.pack()
        def screen20_19():
            f19l500.place_forget()
            frame20.pack_forget()
            frame19.pack()
        def screen2_20():
            f20l500.place_forget()
            frame2.pack_forget()
            frame20.pack()
        def screen21_20():
            f20l500.place_forget()
            frame21.pack_forget()
            frame20.pack()
        def screen2_21():
            f21l500.place_forget()
            frame2.pack_forget()
            frame21.pack()
        def screen22_21():
            f21l500.place_forget()
            frame22.pack_forget()
            frame21.pack()
        def screen2_22():
            f22l500.place_forget()
            frame2.pack_forget()
            frame22.pack()
            
        def tip():
            msb.showinfo("Tip", "The Word might be any name\n of Hindu mythology\nwords are not Repeated.")
        def level1():
            global catc
            l=['VANI', 'TARA', 'SAHA']
            z=f3e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.catc==0 and z==t0):
                        f3l500.place_forget()
                        f3e1.delete(0,END)
                        f3l1.place_forget()
                        f3l3.place(x=75,y=75)
                        self.catc+=1
                        ca=0
                    elif(self.catc==1 and z==t1):
                        f3l500.place_forget()
                        f3e1.delete(0,END)
                        f3l3.place_forget()
                        f3l4.place(x=75,y=75)
                        self.catc+=1
                        ca=0
                    elif(self.catc==2 and z==t2):
                        f3l500.place_forget()
                        f3e1.delete(0,END)
                        frame3.pack_forget()
                        frame4.pack()
                        self.catc+=1
                        ca=0
                elif(z!=l[i] and i==len(l)-1 and ca==1):
                    f3l500.place(x=45,y=200)
                    ca=1
        def level2():
            global lel2
            l=['RAMA', 'VALI', 'KRTI', 'SITA', 'SAMA']
            z=f4e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel2==0 and z==t3):
                        f4l500.place_forget()
                        f4e1.delete(0,END)
                        f4l1.place_forget()
                        f4l3.place(x=75,y=75)
                        self.lel2+=1
                        ca=0
                    elif(self.lel2==1 and z==t4):
                        f4l500.place_forget()
                        f4e1.delete(0,END)
                        f4l3.place_forget()
                        f4l4.place(x=75,y=75)
                        self.lel2+=1
                        ca=0
                    elif(self.lel2==2 and z==t5):
                        f4l500.place_forget()
                        f4e1.delete(0,END)
                        f4l4.place_forget()
                        f4l5.place(x=75,y=75)
                        self.lel2+=1
                        ca=0
                    elif(self.lel2==3 and z==t6):
                        f4l500.place_forget()
                        f4e1.delete(0,END)
                        f4l5.place_forget()
                        f4l6.place(x=75,y=75)
                        self.lel2+=1
                        ca=0
                    elif(self.lel2==4 and z==t7):
                        f4l6.place_forget()
                        f4e1.delete(0,END)
                        frame4.pack_forget()
                        frame5.pack()
                        self.lel2+=1
                        ca=0
                elif(ca==1):
                    f4l500.place(x=45,y=200)
                    ca=1

        def level3():
            global lel3
            l=['AMBA', 'JAYA', 'AMIT', 'KALI', 'ADYA', 'RAHU', 'LAVA']
            z=f5e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel3==0 and z==t8):
                        f5l500.place_forget()
                        f5e1.delete(0,END)
                        f5l1.place_forget()
                        f5l3.place(x=75,y=75)
                        self.lel3+=1
                        ca=0
                    elif(self.lel3==1 and z==t9):
                        f5l500.place_forget()
                        f5e1.delete(0,END)
                        f5l3.place_forget()
                        f5l4.place(x=75,y=75)
                        self.lel3+=1
                        ca=0
                    elif(self.lel3==2 and z==t10):
                        f5l500.place_forget()
                        f5e1.delete(0,END)
                        f5l4.place_forget()
                        f5l5.place(x=75,y=75)
                        self.lel3+=1
                        ca=0
                    elif(self.lel3==3 and z==t11):
                        f5l500.place_forget()
                        f5e1.delete(0,END)
                        f5l5.place_forget()
                        f5l6.place(x=75,y=75)
                        self.lel3+=1
                        ca=0
                    elif(self.lel3==4 and z==t12):
                        f5l500.place_forget()
                        f5e1.delete(0,END)
                        f5l6.place_forget()
                        f5l7.place(x=75,y=75)
                        self.lel3+=1
                        ca=0
                    elif(self.lel3==5 and z==t13):
                        f5l500.place_forget()
                        f5e1.delete(0,END)
                        f5l7.place_forget()
                        f5l8.place(x=75,y=75)
                        self.lel3+=1
                        ca=0
                    elif(self.lel3==6 and z==t14):
                        f5l8.place_forget()
                        f5e1.delete(0,END)
                        frame5.pack_forget()
                        frame6.pack()
                        self.lel3+=1
                        ca=0
                elif(ca==1):
                    f5l500.place(x=45,y=200)
                    ca=1
        def level4():
            global lel4
            l=['KURMA', 'RADHA', 'ARUNA', 'TARUN', 'SUVAK', 'VIDYA', 'SADAS','PADMA', 'KHARA']
            z=f6e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel4==0 and z==t15):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l1.place_forget()
                        f6l3.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==1 and z==t16):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l3.place_forget()
                        f6l4.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==2 and z==t17):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l4.place_forget()
                        f6l5.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==3 and z==t18):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l5.place_forget()
                        f6l6.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==4 and z==t19):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l6.place_forget()
                        f6l7.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==5 and z==t20):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l7.place_forget()
                        f6l8.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==6 and z==t21):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l8.place_forget()
                        f6l9.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==7 and z==t22):
                        f6l500.place_forget()
                        f6e1.delete(0,END)
                        f6l9.place_forget()
                        f6l10.place(x=75,y=75)
                        self.lel4+=1
                        ca=0
                    elif(self.lel4==8 and z==t23):
                        f6l10.place_forget()
                        f6e1.delete(0,END)
                        frame6.pack_forget()
                        frame7.pack()
                        self.lel4+=1
                        ca=0
                elif(ca==1):
                    f6l500.place(x=45,y=200)
                    ca=1
        def level5():
            global lel5
            l=['SALAN', 'NANDA', 'DEEPA', 'KRITI', 'ADITI', 'RUDRA', 'KALKI', 'KAMSA', 'ANISH', 'AARYA', 'KARNA']
            z=f7e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel5==0 and z==t24):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l1.place_forget()
                        f7l3.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==1 and z==t25):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l3.place_forget()
                        f7l4.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==2 and z==t26):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l4.place_forget()
                        f7l5.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==3 and z==t27):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l5.place_forget()
                        f7l6.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==4 and z==t28):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l6.place_forget()
                        f7l7.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==5 and z==t29):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l7.place_forget()
                        f7l8.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==6 and z==t30):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l8.place_forget()
                        f7l9.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==7 and z==t31):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l9.place_forget()
                        f7l10.place(x=75,y=75)
                        lel5+=1
                        ca=0
                    elif(self.lel5==8 and z==t32):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l10.place_forget()
                        f7l11.place(x=75,y=75)
                        self.lel5+=1
                        ca=0
                    elif(self.lel5==9 and z==t33):
                        f7l500.place_forget()
                        f7e1.delete(0,END)
                        f7l11.place_forget()
                        f7l12.place(x=75,y=75)
                        self.self.lel5+=1
                        ca=0
                    elif(self.lel5==10 and z==t34):
                        f7l12.place_forget()
                        f7e1.delete(0,END)
                        frame7.pack_forget()
                        frame8.pack()
                        self.lel5+=1
                        ca=0
                elif(ca==1):
                    f7l500.place(x=45,y=200)
                    ca=1
        def level6():
            global lel6
            l=['KUNDI', 'YAJNA', 'UMIKA', 'JATIN', 'MANAH', 'AMEYA', 'KUSHA', 'GAURI', 'DEETA', 'AJAYA', 'NITYA', 'SHYLA','GANGA']
            z=f8e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel6==0 and z==t35):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l1.place_forget()
                        f8l3.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==1 and z==t36):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l3.place_forget()
                        f8l4.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==2 and z==t37):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l4.place_forget()
                        f8l5.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==3 and z==t38):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l5.place_forget()
                        f8l6.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==4 and z==t39):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l6.place_forget()
                        f8l7.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==5 and z==t40):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l7.place_forget()
                        f8l8.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==6 and z==t41):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l8.place_forget()
                        f8l9.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==7 and z==t42):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l9.place_forget()
                        f8l10.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==8 and z==t43):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l10.place_forget()
                        f8l11.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==9 and z==t44):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l11.place_forget()
                        f8l12.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==10 and z==t45):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l12.place_forget()
                        f8l13.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==11 and z==t46):
                        f8l500.place_forget()
                        f8e1.delete(0,END)
                        f8l13.place_forget()
                        f8l14.place(x=75,y=75)
                        self.lel6+=1
                        ca=0
                    elif(self.lel6==12 and z==t47):
                        f8l14.place_forget()
                        f8e1.delete(0,END)
                        frame8.pack_forget()
                        frame9.pack()
                        self.lel6+=1
                        ca=0
                elif(ca==1):
                    f8l500.place(x=45,y=200)
                    ca=1
        def level7():
            global lel7
            l=['YADAVI', 'JANAKA', 'KAPILA', 'PRITHU', 'DILIPA', 'VARAHA', 'RAVANA', 'ANGADA', 'APARNA', 'DHEERA', 'TARITA', 'ANWITA', 'GUNINA', 'DEEPTA', 'BHAVYA']
            z=f9e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel7==0 and z==t48):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l1.place_forget()
                        f9l3.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==1 and z==t49):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l3.place_forget()
                        f9l4.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==2 and z==t50):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l4.place_forget()
                        f9l5.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==3 and z==t51):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l5.place_forget()
                        f9l6.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==4 and z==t52):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l6.place_forget()
                        f9l7.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==5 and z==t53):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l7.place_forget()
                        f9l8.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==6 and z==t54):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l8.place_forget()
                        f9l9.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==7 and z==t55):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l9.place_forget()
                        f9l10.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==8 and z==t56):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l10.place_forget()
                        f9l11.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==9 and z==t57):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l11.place_forget()
                        f9l12.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==10 and z==t58):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l12.place_forget()
                        f9l13.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==11 and z==t59):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l13.place_forget()
                        f9l14.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==12 and z==t60):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l14.place_forget()
                        f9l15.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==13 and z==t61):
                        f9l500.place_forget()
                        f9e1.delete(0,END)
                        f9l15.place_forget()
                        f9l16.place(x=75,y=75)
                        self.lel7+=1
                        ca=0
                    elif(self.lel7==14 and z==t62):
                        f9l16.place_forget()
                        f9e1.delete(0,END)
                        frame9.pack_forget()
                        frame10.pack()
                        self.lel7+=1
                        ca=0
                elif(ca==1):
                    f9l500.place(x=45,y=200)
                    ca=1
        def level8():
            global lel8
            l=['BUDDHA', 'KIMAYA', 'PRAJNA', 'SATHWA', 'LASAKI', 'JATAYU', 'AMBUJA', 'ABHAYA', 'AUGADH', 'SAUMYA', 'MOHINI', 'SENANI', 'VIDURA', 'SUKETU', 'KUBERA', 'VETALI', 'SUBAHU']
            z=f10e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel8==0 and z==t63):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l1.place_forget()
                        f10l3.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==1 and z==t64):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l3.place_forget()
                        f10l4.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==2 and z==t65):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l4.place_forget()
                        f10l5.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==3 and z==t66):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l5.place_forget()
                        f10l6.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==4 and z==t67):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l6.place_forget()
                        f10l7.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==5 and z==t68):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l7.place_forget()
                        f10l8.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==6 and z==t69):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l8.place_forget()
                        f10l9.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==7 and z==t70):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l9.place_forget()
                        f10l10.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==8 and z==t71):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l10.place_forget()
                        f10l11.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==9 and z==t72):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l11.place_forget()
                        f10l12.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==10 and z==t73):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l12.place_forget()
                        f10l13.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==11 and z==t74):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l13.place_forget()
                        f10l14.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==12 and z==t75):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l14.place_forget()
                        f10l15.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==13 and z==t76):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l15.place_forget()
                        f10l16.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==14 and z==t77):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l16.place_forget()
                        f10l17.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==15 and z==t78):
                        f10l500.place_forget()
                        f10e1.delete(0,END)
                        f10l17.place_forget()
                        f10l18.place(x=75,y=75)
                        self.lel8+=1
                        ca=0
                    elif(self.lel8==16 and z==t79):
                        f10l18.place_forget()
                        f10e1.delete(0,END)
                        frame10.pack_forget()
                        frame11.pack()
                        self.lel8+=1
                        ca=0
                elif(ca==1):
                    f10l500.place(x=45,y=200)
                    ca=1
        def level9():
            global lel9
            l=['BHEEMA', 'UTTARA', 'RAMESH', 'LOUKYA', 'KESHAV', 'VAMIKA', 'MUKUND', 'VARADA', 'NAMISH', 'TANISI', 'AMBIKA', 'VARUNI', 'BHIMBA', 'WAMIKA', 'YAYATI', 'MENAKA', 'ANJANA', 'NAKULA', 'PAVAKI']
            z=f11e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel9==0 and z==t80):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l1.place_forget()
                        f11l3.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==1 and z==t81):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l3.place_forget()
                        f11l4.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==2 and z==t82):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l4.place_forget()
                        f11l5.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==3 and z==t83):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l5.place_forget()
                        f11l6.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==4 and z==t84):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l6.place_forget()
                        f11l7.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==5 and z==t85):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l7.place_forget()
                        f11l8.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==6 and z==t86):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l8.place_forget()
                        f11l9.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==7 and z==t87):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l9.place_forget()
                        f11l10.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==8 and z==t88):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l10.place_forget()
                        f11l11.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==9 and z==t89):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l11.place_forget()
                        f11l12.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==10 and z==t90):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l12.place_forget()
                        f11l13.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==11 and z==t91):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l13.place_forget()
                        f11l14.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==12 and z==t92):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l14.place_forget()
                        f11l15.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==13 and z==t93):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l15.place_forget()
                        f11l16.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==14 and z==t94):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l16.place_forget()
                        f11l17.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==15 and z==t95):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l17.place_forget()
                        f11l18.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==16 and z==t96):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l18.place_forget()
                        f11l19.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==17 and z==t97):
                        f11l500.place_forget()
                        f11e1.delete(0,END)
                        f11l19.place_forget()
                        f11l20.place(x=75,y=75)
                        self.lel9+=1
                        ca=0
                    elif(self.lel9==18 and z==t98):
                        f11l20.place_forget()
                        f11e1.delete(0,END)
                        frame11.pack_forget()
                        frame12.pack()
                        self.lel9+=1
                        ca=0
                elif(ca==1):
                    f11l500.place(x=45,y=200)
                    ca=1
        def level10():
            global lel10
            l=['TATAKA', 'ROHINI', 'SURASA', 'BRAHMI', 'SUMALI', 'ADITYA', 'VAMANA', 'BALAKI', 'SARIKA', 'ARJUNA', 'VIRAVI', 'SUTADA', 'VINDHA', 'GIRIJA', 'GARUDA', 'KESARI', 'ANAGHA', 'MATSYA', 'BRINDA', 'ISHANI', 'ARYAHI']
            z=f12e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel10==0 and z==t99):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l1.place_forget()
                        f12l3.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==1 and z==t100):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l3.place_forget()
                        f12l4.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==2 and z==t101):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l4.place_forget()
                        f12l5.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==3 and z==t102):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l5.place_forget()
                        f12l6.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==4 and z==t103):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l6.place_forget()
                        f12l7.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==5 and z==t104):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l7.place_forget()
                        f12l8.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==6 and z==t105):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l8.place_forget()
                        f12l9.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==7 and z==t106):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l9.place_forget()
                        f12l10.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==8 and z==t107):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l10.place_forget()
                        f12l11.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==9 and z==t108):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l11.place_forget()
                        f12l12.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==10 and z==t109):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l12.place_forget()
                        f12l13.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==11 and z==t110):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l13.place_forget()
                        f12l14.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==12 and z==t111):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l14.place_forget()
                        f12l15.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==13 and z==t112):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l15.place_forget()
                        f12l16.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==14 and z==t113):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l16.place_forget()
                        f12l17.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==15 and z==t114):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l17.place_forget()
                        f12l18.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==16 and z==t115):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l18.place_forget()
                        f12l19.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==17 and z==t116):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l19.place_forget()
                        f12l20.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==18 and z==t117):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l20.place_forget()
                        f12l21.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==19 and z==t118):
                        f12l500.place_forget()
                        f12e1.delete(0,END)
                        f12l21.place_forget()
                        f12l22.place(x=75,y=75)
                        self.lel10+=1
                        ca=0
                    elif(self.lel10==20 and z==t119):
                        f12l22.place_forget()
                        f12e1.delete(0,END)
                        frame12.pack_forget()
                        frame13.pack()
                        self.lel10+=1
                        ca=0
                elif(ca==1):
                    f12l500.place(x=45,y=200)
                    ca=1

        def level11():
            global lel11
            l=['AHALYA', 'URMILA', 'DEETYA', 'KUNTHI', 'SHAILA', 'ADITRI', 'APARAA', 'AKSHAJ', 'PRANSHU', 'SAMPATI', 'DUSSAHA', 'DURJAYA', 'TOSHANI', 'RUKMINI', 'DURVASA', 'SHULINI', 'BHARATI', 'SUNABHA', 'PRAMATI', 'PADMESH', 'ANUSUYA', 'SAVITRI', 'ALOLUPA']
            z=f13e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel11==0 and z==t120):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l1.place_forget()
                        f13l3.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==1 and z==t121):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l3.place_forget()
                        f13l4.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==2 and z==t122):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l4.place_forget()
                        f13l5.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==3 and z==t123):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l5.place_forget()
                        f13l6.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==4 and z==t124):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l6.place_forget()
                        f13l7.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==5 and z==t125):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l7.place_forget()
                        f13l8.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==6 and z==t126):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l8.place_forget()
                        f13l9.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==7 and z==t127):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l9.place_forget()
                        f13l10.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==8 and z==t128):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l10.place_forget()
                        f13l11.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==9 and z==t129):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l11.place_forget()
                        f13l12.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==10 and z==t130):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l12.place_forget()
                        f13l13.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==11 and z==t131):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l13.place_forget()
                        f13l14.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==12 and z==t132):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l14.place_forget()
                        f13l15.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==13 and z==t133):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l15.place_forget()
                        f13l16.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==14 and z==t134):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l16.place_forget()
                        f13l17.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==15 and z==t135):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l17.place_forget()
                        f13l18.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==16 and z==t136):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l18.place_forget()
                        f13l19.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==17 and z==t137):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l19.place_forget()
                        f13l20.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==18 and z==t138):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l20.place_forget()
                        f13l21.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==19 and z==t139):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l21.place_forget()
                        f13l22.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==20 and z==t140):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l22.place_forget()
                        f13l23.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==21 and z==t141):
                        f13l500.place_forget()
                        f13e1.delete(0,END)
                        f13l23.place_forget()
                        f13l24.place(x=75,y=75)
                        self.lel11+=1
                        ca=0
                    elif(self.lel11==22 and z==t142):
                        f13l24.place_forget()
                        f13e1.delete(0,END)
                        frame13.pack_forget()
                        frame14.pack()
                        self.lel11+=1
                        ca=0
                elif(ca==1):
                    f13l500.place(x=45,y=200)
                    ca=1
        def level12():
            global lel12
            l=['ATIKAYA', 'BHAIRAV', 'AVIGHNA', 'BHARATA', 'VIRJASA', 'SHABARI', 'PARMESH', 'TRIGUNA', 'SATYAKI', 'SHUBHAN', 'BAHVASI', 'ANAADIH', 'PARESHA', 'TRARITI', 'GAYATRI', 'VATVEGA', 'PRANAVA', 'ILAVIDA', 'SANJAYA', 'KRADHAN', 'KAVACHI', 'MARICHA', 'KASHTHA', 'VIKTANA', 'DURMADA']
            z=f14e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel12==0 and z==t143):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l1.place_forget()
                        f14l3.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==1 and z==t144):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l3.place_forget()
                        f14l4.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==2 and z==t145):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l4.place_forget()
                        f14l5.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==3 and z==t146):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l5.place_forget()
                        f14l6.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==4 and z==t147):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l6.place_forget()
                        f14l7.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==5 and z==t148):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l7.place_forget()
                        f14l8.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==6 and z==t149):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l8.place_forget()
                        f14l9.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==7 and z==t150):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l9.place_forget()
                        f14l10.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==8 and z==t151):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l10.place_forget()
                        f14l11.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==9 and z==t152):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l11.place_forget()
                        f14l12.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==10 and z==t153):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l12.place_forget()
                        f14l13.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==11 and z==t154):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l13.place_forget()
                        f14l14.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==12 and z==t155):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l14.place_forget()
                        f14l15.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==13 and z==t156):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l15.place_forget()
                        f14l16.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==14 and z==t157):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l16.place_forget()
                        f14l17.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==15 and z==t158):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l17.place_forget()
                        f14l18.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==16 and z==t159):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l18.place_forget()
                        f14l19.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==17 and z==t160):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l19.place_forget()
                        f14l20.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==18 and z==t161):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l20.place_forget()
                        f14l21.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==19 and z==t162):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l21.place_forget()
                        f14l22.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==20 and z==t163):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l22.place_forget()
                        f14l23.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==21 and z==t164):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l23.place_forget()
                        f14l24.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==22 and z==t165):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l24.place_forget()
                        f14l25.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==23 and z==t166):
                        f14l500.place_forget()
                        f14e1.delete(0,END)
                        f14l25.place_forget()
                        f14l26.place(x=75,y=75)
                        self.lel12+=1
                        ca=0
                    elif(self.lel12==24 and z==t167):
                        f14l26.place_forget()
                        f14e1.delete(0,END)
                        frame14.pack_forget()
                        frame15.pack()
                        self.lel12+=1
                        ca=0
                elif(ca==1):
                    f14l500.place(x=45,y=200)
                    ca=1
        def level13():
            global lel13
            l=['CHITHRA', 'JAITHRA', 'THATAKA', 'HERAMBA', 'AEINDRI', 'KRISHNA', 'VANMAYI', 'SUKHADA', 'HAMSINI', 'SAMENDU', 'AYOBAHU', 'EVYAVAN', 'VIKARNA', 'MANDAVI', 'BHISHMA', 'UMAPATI', 'VIVITSU', 'HIDIMBI', 'DURVIGA', 'JAYAPAL', 'BHUDHAV', 'MANTRAM', 'SALYUDU', 'SUGRIVA', 'HANUMAN', 'KAIKEYI', 'TVARITA']
            z=f15e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel13==0 and z==t168):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l1.place_forget()
                        f15l3.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==1 and z==t169):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l3.place_forget()
                        f15l4.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==2 and z==t170):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l4.place_forget()
                        f15l5.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==3 and z==t171):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l5.place_forget()
                        f15l6.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==4 and z==t172):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l6.place_forget()
                        f15l7.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==5 and z==t173):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l7.place_forget()
                        f15l8.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==6 and z==t174):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l8.place_forget()
                        f15l9.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==7 and z==t175):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l9.place_forget()
                        f15l10.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==8 and z==t176):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l10.place_forget()
                        f15l11.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==9 and z==t177):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l11.place_forget()
                        f15l12.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==10 and z==t178):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l12.place_forget()
                        f15l13.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==11 and z==t179):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l13.place_forget()
                        f15l14.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==12 and z==t180):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l14.place_forget()
                        f15l15.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==13 and z==t181):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l15.place_forget()
                        f15l16.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==14 and z==t182):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l16.place_forget()
                        f15l17.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==15 and z==t183):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l17.place_forget()
                        f15l18.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==16 and z==t184):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l18.place_forget()
                        f15l19.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==17 and z==t185):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l19.place_forget()
                        f15l20.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==18 and z==t186):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l20.place_forget()
                        f15l21.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==19 and z==t187):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l21.place_forget()
                        f15l22.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==20 and z==t188):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l22.place_forget()
                        f15l23.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==21 and z==t189):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l23.place_forget()
                        f15l24.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==22 and z==t190):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l24.place_forget()
                        f15l25.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==23 and z==t191):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l25.place_forget()
                        f15l26.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==24 and z==t192):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l26.place_forget()
                        f15l27.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==25 and z==t193):
                        f15l500.place_forget()
                        f15e1.delete(0,END)
                        f15l27.place_forget()
                        f15l28.place(x=75,y=75)
                        self.lel13+=1
                        ca=0
                    elif(self.lel13==26 and z==t194):
                        f15l28.place_forget()
                        f15e1.delete(0,END)
                        frame15.pack_forget()
                        frame16.pack()
                        self.lel13+=1
                        ca=0
                elif(ca==1):
                    f15l500.place(x=45,y=200)
                    ca=1
        def level14():
            global lel14
            l=['SUSHENA', 'VALLARI', 'UDDANDA', 'RAYIRTH', 'BHAVANI', 'TUMBURU', 'DEVESHI', 'SHRIHAN', 'VIRADHA', 'MANOMAY', 'AJITESH', 'ANUDARA', 'VAARAHI', 'SWAROOP', 'SURESHI', 'SUVARMA', 'SUMITRA', 'RAMAKANT', 'RISHABHA', 'PRAHASTA', 'SARASANA', 'SAMAVART', 'BHASKARI', 'SAHADEVA', 'JAMBAVAN', 'MAYASURA', 'SATINDRA', 'SRIRUDRA', 'PITAMBAR']
            z=f16e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel14==0 and z==t195):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l1.place_forget()
                        f16l3.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==1 and z==t196):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l3.place_forget()
                        f16l4.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==2 and z==t197):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l4.place_forget()
                        f16l5.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==3 and z==t198):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l5.place_forget()
                        f16l6.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==4 and z==t199):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l6.place_forget()
                        f16l7.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==5 and z==t200):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l7.place_forget()
                        f16l8.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==6 and z==t201):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l8.place_forget()
                        f16l9.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==7 and z==t202):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l9.place_forget()
                        f16l10.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==8 and z==t203):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l10.place_forget()
                        f16l11.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==9 and z==t204):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l11.place_forget()
                        f16l12.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==10 and z==t205):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l12.place_forget()
                        f16l13.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==11 and z==t206):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l13.place_forget()
                        f16l14.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==12 and z==t207):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l14.place_forget()
                        f16l15.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==13 and z==t208):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l15.place_forget()
                        f16l16.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==14 and z==t209):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l16.place_forget()
                        f16l17.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==15 and z==t210):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l17.place_forget()
                        f16l18.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==16 and z==t211):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l18.place_forget()
                        f16l19.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==17 and z==t212):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l19.place_forget()
                        f16l20.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==18 and z==t213):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l20.place_forget()
                        f16l21.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==19 and z==t214):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l21.place_forget()
                        f16l22.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==20 and z==t215):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l22.place_forget()
                        f16l23.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==21 and z==t216):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l23.place_forget()
                        f16l24.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==22 and z==t217):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l24.place_forget()
                        f16l25.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==23 and z==t218):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l25.place_forget()
                        f16l26.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==24 and z==t219):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l26.place_forget()
                        f16l27.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==25 and z==t220):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l27.place_forget()
                        f16l28.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==26 and z==t221):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l28.place_forget()
                        f16l29.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==27 and z==t222):
                        f16l500.place_forget()
                        f16e1.delete(0,END)
                        f16l29.place_forget()
                        f16l30.place(x=75,y=75)
                        self.lel14+=1
                        ca=0
                    elif(self.lel14==28 and z==t223):
                        f16l30.place_forget()
                        f16e1.delete(0,END)
                        frame16.pack_forget()
                        frame17.pack()
                        self.lel14+=1
                        ca=0
                elif(ca==1):
                    f16l500.place(x=45,y=200)
                    ca=1
        def level15():
            global lel15
            l=['INDRAJIT', 'JAYANTAH', 'AGRAYAYI', 'SURESHAM', 'PRAMODAN', 'NISHANGI', 'SHIVANNE', 'KAISHORI', 'KABANDHA', 'VIRABAHI', 'KUNDASHI', 'SIKANDHI', 'KUNDUSAI', 'AMEYATMA', 'AVANEESH', 'VASISTHA', 'VARALIKA', 'MALYAVAN', 'NAGAADAT', 'APARAJIT', 'MAHABAHU', 'SHANKHIN', 'BHARGAVI', 'SUBHADRA', 'ALAMPATA', 'MADHUBAN', 'SIDDHAMA', 'KAUSALYA', 'MAHODARA', 'GANDHARI', 'VISHRAVA']
            z=f17e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel15==0 and z==t224):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l1.place_forget()
                        f17l3.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==1 and z==t225):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l3.place_forget()
                        f17l4.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==2 and z==t226):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l4.place_forget()
                        f17l5.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==3 and z==t227):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l5.place_forget()
                        f17l6.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==4 and z==t228):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l6.place_forget()
                        f17l7.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==5 and z==t229):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l7.place_forget()
                        f17l8.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==6 and z==t230):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l8.place_forget()
                        f17l9.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==7 and z==t231):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l9.place_forget()
                        f17l10.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==8 and z==t232):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l10.place_forget()
                        f17l11.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==9 and z==t233):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l11.place_forget()
                        f17l12.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==10 and z==t234):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l12.place_forget()
                        f17l13.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==11 and z==t235):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l13.place_forget()
                        f17l14.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==12 and z==t236):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l14.place_forget()
                        f17l15.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==13 and z==t237):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l15.place_forget()
                        f17l16.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==14 and z==t238):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l16.place_forget()
                        f17l17.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==15 and z==t239):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l17.place_forget()
                        f17l18.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==16 and z==t240):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l18.place_forget()
                        f17l19.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==17 and z==t241):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l19.place_forget()
                        f17l20.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==18 and z==t242):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l20.place_forget()
                        f17l21.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==19 and z==t243):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l21.place_forget()
                        f17l22.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==20 and z==t244):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l22.place_forget()
                        f17l23.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==21 and z==t245):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l23.place_forget()
                        f17l24.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==22 and z==t246):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l24.place_forget()
                        f17l25.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==23 and z==t247):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l25.place_forget()
                        f17l26.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==24 and z==t248):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l26.place_forget()
                        f17l27.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==25 and z==t249):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l27.place_forget()
                        f17l28.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==26 and z==t250):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l28.place_forget()
                        f17l29.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==27 and z==t251):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l29.place_forget()
                        f17l30.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==28 and z==t252):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l30.place_forget()
                        f17l31.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==29 and z==t253):
                        f17l500.place_forget()
                        f17e1.delete(0,END)
                        f17l31.place_forget()
                        f17l32.place(x=75,y=75)
                        self.lel15+=1
                        ca=0
                    elif(self.lel15==30 and z==t254):
                        f17l32.place_forget()
                        f17e1.delete(0,END)
                        frame17.pack_forget()
                        frame18.pack()
                        self.lel15+=1
                        ca=0
                elif(ca==1):
                    f17l500.place(x=45,y=200)
                    ca=1
        def level16():
            global lel16
            l=['AASHIRYA', 'JAGADISH', 'DHUSSALA', 'DURMUKHA', 'UPANANDA', 'NAROTTAM', 'KAMALIKA', 'NITYANTA', 'PARIJATA', 'MAHAKRAM', 'AMBALIKA', 'KAVEESHA', 'UGRASENA', 'ASHUTOSH', 'SADASIVA', 'SUHASTHA', 'SAHISHNU', 'KAMAKSHI', 'SUVARCHA', 'NARSIMHA', 'BALARAMA', 'AKHURATH', 'SULOCHAN', 'AMRITAYA', 'MANTHARA', 'BHIMVEGA', 'EKALAVYA', 'PADMAKAR', 'KAKASURA', 'SHAMBUKA', 'DRAUPADI', 'LOHITAKSH', 'VASISHTHA']
            z=f18e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel16==0 and z==t255):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l1.place_forget()
                        f18l3.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==1 and z==t256):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l3.place_forget()
                        f18l4.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==2 and z==t257):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l4.place_forget()
                        f18l5.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==3 and z==t258):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l5.place_forget()
                        f18l6.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==4 and z==t259):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l6.place_forget()
                        f18l7.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==5 and z==t260):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l7.place_forget()
                        f18l8.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==6 and z==t261):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l8.place_forget()
                        f18l9.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==7 and z==t262):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l9.place_forget()
                        f18l10.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==8 and z==t263):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l10.place_forget()
                        f18l11.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==9 and z==t264):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l11.place_forget()
                        f18l12.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==10 and z==t265):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l12.place_forget()
                        f18l13.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==11 and z==t266):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l13.place_forget()
                        f18l14.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==12 and z==t267):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l14.place_forget()
                        f18l15.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==13 and z==t268):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l15.place_forget()
                        f18l16.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==14 and z==t269):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l16.place_forget()
                        f18l17.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==15 and z==t270):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l17.place_forget()
                        f18l18.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==16 and z==t271):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l18.place_forget()
                        f18l19.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==17 and z==t272):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l19.place_forget()
                        f18l20.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==18 and z==t273):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l20.place_forget()
                        f18l21.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==19 and z==t274):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l21.place_forget()
                        f18l22.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==20 and z==t275):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l22.place_forget()
                        f18l23.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==21 and z==t276):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l23.place_forget()
                        f18l24.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==22 and z==t277):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l24.place_forget()
                        f18l25.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==23 and z==t278):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l25.place_forget()
                        f18l26.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==24 and z==t279):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l26.place_forget()
                        f18l27.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==25 and z==t280):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l27.place_forget()
                        f18l28.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==26 and z==t281):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l28.place_forget()
                        f18l29.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==27 and z==t282):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l29.place_forget()
                        f18l30.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==28 and z==t283):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l30.place_forget()
                        f18l31.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==29 and z==t284):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l31.place_forget()
                        f18l32.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==30 and z==t285):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l32.place_forget()
                        f18l33.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==31 and z==t286):
                        f18l500.place_forget()
                        f18e1.delete(0,END)
                        f18l33.place_forget()
                        f18l34.place(x=75,y=75)
                        self.lel16+=1
                        ca=0
                    elif(self.lel16==32 and z==t287):
                        f18l34.place_forget()
                        f18e1.delete(0,END)
                        frame18.pack_forget()
                        frame19.pack()
                        self.lel16+=1
                        ca=0
                elif(ca==1):
                    f18l500.place(x=45,y=200)
                    ca=1

        def level17():
            global lel17
            l=['VEDAKARTA', 'APARAJEET', 'CHITRANGA', 'PADMAPATI', 'DHANANJAY', 'URNANABHA', 'SASIREKHA', 'DEVANTAKA', 'JALADHIJA', 'HYMAVATHY', 'MANDODARI', 'VEERYAVAN', 'UGRASARVA', 'VRIDARAKA', 'MARICHUDU', 'CHAKRIKAA', 'INDRARJUN', 'DURADHARA', 'SARVATMAN', 'DIRGHABHU', 'NIRANJANA', 'SARVAYONI', 'PADMANABH', 'ANUVINDHA', 'SATKARTAR', 'SINHAYANA', 'MAHATEJAS', 'KAMALAKAR', 'SWAYAMBHU', 'SOMAKIRTI', 'SRIKANTHA', 'YASHVASIN', 'PARIKSHIT', 'HARIPRIYA', 'KICHAKUDU']
            z=f19e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel17==0 and z==t288):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l1.place_forget()
                        f19l3.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==1 and z==t289):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l3.place_forget()
                        f19l4.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==2 and z==t290):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l4.place_forget()
                        f19l5.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==3 and z==t291):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l5.place_forget()
                        f19l6.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==4 and z==t292):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l6.place_forget()
                        f19l7.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==5 and z==t293):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l7.place_forget()
                        f19l8.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==6 and z==t294):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l8.place_forget()
                        f19l9.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==7 and z==t295):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l9.place_forget()
                        f19l10.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==8 and z==t296):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l10.place_forget()
                        f19l11.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==9 and z==t297):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l11.place_forget()
                        f19l12.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==10 and z==t298):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l12.place_forget()
                        f19l13.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==11 and z==t299):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l13.place_forget()
                        f19l14.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==12 and z==t300):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l14.place_forget()
                        f19l15.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==13 and z==t301):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l15.place_forget()
                        f19l16.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==14 and z==t302):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l16.place_forget()
                        f19l17.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==15 and z==t303):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l17.place_forget()
                        f19l18.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==16 and z==t304):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l18.place_forget()
                        f19l19.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==17 and z==t305):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l19.place_forget()
                        f19l20.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==18 and z==t306):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l20.place_forget()
                        f19l21.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==19 and z==t307):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l21.place_forget()
                        f19l22.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==20 and z==t308):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l22.place_forget()
                        f19l23.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==21 and z==t309):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l23.place_forget()
                        f19l24.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==22 and z==t310):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l24.place_forget()
                        f19l25.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==23 and z==t311):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l25.place_forget()
                        f19l26.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==24 and z==t312):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l26.place_forget()
                        f19l27.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==25 and z==t313):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l27.place_forget()
                        f19l28.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==26 and z==t314):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l28.place_forget()
                        f19l29.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==27 and z==t315):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l29.place_forget()
                        f19l30.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==28 and z==t316):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l30.place_forget()
                        f19l31.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==29 and z==t317):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l31.place_forget()
                        f19l32.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==30 and z==t318):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l32.place_forget()
                        f19l33.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==31 and z==t319):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l33.place_forget()
                        f19l34.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==32 and z==t320):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l34.place_forget()
                        f19l35.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==33 and z==t321):
                        f19l500.place_forget()
                        f19e1.delete(0,END)
                        f19l35.place_forget()
                        f19l36.place(x=75,y=75)
                        self.lel17+=1
                        ca=0
                    elif(self.lel17==34 and z==t322):
                        f19l36.place_forget()
                        f19e1.delete(0,END)
                        frame19.pack_forget()
                        frame20.pack()
                        self.lel17+=1
                        ca=0
                elif(ca==1):
                    f19l500.place(x=45,y=200)
                    ca=1
        def level18():
            global lel18
            l=['SULOCHANA', 'SABAREESH', 'PANDURAJU', 'SHATAKSHI', 'SHRESHTHA', 'VAISHNAVI', 'UGRAYUDHA', 'AKSHOBHYA', 'BHUVANESH', 'PADMAKSHI', 'LAKSHMANA', 'DUSHKARNA', 'VYOMASURA', 'ABHIMANYU', 'SHISHUPALA', 'DASHARATHA', 'JARASANDHA', 'ADI-PURUSH', 'JALAGANDHA', 'DHARMARAJU', 'TARAKASURA', 'SURESHWARA', 'SHATRUGHNA', 'AADIYAKETU', 'CHITRASENA', 'SAMARENDRA', 'TRIVIKRAMA', 'HAYAGREEVA', 'EKAAKSHARA', 'DHUSHASANA', 'ANANTAJEET', 'YOGESHWARI', 'SATYABHAMA', 'JARASANGHA', 'MAHADHYUTA', 'BHIMARATHA', 'VIBHISHANA']
            z=f20e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel18==0 and z==t323):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l1.place_forget()
                        f20l3.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==1 and z==t324):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l3.place_forget()
                        f20l4.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==2 and z==t325):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l4.place_forget()
                        f20l5.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==3 and z==t326):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l5.place_forget()
                        f20l6.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==4 and z==t327):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l6.place_forget()
                        f20l7.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==5 and z==t328):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l7.place_forget()
                        f20l8.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==6 and z==t329):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l8.place_forget()
                        f20l9.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==7 and z==t330):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l9.place_forget()
                        f20l10.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==8 and z==t331):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l10.place_forget()
                        f20l11.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==9 and z==t332):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l11.place_forget()
                        f20l12.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==10 and z==t333):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l12.place_forget()
                        f20l13.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==11 and z==t334):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l13.place_forget()
                        f20l14.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==12 and z==t335):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l14.place_forget()
                        f20l15.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==13 and z==t336):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l15.place_forget()
                        f20l16.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==14 and z==t337):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l16.place_forget()
                        f20l17.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==15 and z==t338):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l17.place_forget()
                        f20l18.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==16 and z==t339):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l18.place_forget()
                        f20l19.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==17 and z==t340):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l19.place_forget()
                        f20l20.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==18 and z==t341):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l20.place_forget()
                        f20l21.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==19 and z==t342):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l21.place_forget()
                        f20l22.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==20 and z==t343):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l22.place_forget()
                        f20l23.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==21 and z==t344):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l23.place_forget()
                        f20l24.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==22 and z==t345):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l24.place_forget()
                        f20l25.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==23 and z==t346):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l25.place_forget()
                        f20l26.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==24 and z==t347):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l26.place_forget()
                        f20l27.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==25 and z==t348):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l27.place_forget()
                        f20l28.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==26 and z==t349):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l28.place_forget()
                        f20l29.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==27 and z==t350):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l29.place_forget()
                        f20l30.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==28 and z==t351):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l30.place_forget()
                        f20l31.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==29 and z==t352):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l31.place_forget()
                        f20l32.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==30 and z==t353):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l32.place_forget()
                        f20l33.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==31 and z==t354):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l33.place_forget()
                        f20l34.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==32 and z==t355):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l34.place_forget()
                        f20l35.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==33 and z==t356):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l35.place_forget()
                        f20l36.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==34 and z==t357):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l36.place_forget()
                        f20l37.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==35 and z==t358):
                        f20l500.place_forget()
                        f20e1.delete(0,END)
                        f20l37.place_forget()
                        f20l38.place(x=75,y=75)
                        self.lel18+=1
                        ca=0
                    elif(self.lel18==36 and z==t359):
                        f20l38.place_forget()
                        f20e1.delete(0,END)
                        frame20.pack_forget()
                        frame21.pack()
                        self.lel18+=1
                        ca=0
                elif(ca==1):
                    f20l500.place(x=45,y=200)
                    ca=1
        def level19():
            global lel19
            l=['KUNDADHARA', 'CHITRAKSHA', 'SANTHANUDU', 'MAHISASURA', 'DIRGHAROMA', 'SURPANAKHA', 'UPACHITRAN', 'SAHASRAJIT', 'SHIVAPRIYA', 'BHANUMATHI', 'ASHWATHAMA', 'KARTIKEYAN', 'SURESHWARI', 'DATTATREYA', 'NARAKASURA', 'DURDHAESHA', 'BHAVAPRITA', 'LAVANASURA', 'DURMARSHAN', 'BILVANILAYA', 'VISHALAKSHI', 'BHAGYASHREE', 'BARBARIKUDU', 'FOUR-KUMARS', 'SUKRACHARYA', 'RAUDRAKARMA', 'DANALAKSHMI', 'KUMBHAKARNA', 'GHATOTKACHA', 'KUNDHADHARA', 'VISHVAMITRA', 'VISHALAKSHA', 'KRUPACHARYA', 'ANAGHRUSHYA', 'CHANDRARUPA', 'SHURPANAKHA', 'DHANURDHARA', 'RUDRAVEERYA', 'JAYALAKSHMI']
            z=f21e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel19==0 and z==t360):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l1.place_forget()
                        f21l3.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==1 and z==t361):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l3.place_forget()
                        f21l4.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==2 and z==t362):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l4.place_forget()
                        f21l5.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==3 and z==t363):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l5.place_forget()
                        f21l6.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==4 and z==t364):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l6.place_forget()
                        f21l7.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==5 and z==t365):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l7.place_forget()
                        f21l8.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==6 and z==t366):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l8.place_forget()
                        f21l9.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==7 and z==t367):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l9.place_forget()
                        f21l10.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==8 and z==t368):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l10.place_forget()
                        f21l11.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==9 and z==t369):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l11.place_forget()
                        f21l12.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==10 and z==t370):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l12.place_forget()
                        f21l13.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==11 and z==t371):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l13.place_forget()
                        f21l14.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==12 and z==t372):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l14.place_forget()
                        f21l15.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==13 and z==t373):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l15.place_forget()
                        f21l16.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==14 and z==t374):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l16.place_forget()
                        f21l17.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==15 and z==t375):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l17.place_forget()
                        f21l18.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==16 and z==t376):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l18.place_forget()
                        f21l19.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==17 and z==t377):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l19.place_forget()
                        f21l20.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==18 and z==t378):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l20.place_forget()
                        f21l21.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==19 and z==t379):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l21.place_forget()
                        f21l22.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==20 and z==t380):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l22.place_forget()
                        f21l23.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==21 and z==t381):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l23.place_forget()
                        f21l24.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==22 and z==t382):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l24.place_forget()
                        f21l25.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==23 and z==t383):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l25.place_forget()
                        f21l26.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==24 and z==t384):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l26.place_forget()
                        f21l27.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==25 and z==t385):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l27.place_forget()
                        f21l28.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==26 and z==t386):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l28.place_forget()
                        f21l29.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==27 and z==t387):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l29.place_forget()
                        f21l30.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==28 and z==t388):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l30.place_forget()
                        f21l31.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==29 and z==t389):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l31.place_forget()
                        f21l32.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==30 and z==t390):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l32.place_forget()
                        f21l33.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==31 and z==t391):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l33.place_forget()
                        f21l34.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==32 and z==t392):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l34.place_forget()
                        f21l35.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==33 and z==t393):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l35.place_forget()
                        f21l36.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==34 and z==t394):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l36.place_forget()
                        f21l37.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==35 and z==t395):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l37.place_forget()
                        f21l38.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==36 and z==t396):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l38.place_forget()
                        f21l39.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==37 and z==t397):
                        f21l500.place_forget()
                        f21e1.delete(0,END)
                        f21l39.place_forget()
                        f21l40.place(x=75,y=75)
                        self.lel19+=1
                        ca=0
                    elif(self.lel19==38 and z==t398):
                        f21l40.place_forget()
                        f21e1.delete(0,END)
                        frame21.pack_forget()
                        frame22.pack()
                        self.lel19+=1
                        ca=0
                elif(ca==1):
                    f21l500.place(x=45,y=200)
                    ca=1
        def level20():
            global lel20
            l=['DHANVANTARI', 'DHURYODHANA', 'SHRUTAKIRTI', 'DRIDASANDHA', 'DURVIMOCHAN', 'DIRGHLOCHAN', 'SHIVANSHIKA', 'MAHALAKSHMI', 'DUSHPARAJAI', 'THAKSHAKUDU', 'BALVARDHANA', 'DRIDHAVARMA', 'PARASHURAMA', 'CHITRAVARMA', 'KUNDHABHEDI', 'MAMASAKHUNI', 'DRHONACHARYA', 'DHRITARASTRA', 'INDUSHEETALA', 'VIDYALAKSHMI', 'CHITHRAYUDHA', 'RISHYASRINGA', 'CHARUCHITHRA', 'SATHYASANDHA', 'DRIDHAHASTHA', 'NARA-NARAYANA', 'SAGE-KAMBHOJA', 'LAXMANAKUMARA', 'DRIDHAKSHATRA', 'SRAVANA-KUMAR', 'HIRANYAKASIPA', 'VINDHYAVASINI', 'NARADA–NARADA', 'AKSHAYAKUMARA', 'CHITRAKUNDALA', 'VICHITRAVIRYA', 'VIJAYALAKSHMI', 'DUSHPRASARSHAN', 'SOVANNA-MACCHA', 'SEETHA-KALYANAM', 'DHRIDARATHASRAYA']
            z=f22e1.get();z=z.upper();ca=1;
            for i in range(len(l)):
                if(z==l[i]):
                    if(self.lel20==0 and z==t399):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l1.place_forget()
                        f22l3.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==1 and z==t400):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l3.place_forget()
                        f22l4.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==2 and z==t401):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l4.place_forget()
                        f22l5.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==3 and z==t402):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l5.place_forget()
                        f22l6.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==4 and z==t403):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l6.place_forget()
                        f22l7.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==5 and z==t404):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l7.place_forget()
                        f22l8.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==6 and z==t405):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l8.place_forget()
                        f22l9.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==7 and z==t406):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l9.place_forget()
                        f22l10.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==8 and z==t407):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l10.place_forget()
                        f22l11.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==9 and z==t408):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l11.place_forget()
                        f22l12.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==10 and z==t409):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l12.place_forget()
                        f22l13.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==11 and z==t410):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l13.place_forget()
                        f22l14.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==12 and z==t411):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l14.place_forget()
                        f22l15.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==13 and z==t412):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l15.place_forget()
                        f22l16.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==14 and z==t413):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l16.place_forget()
                        f22l17.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==15 and z==t414):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l17.place_forget()
                        f22l18.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==16 and z==t415):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l18.place_forget()
                        f22l19.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==17 and z==t416):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l19.place_forget()
                        f22l20.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==18 and z==t417):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l20.place_forget()
                        f22l21.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==19 and z==t418):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l21.place_forget()
                        f22l22.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==20 and z==t419):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l22.place_forget()
                        f22l23.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==21 and z==t420):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l23.place_forget()
                        f22l24.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==22 and z==t421):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l24.place_forget()
                        f22l25.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==23 and z==t422):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l25.place_forget()
                        f22l26.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==24 and z==t423):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l26.place_forget()
                        f22l27.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==25 and z==t424):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l27.place_forget()
                        f22l28.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==26 and z==t425):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l28.place_forget()
                        f22l29.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==27 and z==t426):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l29.place_forget()
                        f22l30.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==28 and z==t427):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l30.place_forget()
                        f22l31.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==29 and z==t428):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l31.place_forget()
                        f22l32.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==30 and z==t429):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l32.place_forget()
                        f22l33.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==31 and z==t430):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l33.place_forget()
                        f22l34.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==32 and z==t431):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l34.place_forget()
                        f22l35.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==33 and z==t432):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l35.place_forget()
                        f22l36.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==34 and z==t433):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l36.place_forget()
                        f22l37.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==35 and z==t434):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l37.place_forget()
                        f22l38.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==36 and z==t435):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l38.place_forget()
                        f22l39.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==37 and z==t436):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l39.place_forget()
                        f22l40.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==38 and z==t437):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l40.place_forget()
                        f22l41.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==39 and z==t438):
                        f22l500.place_forget()
                        f22e1.delete(0,END)
                        f22l41.place_forget()
                        f22l42.place(x=45,y=75)
                        self.lel20+=1
                        ca=0
                    elif(self.lel20==40 and z==t439):
                        f22l42.place_forget()
                        f22e1.delete(0,END)
                        frame22.pack_forget()
                        frame23.pack()
                        self.lel20+=1
                        ca=0
                elif(ca==1):
                    f22l500.place(x=45,y=200)
                    ca=1
        def gam1(n,l):
            a=choice(l)
            t0=l.index(a)
            l.remove(a)
            un=''
            g=0;g1=0
            for h in a:
                k=randint(1,2);rd=randint(1,2)
                if(k==rd and g<n-1):
                    un=un+'_'
                    g+=1
                elif(g1<n):
                    un=un+h
                    g1=g1 + 1
                else:
                    un=un+'_'
            return un+a

        #frame1
        frame1=Frame(root,bg='yellow')
        frame1.pack()
        frame1.config(width=245,height=360)
        root.config(bg='yellow')
        lb1=Label(frame1,text=' WELCOME \nTO \n MISSING \nLETTERS GAME',fg='orange',bg='yellow',font=('Courier',20,'bold'))
        lb1.place(x=25,y=100)
        btn=Button(frame1,text='Next',command=screen1_2)
        btn.place(x=100,y=300)
        #frame2
        frame2=Frame(root,bg='yellow')
        frame2.config(width=245,height=360)
        f2b1=Button(frame2,text='Next',command=screen2_3)
        f2b1.place(x=180,y=330)
        f2b2=Button(frame2,text='Back',command=screen2_1)
        f2b2.place(x=18,y=330)

        can=Canvas(frame2,bg='black',scrollregion=(0,0,0,500))
        can.place(x=20,y=25)
        can.config(width=179,height=295,bg='white')
        #scroll
        scrollbar = Scrollbar(frame2,orient=VERTICAL,command=can.yview)
        scrollbar.place(x=203,y=25,height=300)
        can.config(yscrollcommand=scrollbar.set)
        can.bind('<Configure>',lambda e: can.configure(scrollregion=can.bbox('all')))

        f1100=Frame(can)
        f1100.pack()
        can.create_window((0,0),window=f1100,anchor='nw')
        f1100.config(width=178,height=600,bg='yellow')

        f2b2=Button(f1100,text="LEVEL 1",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_3).place(x=1,y=0)
        f2b3=Button(f1100,text="LEVEL 2",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_4).place(x=1,y=29)
        f2b4=Button(f1100,text="LEVEL 3",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_5).place(x=1,y=58)
        f2b5=Button(f1100,text="LEVEL 4",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_6).place(x=1,y=88)
        f2b6=Button(f1100,text="LEVEL 5",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_7).place(x=1,y=118)
        f2b7=Button(f1100,text="LEVEL 6",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_8).place(x=1,y=148)
        f2b8=Button(f1100,text="LEVEL 7",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_9).place(x=1,y=178)
        f2b9=Button(f1100,text="LEVEL 8",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_10).place(x=1,y=208)
        f2b10=Button(f1100,text="LEVEL 9",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_11).place(x=1,y=238)
        f2b11=Button(f1100,text="LEVEL 10",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_12).place(x=1,y=268)
        f2b12=Button(f1100,text="LEVEL 11",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_13).place(x=1,y=298)
        f2b13=Button(f1100,text="LEVEL 12",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_14).place(x=1,y=328)
        f2b14=Button(f1100,text="LEVEL 13",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_15).place(x=1,y=358)
        f2b15=Button(f1100,text="LEVEL 14",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_16).place(x=1,y=388)
        f2b16=Button(f1100,text="LEVEL 15",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_17).place(x=1,y=418)
        f2b17=Button(f1100,text="LEVEL 16",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_18).place(x=1,y=448)
        f2b18=Button(f1100,text="LEVEL 17",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_19).place(x=1,y=478)
        f2b19=Button(f1100,text="LEVEL 18",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_20).place(x=1,y=508)
        f2b20=Button(f1100,text="LEVEL 19",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_21).place(x=1,y=538)
        f2b21=Button(f1100,text="LEVEL 20",width=21,fg='black',font=('Arieal',10,'bold'),command=screen2_22).place(x=1,y=568)

        #frame3


        frame3=Frame(root,bg='yellow')
        frame3.config(width=245,height=360)
        f3b1=Button(frame3,text='Next',command=level1)
        f3b1.place(x=180,y=330)
        f3b2=Button(frame3,text='Back',command=screen3_2)
        f3b2.place(x=18,y=330)
        l=['VANI', 'TARA', 'SAHA']
        un=''
        use=gam1(2,l)
        un=use[:4];t0=use[4:]
        f3l0=Label(frame3,text='LEVEL 1',fg='#01796F',bg='yellow',font=('Courier',20,'bold'))
        f3l0.place(x=65,y=15)
        f3l1=Label(frame3,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f3l1.place(x=75,y=75)
        f3l2=Label(frame3,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f3l2.place(x=15,y=114)
        f3v1=StringVar()
        f3e1=Entry(frame3,bd=3,width=17,fg='black')
        f3e1.place(x=85,y=115)
        un=''
        use=gam1(2,l)
        un=use[:4];t1=use[4:]
        f3l3=Label(frame3,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t2=use[4:]
        f3l4=Label(frame3,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f3b4=Button(frame3,text='i',width=2,command=tip)
        f3b4.place(x=195,y=113)

        f3l500=Label(frame3,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        #frame4
        frame4=Frame(root,bg='yellow')
        frame4.config(width=245,height=360)
        f4b1=Button(frame4,text='Next',command=level2)
        f4b1.place(x=180,y=330)
        f4b2=Button(frame4,text='Back',command=screen4_3)
        f4b2.place(x=18,y=330)
        l=['RAMA', 'VALI', 'KRTI', 'SITA', 'SAMA']
        un=''
        use=gam1(2,l)
        un=use[:4];t3=use[4:]
        f4l0=Label(frame4,text='LEVEL 2',fg='#01796F',bg='yellow',font=('Courier',20,'bold'))
        f4l0.place(x=65,y=15)
        f4l1=Label(frame4,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f4l1.place(x=75,y=75)
        f4l2=Label(frame4,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f4l2.place(x=15,y=114)
        f4v1=StringVar()
        f4e1=Entry(frame4,bd=3,width=17,fg='black')
        f4e1.place(x=85,y=115)
        un=''
        use=gam1(2,l)
        un=use[:4];t4=use[4:]
        f4l3=Label(frame4,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t5=use[4:]
        f4l4=Label(frame4,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f4b4=Button(frame4,text='i',width=2,command=tip)
        f4b4.place(x=195,y=113)
        f4l500=Label(frame4,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t6=use[4:]
        f4l5=Label(frame4,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t7=use[4:]
        f4l6=Label(frame4,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        #frame5
        frame5=Frame(root,bg='yellow')
        frame5.config(width=245,height=360)
        f5b1=Button(frame5,text='Next',command=level3)
        f5b1.place(x=180,y=330)
        f5b2=Button(frame5,text='Back',command=screen5_4)
        f5b2.place(x=18,y=330)
        l=['AMBA', 'JAYA', 'AMIT', 'KALI', 'ADYA', 'RAHU', 'LAVA']
        un=''
        use=gam1(2,l)
        un=use[:4];t8=use[4:]
        f5l0=Label(frame5,text='LEVEL 3',fg='#01796F',bg='yellow',font=('Courier',20,'bold'))
        f5l0.place(x=65,y=15)
        f5l1=Label(frame5,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f5l1.place(x=75,y=75)
        f5l2=Label(frame5,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f5l2.place(x=15,y=114)
        f5v1=StringVar()
        f5e1=Entry(frame5,bd=3,width=17,fg='black')
        f5e1.place(x=85,y=115)
        un=''
        use=gam1(2,l)
        un=use[:4];t9=use[4:]
        f5l3=Label(frame5,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t10=use[4:]
        f5l4=Label(frame5,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f5b4=Button(frame5,text='i',width=2,command=tip)
        f5b4.place(x=195,y=113)
        f5l500=Label(frame5,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t11=use[4:]
        f5l5=Label(frame5,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t12=use[4:]
        f5l6=Label(frame5,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t13=use[4:]
        f5l7=Label(frame5,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(2,l)
        un=use[:4];t14=use[4:]
        f5l8=Label(frame5,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        #frame6
        frame6=Frame(root,bg='yellow')
        frame6.config(width=245,height=360)
        f6b1=Button(frame6,text='Next',command=level4)
        f6b1.place(x=180,y=330)
        f6b2=Button(frame6,text='Back',command=screen6_5)
        f6b2.place(x=18,y=330)
        l=['KURMA', 'RADHA', 'ARUNA', 'TARUN', 'SUVAK', 'VIDYA', 'SADAS', 'PADMA', 'KHARA']
        un=''
        use=gam1(3,l)
        un=use[:5];t15=use[5:]
        f6l0=Label(frame6,text='LEVEL 4',fg='#01796F',bg='yellow',font=('Courier',20,'bold'))
        f6l0.place(x=65,y=15)
        f6l1=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f6l1.place(x=75,y=75)
        f6l2=Label(frame6,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f6l2.place(x=15,y=114)
        f6v1=StringVar()
        f6e1=Entry(frame6,bd=3,width=17,fg='black')
        f6e1.place(x=85,y=115)
        un=''
        use=gam1(3,l)
        un=use[:5];t16=use[5:]
        f6l3=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t17=use[5:]
        f6l4=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f6b4=Button(frame6,text='i',width=2,command=tip)
        f6b4.place(x=195,y=113)
        f6l500=Label(frame6,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t18=use[5:]
        f6l5=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t19=use[5:]
        f6l6=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t20=use[5:]
        f6l7=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t21=use[5:]
        f6l8=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t22=use[5:]
        f6l9=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t23=use[5:]
        f6l10=Label(frame6,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        #frame7
        frame7=Frame(root,bg='yellow')
        frame7.config(width=245,height=360)
        f7b1=Button(frame7,text='Next',command=level5)
        f7b1.place(x=180,y=330)
        f7b2=Button(frame7,text='Back',command=screen7_6)
        f7b2.place(x=18,y=330)
        l=['SALAN', 'NANDA', 'DEEPA', 'KRITI', 'ADITI', 'RUDRA', 'KALKI', 'KAMSA', 'ANISH', 'AARYA', 'KARNA']
        un=''
        use=gam1(3,l)
        un=use[:5];t24=use[5:]
        f7l0=Label(frame7,text='LEVEL 5',fg='#01796F',bg='yellow',font=('Courier',20,'bold'))
        f7l0.place(x=65,y=15)
        f7l1=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f7l1.place(x=75,y=75)
        f7l2=Label(frame7,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f7l2.place(x=15,y=114)
        f7v1=StringVar()
        f7e1=Entry(frame7,bd=3,width=17,fg='black')
        f7e1.place(x=85,y=115)
        un=''
        use=gam1(3,l)
        un=use[:5];t25=use[5:]
        f7l3=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t26=use[5:]
        f7l4=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f7b4=Button(frame7,text='i',width=2,command=tip)
        f7b4.place(x=195,y=113)
        f7l500=Label(frame7,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t27=use[5:]
        f7l5=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t28=use[5:]
        f7l6=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t29=use[5:]
        f7l7=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t30=use[5:]
        f7l8=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t31=use[5:]
        f7l9=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t32=use[5:]
        f7l10=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t33=use[5:]
        f7l11=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t34=use[5:]
        f7l12=Label(frame7,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))

        #frame8
        frame8=Frame(root,bg='yellow')
        frame8.config(width=245,height=360)
        f8b1=Button(frame8,text='Next',command=level6)
        f8b1.place(x=180,y=330)
        f8b2=Button(frame8,text='Back',command=screen8_7)
        f8b2.place(x=18,y=330)
        l=['KUNDI', 'YAJNA', 'UMIKA', 'JATIN', 'MANAH', 'AMEYA', 'KUSHA', 'GAURI', 'DEETA', 'AJAYA', 'NITYA', 'SHYLA','GANGA']
        un=''
        use=gam1(3,l)
        un=use[:5];t35=use[5:]
        f8l0=Label(frame8,text='LEVEL 6',fg='#01796F',bg='yellow',font=('Courier',20,'bold'))
        f8l0.place(x=65,y=15)
        f8l1=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f8l1.place(x=75,y=75)
        f8l2=Label(frame8,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f8l2.place(x=15,y=114)
        f8v1=StringVar()
        f8e1=Entry(frame8,bd=3,width=17,fg='black')
        f8e1.place(x=85,y=115)
        un=''
        use=gam1(3,l)
        un=use[:5];t36=use[5:]
        f8l3=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t37=use[5:]
        f8l4=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        f8b4=Button(frame8,text='i',width=2,command=tip)
        f8b4.place(x=195,y=113)
        f8l500=Label(frame8,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t38=use[5:]
        f8l5=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t39=use[5:]
        f8l6=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t40=use[5:]
        f8l7=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t41=use[5:]
        f8l8=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t42=use[5:]
        f8l9=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t43=use[5:]
        f8l10=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t44=use[5:]
        f8l11=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t45=use[5:]
        f8l12=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t46=use[5:]
        f8l13=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))
        un=''
        use=gam1(3,l)
        un=use[:5];t47=use[5:]
        f8l14=Label(frame8,text=un,fg='#FF0800',bg='yellow',font=('Courier',20,'bold'))



        #frame9
        frame9=Frame(root,bg='yellow')
        frame9.config(width=245,height=360)
        f9b1=Button(frame9,text='Next',command=level7)
        f9b1.place(x=180,y=330)
        f9b2=Button(frame9,text='Back',command=screen9_8)
        f9b2.place(x=18,y=330)
        l=['YADAVI', 'JANAKA', 'KAPILA', 'PRITHU', 'DILIPA', 'VARAHA', 'RAVANA', 'ANGADA', 'APARNA', 'DHEERA', 'TARITA', 'ANWITA', 'GUNINA', 'DEEPTA', 'BHAVYA']
        un=''
        use=gam1(4,l)
        un=use[:6];t48=use[6:]
        f9l0=Label(frame9,text='LEVEL 7',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f9l0.place(x=65,y=15)
        f9l1=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f9l1.place(x=75,y=75)
        f9l2=Label(frame9,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f9l2.place(x=15,y=114)
        f9v1=StringVar()
        f9e1=Entry(frame9,bd=3,width=17,fg='black')
        f9e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:6];t49=use[6:]
        f9l3=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t50=use[6:]
        f9l4=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f9b4=Button(frame9,text='i',width=2,command=tip)
        f9b4.place(x=195,y=113)
        f9l500=Label(frame9,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t51=use[6:]
        f9l5=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t52=use[6:]
        f9l6=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t53=use[6:]
        f9l7=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t54=use[6:]
        f9l8=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t55=use[6:]
        f9l9=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t56=use[6:]
        f9l10=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t57=use[6:]
        f9l11=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t58=use[6:]
        f9l12=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t59=use[6:]
        f9l13=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t60=use[6:]
        f9l14=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t61=use[6:]
        f9l15=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t62=use[6:]
        f9l16=Label(frame9,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))



        #frame10
        frame10=Frame(root,bg='yellow')
        frame10.config(width=245,height=360)
        f10b1=Button(frame10,text='Next',command=level8)
        f10b1.place(x=180,y=330)
        f10b2=Button(frame10,text='Back',command=screen10_9)
        f10b2.place(x=18,y=330)
        l=['BUDDHA', 'KIMAYA', 'PRAJNA', 'SATHWA', 'LASAKI', 'JATAYU', 'AMBUJA', 'ABHAYA', 'AUGADH', 'SAUMYA', 'MOHINI', 'SENANI', 'VIDURA', 'SUKETU', 'KUBERA', 'VETALI', 'SUBAHU']
        un=''
        use=gam1(4,l)
        un=use[:6];t63=use[6:]
        f10l0=Label(frame10,text='LEVEL 8',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f10l0.place(x=65,y=15)
        f10l1=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f10l1.place(x=75,y=75)
        f10l2=Label(frame10,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f10l2.place(x=15,y=114)
        f10v1=StringVar()
        f10e1=Entry(frame10,bd=3,width=17,fg='black')
        f10e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:6];t64=use[6:]
        f10l3=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t65=use[6:]
        f10l4=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f10b4=Button(frame10,text='i',width=2,command=tip)
        f10b4.place(x=195,y=113)
        f10l500=Label(frame10,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t66=use[6:]
        f10l5=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t67=use[6:]
        f10l6=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t68=use[6:]
        f10l7=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t69=use[6:]
        f10l8=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t70=use[6:]
        f10l9=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t71=use[6:]
        f10l10=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t72=use[6:]
        f10l11=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t73=use[6:]
        f10l12=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t74=use[6:]
        f10l13=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t75=use[6:]
        f10l14=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t76=use[6:]
        f10l15=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t77=use[6:]
        f10l16=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t78=use[6:]
        f10l17=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t79=use[6:]
        f10l18=Label(frame10,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        #frame11
        frame11=Frame(root,bg='yellow')
        frame11.config(width=245,height=360)
        frame11=Frame(root,bg='yellow')
        frame11.config(width=245,height=360)
        f11b1=Button(frame11,text='Next',command=level9)
        f11b1.place(x=180,y=330)
        f11b2=Button(frame11,text='Back',command=screen11_10)
        f11b2.place(x=18,y=330)
        l=['BHEEMA', 'UTTARA', 'RAMESH', 'LOUKYA', 'KESHAV', 'VAMIKA', 'MUKUND', 'VARADA', 'NAMISH', 'TANISI', 'AMBIKA', 'VARUNI', 'BHIMBA', 'WAMIKA', 'YAYATI', 'MENAKA', 'ANJANA', 'NAKULA', 'PAVAKI']
        un=''
        use=gam1(4,l)
        un=use[:6];t80=use[6:]
        f11l0=Label(frame11,text='LEVEL 9',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f11l0.place(x=65,y=15)
        f11l1=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f11l1.place(x=75,y=75)
        f11l2=Label(frame11,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f11l2.place(x=15,y=114)
        f11v1=StringVar()
        f11e1=Entry(frame11,bd=3,width=17,fg='black')
        f11e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:6];t81=use[6:]
        f11l3=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t82=use[6:]
        f11l4=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f11b4=Button(frame11,text='i',width=2,command=tip)
        f11b4.place(x=195,y=113)
        f11l500=Label(frame11,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t83=use[6:]
        f11l5=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t84=use[6:]
        f11l6=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t85=use[6:]
        f11l7=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t86=use[6:]
        f11l8=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t87=use[6:]
        f11l9=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t88=use[6:]
        f11l10=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t89=use[6:]
        f11l11=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t90=use[6:]
        f11l12=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t91=use[6:]
        f11l13=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t92=use[6:]
        f11l14=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t93=use[6:]
        f11l15=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t94=use[6:]
        f11l16=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t95=use[6:]
        f11l17=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t96=use[6:]
        f11l18=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t97=use[6:]
        f11l19=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t98=use[6:]
        f11l20=Label(frame11,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        #frame12
        frame12=Frame(root,bg='yellow')
        frame12.config(width=245,height=360)
        f12b1=Button(frame12,text='Next',command=level10)
        f12b1.place(x=180,y=330)
        f12b2=Button(frame12,text='Back',command=screen12_11)
        f12b2.place(x=18,y=330)
        l=['TATAKA', 'ROHINI', 'SURASA', 'BRAHMI', 'SUMALI', 'ADITYA', 'VAMANA', 'BALAKI', 'SARIKA', 'ARJUNA', 'VIRAVI', 'SUTADA', 'VINDHA', 'GIRIJA', 'GARUDA', 'KESARI', 'ANAGHA', 'MATSYA', 'BRINDA', 'ISHANI', 'ARYAHI']
        un=''
        use=gam1(4,l)
        un=use[:6];t99=use[6:]
        f12l0=Label(frame12,text='LEVEL 10',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f12l0.place(x=65,y=15)
        f12l1=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f12l1.place(x=75,y=75)
        f12l2=Label(frame12,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f12l2.place(x=15,y=114)
        f12v1=StringVar()
        f12e1=Entry(frame12,bd=3,width=17,fg='black')
        f12e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:6];t100=use[6:]
        f12l3=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t101=use[6:]
        f12l4=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f12b4=Button(frame12,text='i',width=2,command=tip)
        f12b4.place(x=195,y=113)
        f12l500=Label(frame12,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t102=use[6:]
        f12l5=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t103=use[6:]
        f12l6=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t104=use[6:]
        f12l7=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t105=use[6:]
        f12l8=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t106=use[6:]
        f12l9=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t107=use[6:]
        f12l10=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t108=use[6:]
        f12l11=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t109=use[6:]
        f12l12=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t110=use[6:]
        f12l13=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t111=use[6:]
        f12l14=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t112=use[6:]
        f12l15=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t113=use[6:]
        f12l16=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t114=use[6:]
        f12l17=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t115=use[6:]
        f12l18=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t116=use[6:]
        f12l19=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t117=use[6:]
        f12l20=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t118=use[6:]
        f12l21=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t119=use[6:]
        f12l22=Label(frame12,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))



        #frame13
        frame13=Frame(root,bg='yellow')
        frame13.config(width=245,height=360)
        f13b1=Button(frame13,text='Next',command=level11)
        f13b1.place(x=180,y=330)
        f13b2=Button(frame13,text='Back',command=screen13_12)
        f13b2.place(x=18,y=330)
        l=['AHALYA', 'URMILA', 'DEETYA', 'KUNTHI', 'SHAILA', 'ADITRI', 'APARAA', 'AKSHAJ']
        un=''
        use=gam1(4,l)
        un=use[:6];t120=use[6:]
        f13l0=Label(frame13,text='LEVEL 11',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f13l0.place(x=65,y=15)
        f13l1=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f13l1.place(x=75,y=75)
        f13l2=Label(frame13,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f13l2.place(x=15,y=114)
        f13v1=StringVar()
        f13e1=Entry(frame13,bd=3,width=17,fg='black')
        f13e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:6];t121=use[6:]
        f13l3=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t122=use[6:]
        f13l4=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f13b4=Button(frame13,text='i',width=2,command=tip)
        f13b4.place(x=195,y=113)
        f13l500=Label(frame13,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t123=use[6:]
        f13l5=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t124=use[6:]
        f13l6=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t125=use[6:]
        f13l7=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t126=use[6:]
        f13l8=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:6];t127=use[6:]
        f13l9=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        l=['PRANSHU', 'SAMPATI', 'DUSSAHA', 'DURJAYA', 'TOSHANI', 'RUKMINI', 'DURVASA', 'SHULINI', 'BHARATI', 'SUNABHA', 'PRAMATI', 'PADMESH', 'ANUSUYA', 'SAVITRI', 'ALOLUPA']
        un=''
        use=gam1(4,l)
        un=use[:7];t128=use[7:]
        f13l10=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t129=use[7:]
        f13l11=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t130=use[7:]
        f13l12=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t131=use[7:]
        f13l13=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t132=use[7:]
        f13l14=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t133=use[7:]
        f13l15=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t134=use[7:]
        f13l16=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t135=use[7:]
        f13l17=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t136=use[7:]
        f13l18=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t137=use[7:]
        f13l19=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t138=use[7:]
        f13l20=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t139=use[7:]
        f13l21=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t140=use[7:]
        f13l22=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t141=use[7:]
        f13l23=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t142=use[7:]
        f13l24=Label(frame13,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))


        #frame14
        frame14=Frame(root,bg='yellow')
        frame14.config(width=245,height=360)
        f14b1=Button(frame14,text='Next',command=level12)
        f14b1.place(x=180,y=330)
        f14b2=Button(frame14,text='Back',command=screen14_13)
        f14b2.place(x=18,y=330)
        l=['ATIKAYA', 'BHAIRAV', 'AVIGHNA', 'BHARATA', 'VIRJASA', 'SHABARI', 'PARMESH', 'TRIGUNA', 'SATYAKI', 'SHUBHAN', 'BAHVASI', 'ANAADIH', 'PARESHA', 'TRARITI', 'GAYATRI', 'VATVEGA', 'PRANAVA', 'ILAVIDA', 'SANJAYA', 'KRADHAN', 'KAVACHI', 'MARICHA', 'KASHTHA', 'VIKTANA', 'DURMADA']
        un=''
        use=gam1(4,l)
        un=use[:7];t143=use[7:]
        f14l0=Label(frame14,text='LEVEL 12',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f14l0.place(x=65,y=15)
        f14l1=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f14l1.place(x=75,y=75)
        f14l2=Label(frame14,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f14l2.place(x=15,y=114)
        f14v1=StringVar()
        f14e1=Entry(frame14,bd=3,width=17,fg='black')
        f14e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:7];t144=use[7:]
        f14l3=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t145=use[7:]
        f14l4=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f14b4=Button(frame14,text='i',width=2,command=tip)
        f14b4.place(x=195,y=113)
        f14l500=Label(frame14,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t146=use[7:]
        f14l5=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t147=use[7:]
        f14l6=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t148=use[7:]
        f14l7=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t149=use[7:]
        f14l8=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t150=use[7:]
        f14l9=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t151=use[7:]
        f14l10=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t152=use[7:]
        f14l11=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t153=use[7:]
        f14l12=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t154=use[7:]
        f14l13=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t155=use[7:]
        f14l14=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t156=use[7:]
        f14l15=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t157=use[7:]
        f14l16=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t158=use[7:]
        f14l17=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t159=use[7:]
        f14l18=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t160=use[7:]
        f14l19=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t161=use[7:]
        f14l20=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t162=use[7:]
        f14l21=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t163=use[7:]
        f14l22=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t164=use[7:]
        f14l23=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t165=use[7:]
        f14l24=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t166=use[7:]
        f14l25=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t167=use[7:]
        f14l26=Label(frame14,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))



        #frame15
        frame15=Frame(root,bg='yellow')
        frame15.config(width=245,height=360)
        f15b1=Button(frame15,text='Next',command=level13)
        f15b1.place(x=180,y=330)
        f15b2=Button(frame15,text='Back',command=screen15_14)
        f15b2.place(x=18,y=330)
        l=['CHITHRA', 'JAITHRA', 'THATAKA', 'HERAMBA', 'AEINDRI', 'KRISHNA', 'VANMAYI', 'SUKHADA', 'HAMSINI', 'SAMENDU', 'AYOBAHU', 'EVYAVAN', 'VIKARNA', 'MANDAVI', 'BHISHMA', 'UMAPATI', 'VIVITSU', 'HIDIMBI', 'DURVIGA', 'JAYAPAL', 'BHUDHAV', 'MANTRAM', 'SALYUDU', 'SUGRIVA', 'HANUMAN', 'KAIKEYI', 'TVARITA']
        un=''
        use=gam1(4,l)
        un=use[:7];t168=use[7:]
        f15l0=Label(frame15,text='LEVEL 13',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f15l0.place(x=65,y=15)
        f15l1=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f15l1.place(x=75,y=75)
        f15l2=Label(frame15,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f15l2.place(x=15,y=114)
        f15v1=StringVar()
        f15e1=Entry(frame15,bd=3,width=17,fg='black')
        f15e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:7];t169=use[7:]
        f15l3=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t170=use[7:]
        f15l4=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f15b4=Button(frame15,text='i',width=2,command=tip)
        f15b4.place(x=195,y=113)
        f15l500=Label(frame15,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t171=use[7:]
        f15l5=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t172=use[7:]
        f15l6=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t173=use[7:]
        f15l7=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t174=use[7:]
        f15l8=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t175=use[7:]
        f15l9=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t176=use[7:]
        f15l10=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t177=use[7:]
        f15l11=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t178=use[7:]
        f15l12=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t179=use[7:]
        f15l13=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t180=use[7:]
        f15l14=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t181=use[7:]
        f15l15=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t182=use[7:]
        f15l16=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t183=use[7:]
        f15l17=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t184=use[7:]
        f15l18=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t185=use[7:]
        f15l19=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t186=use[7:]
        f15l20=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t187=use[7:]
        f15l21=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t188=use[7:]
        f15l22=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t189=use[7:]
        f15l23=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t190=use[7:]
        f15l24=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t191=use[7:]
        f15l25=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t192=use[7:]
        f15l26=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t193=use[7:]
        f15l27=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t194=use[7:]
        f15l28=Label(frame15,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))


        #frame16
        frame16=Frame(root,bg='yellow')
        frame16.config(width=245,height=360)
        f16b1=Button(frame16,text='Next',command=level14)
        f16b1.place(x=180,y=330)
        f16b2=Button(frame16,text='Back',command=screen16_15)
        f16b2.place(x=18,y=330)
        l=['SUSHENA', 'VALLARI', 'UDDANDA', 'RAYIRTH', 'BHAVANI', 'TUMBURU', 'DEVESHI', 'SHRIHAN', 'VIRADHA', 'MANOMAY', 'AJITESH', 'ANUDARA', 'VAARAHI', 'SWAROOP', 'SURESHI', 'SUVARMA', 'SUMITRA']
        un=''
        use=gam1(4,l)
        un=use[:7];t195=use[7:]
        f16l0=Label(frame16,text='LEVEL 14',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f16l0.place(x=65,y=15)
        f16l1=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f16l1.place(x=75,y=75)
        f16l2=Label(frame16,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f16l2.place(x=15,y=114)
        f16v1=StringVar()
        f16e1=Entry(frame16,bd=3,width=17,fg='black')
        f16e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:7];t196=use[7:]
        f16l3=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t197=use[7:]
        f16l4=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f16b4=Button(frame16,text='i',width=2,command=tip)
        f16b4.place(x=195,y=113)
        f16l500=Label(frame16,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t198=use[7:]
        f16l5=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t199=use[7:]
        f16l6=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t200=use[7:]
        f16l7=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t201=use[7:]
        f16l8=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t202=use[7:]
        f16l9=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t203=use[7:]
        f16l10=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t204=use[7:]
        f16l11=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t205=use[7:]
        f16l12=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t206=use[7:]
        f16l13=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t207=use[7:]
        f16l14=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:7];t208=use[7:]
        f16l15=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:7];t209=use[7:]
        f16l16=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t210=use[7:]
        f16l17=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:7];t211=use[7:]
        f16l18=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        l=['RAMAKANT', 'RISHABHA', 'PRAHASTA', 'SARASANA', 'SAMAVART', 'BHASKARI', 'SAHADEVA', 'JAMBAVAN', 'MAYASURA', 'SATINDRA', 'SRIRUDRA', 'PITAMBAR']

        un=''
        use=gam1(4,l)
        un=use[:8];t212=use[8:]
        f16l19=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t213=use[8:]
        f16l20=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t214=use[8:]
        f16l21=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t215=use[8:]
        f16l22=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t216=use[8:]
        f16l23=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t217=use[8:]
        f16l24=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t218=use[8:]
        f16l25=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t219=use[8:]
        f16l26=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t220=use[8:]
        f16l27=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t221=use[8:]
        f16l28=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t222=use[8:]
        f16l29=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t223=use[8:]
        f16l30=Label(frame16,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))




        #frame17
        frame17=Frame(root,bg='yellow')
        frame17.config(width=245,height=360)
        f17b1=Button(frame17,text='Next',command=level15)
        f17b1.place(x=180,y=330)
        f17b2=Button(frame17,text='Back',command=screen17_16)
        f17b2.place(x=18,y=330)
        l=['INDRAJIT', 'JAYANTAH', 'AGRAYAYI', 'SURESHAM', 'PRAMODAN', 'NISHANGI', 'SHIVANNE', 'KAISHORI', 'KABANDHA', 'VIRABAHI', 'KUNDASHI', 'SIKANDHI', 'KUNDUSAI', 'AMEYATMA', 'AVANEESH', 'VASISTHA', 'VARALIKA', 'MALYAVAN', 'NAGAADAT', 'APARAJIT', 'MAHABAHU', 'SHANKHIN', 'BHARGAVI', 'SUBHADRA', 'ALAMPATA', 'MADHUBAN', 'SIDDHAMA', 'KAUSALYA', 'MAHODARA', 'GANDHARI', 'VISHRAVA']
        un=''
        use=gam1(4,l)
        un=use[:8];t224=use[8:]
        f17l0=Label(frame17,text='LEVEL 15',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f17l0.place(x=65,y=15)
        f17l1=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f17l1.place(x=75,y=75)
        f17l2=Label(frame17,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f17l2.place(x=15,y=114)
        f17v1=StringVar()
        f17e1=Entry(frame17,bd=3,width=17,fg='black')
        f17e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:8];t225=use[8:]
        f17l3=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t226=use[8:]
        f17l4=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f17b4=Button(frame17,text='i',width=2,command=tip)
        f17b4.place(x=195,y=113)
        f17l500=Label(frame17,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t227=use[8:]
        f17l5=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t228=use[8:]
        f17l6=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t229=use[8:]
        f17l7=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t230=use[8:]
        f17l8=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t231=use[8:]
        f17l9=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t232=use[8:]
        f17l10=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t233=use[8:]
        f17l11=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t234=use[8:]
        f17l12=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t235=use[8:]
        f17l13=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t236=use[8:]
        f17l14=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:8];t237=use[8:]
        f17l15=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:8];t238=use[8:]
        f17l16=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t239=use[8:]
        f17l17=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t240=use[8:]
        f17l18=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:8];t241=use[8:]
        f17l19=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t242=use[8:]
        f17l20=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t243=use[8:]
        f17l21=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t244=use[8:]
        f17l22=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t245=use[8:]
        f17l23=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t246=use[8:]
        f17l24=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t247=use[8:]
        f17l25=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t248=use[8:]
        f17l26=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t249=use[8:]
        f17l27=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t250=use[8:]
        f17l28=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t251=use[8:]
        f17l29=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t252=use[8:]
        f17l30=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t253=use[8:]
        f17l31=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t254=use[8:]
        f17l32=Label(frame17,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))




        #frame18
        frame18=Frame(root,bg='yellow')
        frame18.config(width=245,height=360)
        f18b1=Button(frame18,text='Next',command=level16)
        f18b1.place(x=180,y=330)
        f18b2=Button(frame18,text='Back',command=screen18_17)
        f18b2.place(x=18,y=330)
        l=['AASHIRYA', 'JAGADISH', 'DHUSSALA', 'DURMUKHA', 'UPANANDA', 'NAROTTAM', 'KAMALIKA', 'NITYANTA', 'PARIJATA', 'MAHAKRAM', 'AMBALIKA', 'KAVEESHA', 'UGRASENA', 'ASHUTOSH', 'SADASIVA', 'SUHASTHA', 'SAHISHNU', 'KAMAKSHI', 'SUVARCHA', 'NARSIMHA', 'BALARAMA', 'AKHURATH', 'SULOCHAN', 'AMRITAYA', 'MANTHARA', 'BHIMVEGA', 'EKALAVYA', 'PADMAKAR', 'KAKASURA', 'SHAMBUKA', 'DRAUPADI']
        un=''
        use=gam1(4,l)
        un=use[:8];t255=use[8:]
        f18l0=Label(frame18,text='LEVEL 16',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f18l0.place(x=65,y=15)
        f18l1=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f18l1.place(x=75,y=75)
        f18l2=Label(frame18,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f18l2.place(x=15,y=114)
        f18v1=StringVar()
        f18e1=Entry(frame18,bd=3,width=17,fg='black')
        f18e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:8];t256=use[8:]
        f18l3=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t257=use[8:]
        f18l4=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f18b4=Button(frame18,text='i',width=2,command=tip)
        f18b4.place(x=195,y=113)
        f18l500=Label(frame18,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t258=use[8:]
        f18l5=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t259=use[8:]
        f18l6=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t260=use[8:]
        f18l7=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t261=use[8:]
        f18l8=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t262=use[8:]
        f18l9=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t263=use[8:]
        f18l10=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t264=use[8:]
        f18l11=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t265=use[8:]
        f18l12=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t266=use[8:]
        f18l13=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t267=use[8:]
        f18l14=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:8];t268=use[8:]
        f18l15=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:8];t269=use[8:]
        f18l16=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t270=use[8:]
        f18l17=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t271=use[8:]
        f18l18=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:8];t272=use[8:]
        f18l19=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t273=use[8:]
        f18l20=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t274=use[8:]
        f18l21=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t275=use[8:]
        f18l22=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t276=use[8:]
        f18l23=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t277=use[8:]
        f18l24=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t278=use[8:]
        f18l25=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t279=use[8:]
        f18l26=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t280=use[8:]
        f18l27=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t281=use[8:]
        f18l28=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t282=use[8:]
        f18l29=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t283=use[8:]
        f18l30=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t284=use[8:]
        f18l31=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:8];t285=use[8:]
        f18l32=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        l=['LOHITAKSH', 'VASISHTHA']
        un=''
        use=gam1(4,l)
        un=use[:9];t286=use[9:]
        f18l33=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t287=use[9:]
        f18l34=Label(frame18,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))


        #frame19
        frame19=Frame(root,bg='yellow')
        frame19.config(width=245,height=360)
        f19b1=Button(frame19,text='Next',command=level17)
        f19b1.place(x=180,y=330)
        f19b2=Button(frame19,text='Back',command=screen19_18)
        f19b2.place(x=18,y=330)
        l=['VEDAKARTA', 'APARAJEET', 'CHITRANGA', 'PADMAPATI', 'DHANANJAY', 'URNANABHA', 'SASIREKHA', 'DEVANTAKA', 'JALADHIJA', 'HYMAVATHY', 'MANDODARI', 'VEERYAVAN', 'UGRASARVA', 'VRIDARAKA', 'MARICHUDU', 'CHAKRIKAA', 'INDRARJUN', 'DURADHARA', 'SARVATMAN', 'DIRGHABHU', 'NIRANJANA', 'SARVAYONI', 'PADMANABH', 'ANUVINDHA', 'SATKARTAR', 'SINHAYANA', 'MAHATEJAS', 'KAMALAKAR', 'SWAYAMBHU', 'SOMAKIRTI', 'SRIKANTHA', 'YASHVASIN', 'PARIKSHIT', 'HARIPRIYA', 'KICHAKUDU']
        un=''
        use=gam1(4,l)
        un=use[:9];t288=use[9:]
        f19l0=Label(frame19,text='LEVEL 17',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f19l0.place(x=65,y=15)
        f19l1=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f19l1.place(x=75,y=75)
        f19l2=Label(frame19,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f19l2.place(x=15,y=114)
        f19v1=StringVar()
        f19e1=Entry(frame19,bd=3,width=17,fg='black')
        f19e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:9];t289=use[9:]
        f19l3=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t290=use[9:]
        f19l4=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f19b4=Button(frame19,text='i',width=2,command=tip)
        f19b4.place(x=195,y=113)
        f19l500=Label(frame19,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t291=use[9:]
        f19l5=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t292=use[9:]
        f19l6=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t293=use[9:]
        f19l7=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t294=use[9:]
        f19l8=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t295=use[9:]
        f19l9=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t296=use[9:]
        f19l10=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t297=use[9:]
        f19l11=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t298=use[9:]
        f19l12=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t299=use[9:]
        f19l13=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t300=use[9:]
        f19l14=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:9];t301=use[9:]
        f19l15=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:9];t302=use[9:]
        f19l16=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t303=use[9:]
        f19l17=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t304=use[9:]
        f19l18=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:9];t305=use[9:]
        f19l19=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t306=use[9:]
        f19l20=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t307=use[9:]
        f19l21=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t308=use[9:]
        f19l22=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t309=use[9:]
        f19l23=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t310=use[9:]
        f19l24=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t311=use[9:]
        f19l25=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t312=use[9:]
        f19l26=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t313=use[9:]
        f19l27=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t314=use[9:]
        f19l28=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t315=use[9:]
        f19l29=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t316=use[9:]
        f19l30=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t317=use[9:]
        f19l31=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t318=use[9:]
        f19l32=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t319=use[9:]
        f19l33=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t320=use[9:]
        f19l34=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t321=use[9:]
        f19l35=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t322=use[9:]
        f19l36=Label(frame19,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))




        #frame20
        frame20=Frame(root,bg='yellow')
        frame20.config(width=245,height=360)
        f20b1=Button(frame20,text='Next',command=level18)
        f20b1.place(x=180,y=330)
        f20b2=Button(frame20,text='Back',command=screen20_19)
        f20b2.place(x=18,y=330)
        l=['SULOCHANA', 'SABAREESH', 'PANDURAJU', 'SHATAKSHI', 'SHRESHTHA', 'VAISHNAVI', 'UGRAYUDHA', 'AKSHOBHYA', 'BHUVANESH', 'PADMAKSHI', 'LAKSHMANA', 'DUSHKARNA', 'VYOMASURA', 'ABHIMANYU']
        un=''
        use=gam1(4,l)
        un=use[:9];t323=use[9:]
        f20l0=Label(frame20,text='LEVEL 18',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f20l0.place(x=65,y=15)
        f20l1=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f20l1.place(x=75,y=75)
        f20l2=Label(frame20,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f20l2.place(x=15,y=114)
        f20v1=StringVar()
        f20e1=Entry(frame20,bd=3,width=17,fg='black')
        f20e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:9];t324=use[9:]
        f20l3=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t325=use[9:]
        f20l4=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f20b4=Button(frame20,text='i',width=2,command=tip)
        f20b4.place(x=195,y=113)
        f20l500=Label(frame20,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:9];t326=use[9:]
        f20l5=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t327=use[9:]
        f20l6=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t328=use[9:]
        f20l7=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t329=use[9:]
        f20l8=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t330=use[9:]
        f20l9=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t331=use[9:]
        f20l10=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t332=use[9:]
        f20l11=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t333=use[9:]
        f20l12=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t334=use[9:]
        f20l13=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t335=use[9:]
        f20l14=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:9];t336=use[9:]
        f20l15=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        l=['SHISHUPALA', 'DASHARATHA', 'JARASANDHA', 'ADI-PURUSH', 'JALAGANDHA', 'DHARMARAJU', 'TARAKASURA', 'SURESHWARA', 'SHATRUGHNA', 'AADIYAKETU', 'CHITRASENA', 'SAMARENDRA', 'TRIVIKRAMA', 'HAYAGREEVA', 'EKAAKSHARA', 'DHUSHASANA', 'ANANTAJEET', 'YOGESHWARI', 'SATYABHAMA', 'JARASANGHA', 'MAHADHYUTA', 'BHIMARATHA', 'VIBHISHANA']
        un=''
        use=gam1(5,l)
        un=use[:10];t337=use[10:]
        f20l16=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t338=use[10:]
        f20l17=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t339=use[10:]
        f20l18=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(5,l)
        un=use[:10];t340=use[10:]
        f20l19=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t341=use[10:]
        f20l20=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t342=use[10:]
        f20l21=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t343=use[10:]
        f20l22=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t344=use[10:]
        f20l23=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t345=use[10:]
        f20l24=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t346=use[10:]
        f20l25=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t347=use[10:]
        f20l26=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t348=use[10:]
        f20l27=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t349=use[10:]
        f20l28=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t350=use[10:]
        f20l29=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t351=use[10:]
        f20l30=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t352=use[10:]
        f20l31=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t353=use[10:]
        f20l32=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t354=use[10:]
        f20l33=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t355=use[10:]
        f20l34=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t356=use[10:]
        f20l35=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t357=use[10:]
        f20l36=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t358=use[10:]
        f20l37=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t359=use[10:]
        f20l38=Label(frame20,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))




        #frame21
        frame21=Frame(root,bg='yellow')
        frame21.config(width=245,height=360)
        f21b1=Button(frame21,text='Next',command=level19)
        f21b1.place(x=180,y=330)
        f21b2=Button(frame21,text='Back',command=screen21_20)
        f21b2.place(x=18,y=330)
        l=['KUNDADHARA', 'CHITRAKSHA', 'SANTHANUDU', 'MAHISASURA', 'DIRGHAROMA', 'SURPANAKHA', 'UPACHITRAN', 'SAHASRAJIT', 'SHIVAPRIYA', 'BHANUMATHI', 'ASHWATHAMA', 'KARTIKEYAN', 'SURESHWARI', 'DATTATREYA', 'NARAKASURA', 'DURDHAESHA', 'BHAVAPRITA', 'LAVANASURA', 'DURMARSHAN']
        un=''
        use=gam1(4,l)
        un=use[:10];t360=use[10:]
        f21l0=Label(frame21,text='LEVEL 19',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f21l0.place(x=65,y=15)
        f21l1=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f21l1.place(x=75,y=75)
        f21l2=Label(frame21,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f21l2.place(x=15,y=114)
        f21v1=StringVar()
        f21e1=Entry(frame21,bd=3,width=17,fg='black')
        f21e1.place(x=85,y=115)
        un=''
        use=gam1(4,l)
        un=use[:10];t361=use[10:]
        f21l3=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t362=use[10:]
        f21l4=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        f21b4=Button(frame21,text='i',width=2,command=tip)
        f21b4.place(x=195,y=113)
        f21l500=Label(frame21,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))

        un=''
        use=gam1(4,l)
        un=use[:10];t363=use[10:]
        f21l5=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t364=use[10:]
        f21l6=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t365=use[10:]
        f21l7=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t366=use[10:]
        f21l8=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t367=use[10:]
        f21l9=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t368=use[10:]
        f21l10=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t369=use[10:]
        f21l11=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t370=use[10:]
        f21l12=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t371=use[10:]
        f21l13=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t372=use[10:]
        f21l14=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(4,l)
        un=use[:10];t373=use[10:]
        f21l15=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t374=use[10:]
        f21l16=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t375=use[10:]
        f21l17=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t376=use[10:]
        f21l18=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))

        un=''
        use=gam1(5,l)
        un=use[:10];t377=use[10:]
        f21l19=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:10];t378=use[10:]
        f21l20=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        l=['BILVANILAYA', 'VISHALAKSHI', 'BHAGYASHREE', 'BARBARIKUDU', 'FOUR-KUMARS', 'SUKRACHARYA', 'RAUDRAKARMA', 'DANALAKSHMI', 'KUMBHAKARNA', 'GHATOTKACHA', 'KUNDHADHARA', 'VISHVAMITRA', 'VISHALAKSHA', 'KRUPACHARYA', 'ANAGHRUSHYA', 'CHANDRARUPA', 'SHURPANAKHA', 'DHANURDHARA', 'RUDRAVEERYA', 'JAYALAKSHMI']

        un=''
        use=gam1(5,l)
        un=use[:11];t379=use[11:]
        f21l21=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t380=use[11:]
        f21l22=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t381=use[11:]
        f21l23=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t382=use[11:]
        f21l24=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t383=use[11:]
        f21l25=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t384=use[11:]
        f21l26=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t385=use[11:]
        f21l27=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t386=use[11:]
        f21l28=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t387=use[11:]
        f21l29=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t388=use[11:]
        f21l30=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t389=use[11:]
        f21l31=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t390=use[11:]
        f21l32=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t391=use[11:]
        f21l33=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t392=use[11:]
        f21l34=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t393=use[11:]
        f21l35=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t394=use[11:]
        f21l36=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t395=use[11:]
        f21l37=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t396=use[11:]
        f21l38=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t397=use[11:]
        f21l39=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t398=use[11:]
        f21l40=Label(frame21,text=un,fg='#FF0800',bg='yellow',font=('Courier',18,'bold'))




        #frame22
        frame22=Frame(root,bg='yellow')
        frame22.config(width=245,height=360)
        f22b1=Button(frame22,text='Next',command=level20)
        f22b1.place(x=180,y=330)
        f22b2=Button(frame22,text='Back',command=screen22_21)
        f22b2.place(x=18,y=330)
        l=['DHANVANTARI', 'DHURYODHANA', 'SHRUTAKIRTI', 'DRIDASANDHA', 'DURVIMOCHAN', 'DIRGHLOCHAN', 'SHIVANSHIKA', 'MAHALAKSHMI', 'DUSHPARAJAI', 'THAKSHAKUDU', 'BALVARDHANA', 'DRIDHAVARMA', 'PARASHURAMA', 'CHITRAVARMA', 'KUNDHABHEDI', 'MAMASAKHUNI']
        un=''
        use=gam1(5,l)
        un=use[:11];t399=use[11:]
        f22l0=Label(frame22,text='LEVEL 20',fg='#01796F',bg='yellow',font=('Courier',18,'bold'))
        f22l0.place(x=65,y=15)
        f22l1=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        f22l1.place(x=45,y=75)
        f22l2=Label(frame22,text='Enter:',fg='black',bg='yellow',font=('Courier',14,'bold'))
        f22l2.place(x=15,y=114)
        f22v1=StringVar()
        f22e1=Entry(frame22,bd=3,width=17,fg='black')
        f22e1.place(x=85,y=115)
        un=''
        use=gam1(5,l)
        un=use[:11];t400=use[11:]
        f22l3=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t401=use[11:]
        f22l4=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        f22b4=Button(frame22,text='i',width=2,command=tip)
        f22b4.place(x=195,y=113)
        f22l500=Label(frame22,text='WRONG ANSWER',fg='black',bg='yellow',font=('Courier',14,'bold'))

        un=''
        use=gam1(5,l)
        un=use[:11];t402=use[11:]
        f22l5=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t403=use[11:]
        f22l6=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t404=use[11:]
        f22l7=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t405=use[11:]
        f22l8=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t406=use[11:]
        f22l9=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t407=use[11:]
        f22l10=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t408=use[11:]
        f22l11=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t409=use[11:]
        f22l12=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t410=use[11:]
        f22l13=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t411=use[11:]
        f22l14=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t412=use[11:]
        f22l15=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t413=use[11:]
        f22l16=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:11];t414=use[11:]
        f22l17=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        l=['DRHONACHARYA', 'DHRITARASTRA', 'INDUSHEETALA', 'VIDYALAKSHMI', 'CHITHRAYUDHA', 'RISHYASRINGA', 'CHARUCHITHRA', 'SATHYASANDHA', 'DRIDHAHASTHA']
        un=''
        use=gam1(5,l)
        un=use[:12];t415=use[12:]
        f22l18=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))

        un=''
        use=gam1(5,l)
        un=use[:12];t416=use[12:]
        f22l19=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:12];t417=use[12:]
        f22l20=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))

        un=''
        use=gam1(5,l)
        un=use[:12];t418=use[12:]
        f22l21=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:12];t419=use[12:]
        f22l22=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:12];t420=use[12:]
        f22l23=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:12];t421=use[12:]
        f22l24=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:12];t422=use[12:]
        f22l25=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(5,l)
        un=use[:12];t423=use[12:]
        f22l26=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        l=['NARA-NARAYANA', 'SAGE-KAMBHOJA', 'LAXMANAKUMARA', 'DRIDHAKSHATRA', 'SRAVANA-KUMAR', 'HIRANYAKASIPA', 'VINDHYAVASINI', 'NARADA–NARADA', 'AKSHAYAKUMARA', 'CHITRAKUNDALA', 'VICHITRAVIRYA', 'VIJAYALAKSHMI']
        un=''
        use=gam1(6,l)
        un=use[:13];t424=use[13:]
        f22l27=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t425=use[13:]
        f22l28=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t426=use[13:]
        f22l29=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t427=use[13:]
        f22l30=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t428=use[13:]
        f22l31=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t429=use[13:]
        f22l32=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t430=use[13:]
        f22l33=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t431=use[13:]
        f22l34=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t432=use[13:]
        f22l35=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t433=use[13:]
        f22l36=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t434=use[13:]
        f22l37=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:13];t435=use[13:]
        f22l38=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        l=['DUSHPRASARSHAN', 'SOVANNA-MACCHA']
        un=''
        use=gam1(6,l)
        un=use[:14];t436=use[14:]
        f22l39=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        un=''
        use=gam1(6,l)
        un=use[:14];t437=use[14:]
        f22l40=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        l=['SEETHA-KALYANAM']
        un=''
        use=gam1(7,l)
        un=use[:15];t438=use[15:]
        f22l41=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        l=['DHRIDARATHASRAYA']
        un=''
        use=gam1(7,l)
        un=use[:16];t439=use[16:]
        f22l42=Label(frame22,text=un,fg='#FF0800',bg='yellow',font=('Courier',13,'bold'))
        #frame23
        frame23=Frame(root,bg='yellow')
        frame23.config(width=245,height=360)
        f23lb1=Label(frame23,text=' YOU ARE \n THE \n ULTIMATE \nPLAYER',fg='orange',bg='yellow',font=('Courier',20,'bold'))
        f23lb1.place(x=35,y=100)
        root.mainloop()
    def currency(self):
        def can(*e):
            n1=int(f2e1.get())
            cc1=str(v1.get())
            cc2=str(v2.get())
            if(cc1=='INR'):
                    if(cc2=='EUR'):
                            n2=n1*0.0114
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.0047
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*0.0123
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.0038
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*1.6001
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*0.0838
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*0.8428
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*2.8386
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*0.3685
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*0.6725
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='USD'):
                    if(cc2=='EUR'):
                            n2=n1*0.9211
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.377
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*80.984
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.3054
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*129.59
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*6.7845
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*68.25
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*229.88
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*29.84
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*54.46
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='KWD'):
                    if(cc2=='EUR'):
                            n2=n1*3.0154
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*1.2343
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*265.1327
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*3.2739
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*424.2397
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*22.2115
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*223.441
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*752.611
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*97.6921
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*178.2953
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='EUR'):
                    if(cc2=='EUR'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.4093
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*87.9154
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*1.0857
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.3316
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*140.69
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*7.3509
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*74.0622
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*249.5862
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*32.3974
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*59.1275
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='BHD'):
                    if(cc2=='BHD'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EUR'):
                            n2=n1*2.4429
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*214.7966
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*2.6523
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.8101
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*343.6969
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*17.9946
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*181.0203
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*609.7262
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*79.1451
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*144.4455
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='JPY'):
                    if(cc2=='EUR'):
                            n2=n1*0.0071
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.0029
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*0.6249
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*0.0077
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.0024
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*0.0523
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*1.0665
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*1.774
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*0.2303
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*0.4203
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='RUB'):
                    if(cc2=='EUR'):
                            n2=n1*0.0135
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.0055
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*1.1866
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*0.0147
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.0045
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*0.9376
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*0.0975
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*3.3683
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*0.4372
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*0.798
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='CNY'):
                    if(cc2=='EUR'):
                            n2=n1*0.136
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.0556
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*11.9367
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*0.1474
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.045
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*19.1002
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*10.2533
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*33.8839
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*4.3983
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*8.0272
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='EGP'):
                    if(cc2=='EUR'):
                            n2=n1*0.0309
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.0126
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*2.714
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*0.0335
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.0102
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*4.3426
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*0.2274
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*2.2872
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*7.7039
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*1.8251
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='PKR'):
                    if(cc2=='EUR'):
                            n2=n1*0.004
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.0016
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*0.3523
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*0.0044
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.0013
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*0.5637
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*0.0295
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*0.2969
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*0.1298
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1*0.2369
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
            elif(cc1=='PHP'):
                    if(cc2=='EUR'):
                            n2=n1*0.0169
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='BHD'):
                            n2=n1*0.0069
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='INR'):
                            n2=n1*1.487
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='USD'):
                            n2=n1*0.0184
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='KWD'):
                            n2=n1*0.0056
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='JPY'):
                            n2=n1*2.3794
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='CNY'):
                            n2=n1*0.1246
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='RUB'):
                            n2=n1*1.2532
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PKR'):
                            n2=n1*4.2211
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='EGP'):
                            n2=n1*0.5479
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
                    elif(cc2=='PHP'):
                            n2=n1
                            f2l1['text']=n2
                            f2l1.place(x=90,y=230)
        root=Tk()
        root.title('Hemu currency conv')
        root.minsize(width=240,height=360)
        root.maxsize(width=240,height=360)
        root.config(bg='black')
        def screen1_2():
                frame1.pack_forget()
                frame2.pack()
                                
        #frame1	
        frame1=Frame(root)
        frame1.pack()
        frame1.config(width=240,height=360,bg='black')
        lb=Label(frame1,text='WELCOME TO \nCURRENCY \nCONVETOR',bg='black',fg='white',font=('Arieal',15,'bold')).place(x=45,y=100)
        btn=Button(frame1,text='Next',command=screen1_2)
        btn.place(x=100,y=300)
        #frame2
        frame2=Frame(root,bg='black')
        frame2.config(width=240,height=360)
        Label(frame2,text='ENTER AMOUNT',bg='black',fg='blue',font=('Areial',13,'bold')).place(x=50,y=5)
        f2e1=Entry(frame2,bd=3)
        f2e1.place(x=50,y=50)
        Label(frame2,text='FROM',bg='black',fg='red',font=('Areial',13,'bold')).place(x=90,y=100)
        v1=StringVar()
        c1=ttk.Combobox(frame2,textvariable=v1)
        c1['values']=('USD','INR','KWD','EUR','BHD','JPY','RUB','CNY','EGP','PKR','PHP')
        c1.place(x=50,y=130)
        v1.trace('w',can)
        Label(frame2,text='TO',bg='black',fg='red',font=('Areial',13,'bold')).place(x=100,y=160)
        v2=StringVar()
        c2=ttk.Combobox(frame2,textvariable=v2)
        c2['values']=('USD','INR','KWD','EUR','BHD','JPY','RUB','CNY','EGP','PKR','PHP')
        c2.place(x=50,y=190)
        v2.trace('w',can)
        f2l1=Label(frame2,bg='black',fg='pink',font=('Arieal',13,'bold'))
        root.mainloop()
    def calender(self):
        ma=input('Enter Month Name:')
        ma=ma.upper()
        ye=int(input('Enter Year:'))
        lav=['JAN','FEB','AUG','SEPT','OCT','NOV','DEC']
        tr={0:'JANUARY',1:'FEBRUARY',2:'AUGUST',3:'SEPTEMBER',4:'OCTOBER',5:'NOVEMBER',6:'DECEMBER'}
        for i in range(len(lav)):
                if(ma==lav[i]):
                        dra=i
                        ma=tr[dra]

        def lep(n):
                if(n%100==0):
                        if(n%400==0):
                                return 'Y'
                        else:
                                return 'N'
                elif(n%4==0):
                        return 'Y'
                else:
                        return 'N'
        te1=lep(ye)
        try1=len(str(ye))
        em=' ';c=0;hun=1
        mon=['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        ma1={'JANUARY':6, 'FEBRUARY':2, 'MARCH':2, 'APRIL':5, 'MAY':0, 'JUNE':3, 'JULY':5, 'AUGUST':1, 'SEPTEMBER':4, 'OCTOBER':6, 'NOVEMBER':2, 'DECEMBER':4}
        if(te1=='N'):
                co1=ma1[ma]
        else:
                ma1['JANUARY']=5
                ma1['FEBRUARY']=1
                co1=ma1[ma]
        cly=[0, 400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000, 4400, 4800, 5200, 5600, 6000, 6400, 6800, 7200, 7600, 8000, 8400, 8800, 9200, 9600]
        cly1=[0,100,200,300,400]
        d1={100:5,200:3,300:1,400:0}
        for i in range(len(cly)):
            if(ye!=cly[i]):
                if(cly[i-1]<ye and ye<cly[i]):
                    cl=cly[i-1]
                    if(cl!=ye):
                        ge1=ye-cl
                        try1=len(str(ge1))
                        ra=True
            else:
                cat=0
                ra=False
                ge1=400
        for i in range(len(cly1)):
            if(ge1==cly1[i]):
                    hun=d1[ge1]
                    cat=hun
            if(ra==True and ge1!=cly1[i]):
                    if(cly1[i-1]<ge1 and ge1<cly1[i]):
                        cl1=cly1[i-1]
                        ge2=ge1-cl1
                        if(try1==3):
                            co2=d1[cl1]
                        else:
                            co2=0
                        ge3=(ge2//4)
                        ge4=ge2-ge3
                        ge5=ge3*2
                        ge6=(ge5+ge4)%7
                        cat=ge6+co2
        ge7=cat+co1+1
        ge8=ge7%7
        spa=ge8
        da1=['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        for i in da1:
            print(i,end='\t')
        print()
        c=0;j=0;del1=1
        for i in range(len(mon)):
            if(ma==mon[i]):
                if(i<8):
                        te=i
                else:
                        te=i+1
        dat1=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        dat0=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        emp=[' ',' ',' ',' ',' ',' ']
        cha=7-spa;la=1;del2=0
        for i in range(len(emp)):
            if(i<spa):
                print(emp[i],end='\t')
        for i in range(len(dat1)+spa+5):
            if(te%2==0 or te==7):
                if(del2==31):
                        break
                if(del1==1 and i<cha):
                        print(dat1[del2],end='\t')
                elif(del1==1 and i==cha):
                        del1=0
                        print()
                if(c<7 and del1==0):
                    print(dat1[del2],end='\t')
                    c+=1
                elif(c==7 and del1==0):
                    print()
                    c=0
                    del2-=1
            elif(te!=7 and te!=1):
                if(del2==30):
                        break
                if(del1==1 and i<cha):
                        print(dat1[del2],end='\t')
                elif(del1==1 and i==cha):
                        del1=0
                        print()
                if(c<7 and del1==0):
                    print(dat1[del2],end='\t')
                    c+=1
                elif(c==7 and del1==0):
                    print()
                    c=0
                    del2-=1
            elif(te==1):
                if(te1=='Y'):
                    if(i==32):
                        break
                    if(del1==1 and i<cha):
                        print(dat0[del2],end='\t')
                    elif(del1==1 and i==cha):
                        del1=0
                        print()
                    if(c<7 and del1==0):
                        print(dat0[del2],end='\t')
                        c+=1
                    elif(c==7 and del1==0):
                        print()
                        c=0
                        del2-=1
                else:
                    if(i==31):
                        break
                    if(del1==1 and i<cha):
                        print(dat1[del2],end='\t')
                    elif(del1==1 and i==cha):
                        del1=0
                        print()
                    if(c<7 and del1==0):
                        print(dat1[del2],end='\t')
                        c+=1
                    elif(c==7 and del1==0):
                        print()
                        c=0
                        del2-=1
            del2+=1
        input()
    def music_player(self):
        self.lis=[];self.te=0;self.pa=0;self.pla=0;self.old=[]
        mixer.init()
        def add():
            self.old=list(block.get(0,END))
            single=fd.askopenfilename(title='Select File',filetype=[('MP3 Files','*.mp3'),('All','*.*')])
            single1=str(single)
            l=list(block.get(0,END))
            if single1 not in self.lis:
                if(single1!=''):
                    self.lis.append(single1)
            c=single1.count('/')
            for i in range(c):
                f=single1.find('/')
                single1=single1[f+1:]
            if single1 not in l:
                if(single1!=''):
                    self.old.append(single1)
                    block.insert('end',single1)
        def fold():
            self.old=list(block.get(0,END))
            multiple=fd.askopenfilenames(parent=root,title='Select Files')
            out=root.splitlist(multiple)
            out=list(set(out))
            l=list(block.get(0,END))
            if(len(out)!=0):
                for single1 in out:
                    if single1 not in self.lis:
                        self.lis.append(single1)
                        c=single1.count('/')
                        for i in range(c):
                            f=single1.find('/')
                            single1=single1[f+1:]   
                        block.insert('end',single1)
                        self.old.append(single1)
        def play(e):
            global a;global dis;global sonlen
            frame1.pack_forget()
            frame2.pack(fill='both',expand=True)
            l=list(block.get(0,END))
            if(self.te==0):
                a=block.get(ACTIVE)
                self.te=1
            for i in range(len(l)):
                b=self.lis[i].find(a)
                if(b!=-1):
                    dis=i
                    son=self.lis[i]
                    break
            if(self.pa==0):
                mixer.music.load(son)
                mixer.music.play()
                self.pa=1
            else:
                mixer.music.unpause()
            mp3sa=MP3(son)
            sonlen=mp3sa.info.length
            f1sc.config(to=sonlen,value=0)
            h=int(sonlen/3600)
            m=int(sonlen/60)
            s=int(sonlen%60)
            sonlab.config(text=a)
            f1l1.config(text=f'%02d:%02d:%02d'%(h,m,s))
            f1b2.place_forget()
            f1b1.place(x=150,y=270)
            if(round((mixer.music.get_pos()/1000),1)==round(sonlen,1)):
                nextso()
            self.pla=0
            Thread(target=slide).start()
        def slide():
            global sonlen
            f1sc.config(value=(mixer.music.get_pos()/1000))
            h=int(f1sc.get()/3600)
            m=int(f1sc.get()/60)
            s=int(f1sc.get()%60)
            f1l2.config(text=f'%02d:%02d:%02d'%(h,m,s))
            if(self.pla==0):
                f1sc.after(1,slide)
            if(int(f1sc.get())==int(sonlen)):
                nextso()
        def pause():
            global paus;
            self.pa=1;self.pla=1
            mixer.music.pause()
            f1b1.place_forget()
            f1b2.place(x=150,y=270)
        def nextso():
            global a;global sonlen
            self.pla=0
            l=list(block.get(0,END))
            f1b2.place_forget()
            f1b1.place(x=150,y=270)
            i=0
            while(i<len(self.lis)):
                b=self.lis[i].find(a)
                if(b!=-1):
                    if(i+1<=len(self.lis)-1):
                        son=self.lis[i+1]
                        a=son
                        break
                    elif(i==len(self.lis)-1):
                        i=0
                        son=self.lis[i]
                        a=son
                i+=1
            mixer.music.load(son)
            mixer.music.play()
            mp3sa=MP3(son)
            sonlen=mp3sa.info.length
            h=int(sonlen/3600)
            m=int(sonlen/60)
            s=int(sonlen%60)
            sonlab.config(text=a)
            f1l1.config(text=f'%02d:%02d:%02d'%(h,m,s))
            f1sc.config(to=sonlen,value=0)
            Thread(target=slide).start()
        def previ():
            global a;global sonlen
            self.pla=0
            f1b2.place_forget()
            f1b1.place(x=150,y=270)
            l=list(block.get(0,END))
            i=len(self.lis)-1
            while(i>-1):
                b=self.lis[i].find(a)
                if(b!=-1):
                    if(i-1>=0):
                        son=self.lis[i-1]
                        a=son
                        break
                    elif(i==0):
                        i=len(self.lis)-1
                        son=self.lis[i]
                        a=son
                i-=1
            mixer.music.load(son)
            mixer.music.play()
            mp3sa=MP3(son)
            sonlen=mp3sa.info.length
            h=int(sonlen/3600)
            m=int(sonlen/60)
            s=int(sonlen%60)
            sonlab.config(text=a)
            f1l1.config(text=f'%02d:%02d:%02d'%(h,m,s))
            f1sc.config(to=sonlen,value=0)
            Thread(target=slide).start()
        def save():
            filet1=open('text1.db','wb')
            dump(self.lis,filet1)
            filet1.close()
            filet1_2=open('text1.db','rb')
            a=load(filet1_2)
            filet1_2.close()
            lov=list(block.get(0,END))
            file=open('text.db','wb')
            dump(lov,file)
            file.close()
            file2=open('text.db','rb')
            a=load(file2)
            file2.close()
            root.destroy()
        def volplac(a):
            change=1.0-(f1vol.get()/100)
            mixer.music.set_volume(change)
            f1vol1.config(text=f'%3d'%int(100-f1vol.get()))
        def back(ev):
            global a;global dis
            self.pa=0;self.te=0
            frame2.pack_forget()
            frame1.pack()
            l=list(block.get(0,END))
            single1=a
            c=single1.count('/')
            for i in range(c):
                f=single1.find('/')
                single1=single1[f+1:]
            for i in range(len(l)):
                if(l[i]==single1):
                    naa=i
            block.selection_clear(dis)
            block.activate(naa)
            block.select_set(naa)

        def shuffle():
            shuff=[]
            f1bb3.place_forget()
            f1bb2.place(x=0,y=270)
            l=list(block.get(0,END))
            block.delete(0,END)
            i=0
            while(len(l)):
                a=choice(l)
                block.insert(END,a)
                shuff.append(a)
                l.remove(a)
                i+=1
        def unshuffle():
            f1bb2.place_forget()
            f1bb3.place(x=0,y=270)
            block.delete(0,END)
            for i in range(len(self.old)):
                block.insert(END,self.old[i])
        def men_pop(eve):
            popup.tk_popup(eve.x_root,eve.y_root)
        def delet():
            
            l=block.curselection()
            la=list(block.get(0,END))
            for i in range(len(l)):
                fd=l[i]
            ba=str(la[fd])
            i=0
            while(i<len(self.lis)):
                b=self.lis[i].find(ba)
                if(b!=-1):
                    self.lis.remove(self.lis[i])
                    block.delete(l)
                i+=1
        root=Tk()
        root.title('Music Player')
        root.geometry('360x360')
        root.config(bg='black')
        root.resizable(0,0)
        mainmenu=Menu(root)
        root.config(menu=mainmenu)
        root.protocol('WM_DELETE_WINDOW',save)
        filemenu=Menu(mainmenu,tearoff=False)
        helpmenu=Menu(mainmenu,tearoff=False)
        mainmenu.add_cascade(label='Media', menu=filemenu)
        mainmenu.add_cascade(label='Help',menu=helpmenu)
        filemenu.add_command(label='Add Single File',command=add)
        filemenu.add_command(label='Add Multiple Files',command=fold)
        filemenu.add_separator()
        filemenu.add_command(label='Exit',command=save)
        helpmenu.add_cascade(label=u"\U0001F6C8 Support")
        #frame1
        frame1=Frame(root,bg='black')
        frame1.pack(fill='both',expand=True)
        scrol=Scrollbar(frame1,orient=VERTICAL)
        scrol.pack(side='right',fill='both')
        block=Listbox(frame1,width=60,height=100,font=('',12,'bold'),bd=0,selectbackground='blue',fg='black',bg='grey',yscrollcommand=scrol.set)
        block.pack(side='left',fill='both')
        scrol.config(command=block.yview)
        try:
            file1=open('text.db','rb')
            a=load(file1)
            file1.close()
            self.old=list(a)
            for i in a:
                block.insert(END,i)
            file6=open('text1.db','rb')
            a=load(file6)
            self.lis.extend(a)
            self.lis=list(set(self.lis))
            file6.close()
        except:
            pass
        block.bind('<Double-Button-1>',play)

        #frame2
        frame2=Frame(root)
        f1b1=Button(frame2,text='playing',bd=0,command=pause)
        f1b1.place(x=150,y=270)
        f1b2=Button(frame2,text='paused',bd=0,command=lambda:play('1'))
        f1b3=Button(frame2,text='next',bd=0,command=nextso)
        f1b3.place(x=250,y=270)
        f1b4=Button(frame2,text='previous',bd=0,command=previ)
        f1b4.place(x=50,y=270)
        f1sc=ttk.Scale(frame2,from_=0,length=260)
        f1sc.place(x=50,y=220)
        f1l1=Label(frame2,font=('Arieal',8))
        f1l1.place(x=311,y=220)
        f1l2=Label(frame2,font=('Arieal',8))
        f1l2.place(x=0,y=220)
        f1bb1=Button(frame2,text=u'\U0001F519',bd=0,font=('Helvactica',25))
        f1bb1.place(x=0,y=0)
        f1bb1.bind('<ButtonRelease-1>',back)
        f1bb2=Button(frame2,text=u'\U0001F500',bd=0,font=('',17,'bold'),command=unshuffle)
        sonlab=Label(frame2,text='',bd=0,font=('',15))
        sonlab.place(x=100,y=100)
        f1bb3=Button(frame2,text=u'\U0001F501',bd=0,font=('',17,'bold'),command=shuffle)
        f1bb3.place(x=0,y=270)

        v1=IntVar()
        v1.set(0)
        f1vol=ttk.Scale(frame2,from_=0,to=100,length=170,variable=v1,orient='vertical')
        f1vol.bind('<Button-1>',volplac)
        f1vol.bind('<ButtonRelease-1>',volplac)
        f1vol.bind('<Leave>',volplac)
        f1vol.bind('<Enter>',volplac)
        f1vol.place(x=320,y=30)
        f1vol1=Label(frame2,text='100',font=('Arieal',8))
        f1vol1.place(x=320,y=200)
        popup=Menu(block,tearoff=0)
        popup.add_command(label='Play',command=lambda:play(''))
        popup.add_command(label='Delete',command=delet)
        block.bind('<Button-3>',men_pop)


        root.mainloop()

    def rockpapergame(self):
        print("ROCK PAPER SCISSOR GAME:-")
        i=1;p=0;q=0;r=0;s=0;v=0;
        while(1):
            a=input("Enter Your Chooice:")
            x=['Rock','Paper','Scissor']
            c=a.capitalize()
            d=choice(x)
            print('Coputer Chooice:',d)
            if(c=='Rock' or c=='Paper' or c=='Scissor'):
                if(c=='Scissor' and d=='Rock'):
                    print('You lost..')
                    p+=1
                elif(c=='Rock' and d=='Paper'):
                    print('You lost')
                    q+=1
                elif(c=='Paper' and d=='Scissor'):
                    print('You lost')
                    r+=1
                elif(c==d):
                    print('Draw')
                    s+=1
                else:
                    print('You Won')
                    v+=1
            else:
                print("Please Enter Only from ROCK PAPER SCISSOR")
            e=input('''Choose the option:-
            Enter Any key - To close the game
            Enter N - To contiue the game again
            Enter Here: ''')
            if(e=='n' or e=='N'):
                pass
            else:
                break
            i+=1
        print('Number of Rounds You Played:',i)
        if((p+q+r)!=0):
            print('You LOST:',(p+q+r))
        if((s)!=0):
            print('DRAWS:',(s))
        if(v!=0):
            print('You WON:',v)
        print('******THANK YOU FOR PLAYING******')
        input()
    
    def magic_form(self):
        root=Tk()
        root.title('Magic Login')
        root.minsize(width=240,height=360)
        root.maxsize(width=240,height=360)
        def screen1_2():
            frame1.pack_forget()
            frame2.pack()
        def change(eve):
            self.te=str(f1e1.get());ta=str(f1e2.get())
            if(self.te=='' or ta==''):
                f1b1.place_forget()
                f1b3.place_forget()
                f1b2.place(x=25,y=300)
                f1b2.bind('<Enter>',cha)
                f1b3.bind('<Enter>',cha)
            else:
                f1b1.place_forget()
                f1b2.place_forget()
                f1b3.place(x=100,y=300)
        def cha(e):
            tr = str(f1e1.get());ta1=str(f1e2.get())
            if(tr=='' or ta1==''):
                f1b1.place_forget()
                f1b3.place_forget()
                f1b2.place(x=150,y=300)
                f1b2.bind('<Enter>',change)
                f1b3.bind('<Enter>',cha)
            else:
                f1b1.place_forget()
                f1b2.place_forget()
                f1b3.place(x=100,y=300)
        frame1=Frame(root,bg='black')
        frame1.config(width=240,height=360)
        frame1.pack()
        Label(frame1,text='Magic Login',bg='black',fg='green',font=('Areial',15,'bold')).place(x=65,y=2)
        Label(frame1,text='User Id :',bg='black',fg='blue',font=('Areial',13,'bold')).place(x=25,y=40)
        Label(frame1,text='Password :',bg='black',fg='blue',font=('Areial',13,'bold')).place(x=5,y=100)
        f1e1=Entry(frame1,bd=3,width=20)
        f1e1.place(x=100,y=40)
        f1e2=Entry(frame1,bd=3,width=20,show='*')
        f1e2.place(x=100,y=100)
        if(str(f1e1.get())!='' and str(f1e2.get())!=''):
            f1b2.place_forget()
            f1b3.place(x=100,y=300)
        f1b1=Button(frame1,text='Submit',fg='black',font=('Areial',8,'bold'))
        f1b1.bind('<Enter>',change)
        f1b1.place(x=180,y=300)
        f1b2=Button(frame1,text='Fill the form',fg='red',font=('Areial',8,'bold'))
        f1b2.bind('<Enter>',cha)
        f1b3=Button(frame1,text='Submit',fg='green',font=('Areial',8,'bold'),command=screen1_2)
        f1b3.bind('<Enter>',cha)
        frame2=Frame(root,bg='black')
        frame2.config(width=240,height=360)
        Label(frame2,text='Thank You',bg='black',fg='blue',font=('Areial',25,'bold')).place(x=25,y=130)
        root.mainloop()


##test1=Hemu()
##test1.propose()
##test1.music_player()
##test1.tictactoe()
##test1.simple_cal_gui()
##test1.virtualatm()
##test1.missinglettersgame()
##test1.currency()
##test1.calender()
##test1.rockpapergame()
##test1.magic_form()
##
