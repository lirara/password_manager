#!/usr/bin/env python
# coding: utf-8

from tkinter import Tk     #实现复制
import hashlib          #hash加密
import getpass          #隐藏输入
import random              
import os                  
import time


def Main_help():
    _help="""[0]help : 帮助
[1]login : 登录
[7]del user : 删除账户
[8][9]exit : 退出程序
"""
    return _help

def Login_help():
    _help="""[0]help : 帮助
[1]new : 新建密码
[2]find : 查找密码
[3]look : 查看全部密码
[4]del : 删除密码
[5]rep : 更改密码或标签
[6]gen : 生成密码
[7]copy : 复制密码
[8]back : 返回
[9]exit : 退出程序"""
    return _help

def detailed_help():
    _help="""
    本工具十分简单，全程可仅由数字或单词操作。
    建立新用户时请牢记自己设的密钥，密钥为不显示输入。
    只需要记住密钥便可随时查看所有密码和标签。
    新建的密码位数需小于64位，不然会出错。标签同理。
    （应该没人会用那么长的密码吧？标签感觉64个字也够用了）
    保存的文件由SHA3算法加密，理论上无法破解。
    善用程序随机生成的密码以及一键复制可使注册更加轻松。
    最后感谢您的使用。
    """
    return _help

def encryption(password,key):
    """
    password : 需要加密的密码/字符串
    key : 密钥的16进制hash值
    返回加密后的字符串
    """
    key=str(key)
    count=0
    out=''
    out+=chr(ord(key[0])+len(password)) #将密码长度加密于第一位
    for i in key[1:]:
        if count==len(password):
            count=0
        out+=chr(ord(i)+ord(password[count]))  #将密码每一位循环加到密钥的hash值上
        count+=1
    return out


def decryption(string,key):
    """
    string : 需要解密的字符串
    key : 密钥的16进制hash值
    返回解密后的字符串
    """
    key=str(key)
    length=ord(string[0])-ord(key[0]) #解析密码长度
    out=""
    lenstring=len(string)
    if lenstring>64:            #防止传入文本过长导致bug
        lenstring=64           #密码不长于64位，故解密的字符串只需64位即可
    for i in range(1,lenstring):    #循环解出密码
        out+=chr(ord(string[i])-ord(key[i]))
    return out[:length]          #通过密码长度截取密码


def re_sort(name,del_num=-1,rep_num=-1,_pw=None,_tag=None):
    '''对文件里的序号进行重新排序
       name : 文件名
       del_num : 需要删除的密码，默认无
       rep_num : 需要更改的密码，默认无
       _pw,_tag：更改的密码和标签，rep_num>0时有效
     '''
    f=open(name,"r+",encoding="utf-8")
    line=[]
    line.append(f.readline())    #记下第一行的密钥
    count=1
    for i in f.readlines():
        if count==del_num:    #跳过需删除的一行
            pass
        elif count==rep_num:   #需更改的一行
            line.append("%d_____%s_____%s"%(count,_pw,_tag))     
        else:
            t=i.split("_____")
            line.append("%d_____%s_____%s"%(count,t[1],t[2]))
        count+=1
    f.close()
    with open(name,"w",encoding="utf-8") as f:    #重写文件
        for i in line:
            f.write(i)


def new(f,key,_pw=None,_tag=None):
    '''f:文件指针
       key:密钥的16进制hash值
       _pw:传入的密码，若为空则输入
       _tag:传入的标签，若为空则输入
       '''
    if _pw == None or _tag == None:
        pw=input("新建的密码：(无输入返回)：")
        if len(pw) == 0:
            return
        tag=input("该密码的标签:")
    else:
        pw=_pw
        tag=_tag
    for i in f.readlines():                     #移动文件指针至末尾
        pass
    if len(tag)>0:
        print("99_____%s_____%s"%(encryption(pw,key),encryption(tag,key)),file=f)    #后续再对序号进行重新排序
    else:
        print("99_____%s_____%s"%(encryption(pw,key),encryption("无",key)),file=f)
    print("新建成功，返回")


def find(f,key):
    '''f:文件指针
       key:密钥的16进制hash值'''
    tag=input("请输入标签（无输入返回）:")
    if len(tag) == 0:
        return
    for i in f.readlines()[1:]:
        t=i.split("_____")
        t[2]=decryption(t[2],key)
        if tag in t[2]:
            print(t[0],decryption(t[1],key),t[2])


def look(f,key):
    '''f:文件指针
       key:密钥的16进制hash值'''
    print("序号 密码  标签")
    for i in f.readlines()[1:]:
        t=i.split("_____")  
        print(t[0],decryption(t[1],key),decryption(t[2],key))



def del_pw(f,key):
    '''f:文件指针
       key:密钥的16进制hash值
       返回删除的密码序号'''
    num=input("输入要删除的密码序号（无输入返回）：")
    if len(num) == 0:
        return -1
    num=int(num)
    if num<1:
        print("输入错误，返回")
        return -1
    count=1
    for i in f.readlines()[1:]:
        if count==num:
            t=i.split("_____")
            print("要删除的密码是：")
            print(t[0],decryption(t[1],key),decryption(t[2],key))
            print("输入yes或者1确认，输入其他取消")
            choice=input()
            if choice == "yes" or choice == "1":
                print("已删除，返回")
                return num
            else:
                print("取消删除，返回")
                return -1
        count+=1
    print("未找到该密码，返回")
    return -1


def rep(f,key):
    '''f:文件指针
       key:密钥的16进制hash值
       返回更改后的密码和标签的序号和hash值
    '''
    num=input("输入要更改的密码或标签序号(无输入返回)：")
    if len(num) == 0:
        return -1,None,None
    num=int(num)
    if num<1:
        print("输入错误，返回")
        return -1,None,None
    count=1
    for i in f.readlines()[1:]:
        if count==num:
            t=i.split("_____")
            print("要更改的密码或标签是：")
            print(t[0],decryption(t[1],key),decryption(t[2],key))
            print("1：更改密码和标签     2：只更改密码     3：只更改标签     输入其他返回")
            choice=input()
            if choice == "1":
                _pw=input("输入新密码：")
                _tag=input("输入新标签：")
                print("修改成功")
                return count,encryption(_pw,key),encryption(_tag,key)+"\n"          #函数返回的字符串不带换行号
            if choice == "2":                                                       #为了方便后续文件写入加上换行号
                _pw=input("输入新密码：")
                print("修改成功")
                return count,encryption(_pw,key),t[2]
            if choice == "3":
                _tag=input("输入新标签：")
                print("修改成功")
                return count,t[1],encryption(_tag,key)+"\n"
            else:
                print("返回")
                return -1,None,None
        count+=1
    print("未找到该密码，返回")
    return -1,None,None


def gen(f,key):
    '''f:文件指针
       key:密钥的16进制hash值
       返回生成的密码和标签
    '''
    num=input("输入产生密码的位数（无输入返回）：")
    if len(num) == 0:
        return None,None
    num=int(num)
    if num<1:
        print("输入错误，返回")
        return None,None
    print("请输入密码规格（可多选）")
    print("1：数字     2：大写字母     3：小写字母     4：特殊符号")
    string=input()
    ls=[]
    if "1" in string:
        ls.append(1)
    if "2" in string:
        ls.append(2)
    if "3" in string:
        ls.append(3)
    if "4" in string:
        ls.append(4)
    if len(ls) == 0 :
        print("未选择密码规格，返回")
        return None,None
    symbol=['+','-','*','_',')','#',"~","`",'.',',','?','}']   #不是所有的特殊符号都能用作密码，这里只列出一部分
    while True:
        out=""
        i=0
        while i<num: 
            r=random.choice(ls)
            if r==1:
                out+=str(random.randint(0,9))
            elif r==2:
                out+=chr(random.randint(65,90))
            elif r==3:
                out+=chr(random.randint(97,122))
            elif r==4:
                out+=symbol[random.randint(0,len(symbol)-1)]
            i+=1
        print("产生的密码为",out)
        print("输入yes或者1接受，输入其他拒绝并重新产生密码")
        print("若接受会自动复制到剪贴板并保存到文件里")
        choice=input()
        if choice == "yes" or choice == "1" :
            clip=Tk()                             #复制到系统剪贴板
            clip.withdraw()
            clip.clipboard_clear()
            clip.clipboard_append(out)
            clip.update()
            time.sleep(.2)
            clip.update()
            clip.destroy()
            tag=input("已复制，请输入标签:")
            return out,tag
        else:
            pass


def copy(f,key):
    '''f:文件指针
       key:密钥的16进制hash值
    '''
    num=input("输入要复制的密码序号（无输入返回）：")
    if len(num) == 0:
        return
    num=int(num)
    if num<1:
        print("输入错误，返回")
        return
    count=1
    for i in f.readlines()[1:]:
        if count==num:
            t=i.split("_____")
            print("要复制的密码是：")
            print(decryption(t[1],key))
            print("输入yes或者1确定，输入其他取消")
            choice=input()
            if choice == "yes" or choice == "1":
                clip=Tk()                             #复制到系统剪贴板
                clip.withdraw()
                clip.clipboard_clear()
                clip.clipboard_append(decryption(t[1],key))
                clip.update()
                time.sleep(.2)
                clip.update()
                clip.destroy()
                print("已复制，返回")
                return
            else:
                print("取消复制，返回")
                return
        count+=1
    print("未找到该密码，返回")
    return


def login():
    """[0]help : 帮助
[1]new : 新建密码
[2]find : 查找密码
[3]look : 查看全部密码
[4]del : 删除密码
[5]rep : 更改密码或标签
[6]gen : 生成密码
[7]copy : 复制密码
[8]back : 返回
[9]exit : 退出程序"""
    name=input("请输入用户名：")
    if not os.path.exists(name):     #若文件不存在（该用户第一次登录）
        f=open(name,"w",encoding='utf-8')
        print("创建用户成功")
        key=hashlib.sha3_256(getpass.getpass("请设置密钥：").encode('utf8')).hexdigest()   #将一重加密的密钥用作密码加密
        print(hashlib.sha3_256(key.encode('utf8')).hexdigest(),file=f)               #保存两重加密后的密钥作登录验证
    else:
        f=open(name,"r+",encoding='utf-8')
        key=hashlib.sha3_256(getpass.getpass("请输入密钥：").encode('utf8')).hexdigest()
        if hashlib.sha3_256(key.encode('utf8')).hexdigest()[:64]!=f.readline()[:64]:     #文本有时会读取超过64位，选前64位比较
            print("密钥错误！")
            return
        else:
            print("密钥正确")
    f.close()
    _help=Login_help()
    print(_help)
    flag = 1                #1:打开文件 0:刷新文件指针
    while True:
        _help=Login_help()
        if flag == 1:
            f=open(name, mode='r+',encoding='utf-8')
            flag = 0
        else:
            f.seek(0)
        _input=input()
        if _input=="help" or _input=="0":                   #查看帮助
            print(_help)    
        elif _input=="new" or _input=="1":                  #新建密码
            new(f,key)      
            f.close()
            re_sort(name)   #新建密码后排序
            flag = 1
        elif _input=="find" or _input=="2":                 #寻找密码
            find(f,key)     
        elif _input=="look" or _input=="3":                 #查看全部密码
            look(f,key)     
        elif _input=="del" or _input=="4":                  #删除密码
            num=del_pw(f,key)    
            f.close()
            re_sort(name,del_num=num) #删除密码并排序
            flag = 1
        elif _input=="rep" or _input=="5":                  #更改密码或标签
            num,pw,tag=rep(f,key)      
            if num>0:
                f.close()
                re_sort(name,rep_num=num,_pw=pw,_tag=tag)
                flag=1
        elif _input=="gen" or _input=="6":                  #生成密码
            pw,tag=gen(f,key)
            if pw != None:
                new(f,key,_pw=pw,_tag=tag)
                f.close()
                re_sort(name)
                flag=1
        elif _input=="copy" or _input=="7":                 #复制
            copy(f,key)
        elif _input=="back" or _input=="8":                 #返回
            f.close()
            break
        elif _input=="exit" or _input=="9":                 #退出
            f.close()
            os._exit(1)
        else:
            print("输入无效")
        print()


def del_user():
    name=input("请输入需要删除的用户名：")
    if not os.path.exists(name):     #若文件不存在（该用户第一次登录）
        print("没有找到该用户，删除失败")
        return
    else:
        f=open(name,"r+",encoding='utf-8')
        key=hashlib.sha3_256(getpass.getpass("请输入密钥：").encode('utf8')).hexdigest()
        if hashlib.sha3_256(key.encode('utf8')).hexdigest()[:64]!=f.readline()[:64]:
            print("密钥错误！删除失败")
            f.close()
            return
        else:
            print("密钥正确，确定要删除%s？\n输入yes或者1确认，输入其他取消"%(name))
            f.close()
            choice=input()
            if choice=="yes" or choice=="1":
                os.remove(name)
            else:
                print("取消删除")
                return


if __name__ == '__main__':
    """[0]help : 帮助
[1]login : 登录
[7]del user : 删除账户
[8][9]exit : 退出程序
"""
    print("欢迎使用密码管理，请输入数字或字母选择")
    while True:
        _help=Main_help()
        print(_help)
        _input=input()
        if _input=="help" or _input=="0":
            _help=detailed_help()
            print(_help)
        elif _input=="login" or _input=="1":
            login()
        elif _input=="del user" or _input=="7":
            del_user()
        elif _input=="exit" or _input=="8" or _input=="9":
            os._exit(1)
        else:
            print("输入无效")
        print()

