#!/usr/bin/env python
# coding: utf-8

from tkinter import Tk     #copy
import hashlib          #hash
import getpass          #hidden input
import random              
import os                  
import time


def Main_help():
    _help="""[0]help :
[1]login 
[7]del user 
[8][9]exit 
"""
    return _help

def Login_help():
    _help="""[0]help 
[1]new : new password
[2]find : find password using tag
[3]look : look all passwords
[4]del : delete password
[5]rep : replace password or tag
[6]gen : generate a new password
[7]copy : copy a password
[8]back 
[9]exit """
    return _help

def detailed_help():
    _help="""
    This tool is very simple, the whole process can be operated by Numbers or words.
    When creating a new user, remember the key you set. The key is not displayed.
    All passwords and labels can be viewed at any time just by remembering the key.
    The new password number must be less than 64 bits or there will be an error.
    Same thing with labels.
    (no one would use a passwords > 64 bits, would they?)
    The saved files are encrypted by the SHA3 algorithm and theoretically uncrackable.
    Making good use of randomly generated passwords and one-click replication makes registration easier.
    Finally, thank you for your use.
    """
    return _help

def encryption(password,key):
    """
    password : Encrypted password/string required
    key : The hexadecimal hash value of the key
    Return the encrypted string
    """
    key=str(key)
    count=0
    out=''
    out+=chr(ord(key[0])+len(password)) #Encrypt the password length in the first place
    for i in key[1:]:
        if count==len(password):
            count=0
        out+=chr(ord(i)+ord(password[count]))  #Adds each bit of the password loop to the hash value of the key
        count+=1
    return out


def decryption(string,key):
    """
    string : Strings to be decrypted
    key : The hexadecimal hash value of the key
    Return the decrypted string
    """
    key=str(key)
    length=ord(string[0])-ord(key[0]) #Password length
    out=""
    lenstring=len(string)
    if lenstring>64:            #Prevents incoming text from being too long and causing bugs
        lenstring=64           #The password is no longer than 64 bits, so the decrypted string needs only 64 bits
    for i in range(1,lenstring):    #Loop out the password
        out+=chr(ord(string[i])-ord(key[i]))
    return out[:length]          #Intercept a password by its length


def re_sort(name,del_num=-1,rep_num=-1,_pw=None,_tag=None):
    '''Reorder the serial Numbers in the file
       name : file name
       del_num : The password sequence number to delete
       rep_num : The password sequence number that needs to be changed
       _pw,_tag：Changed password and label
     '''
    f=open(name,"r+",encoding="utf-8")
    line=[]
    line.append(f.readline())    #Remember the key on the first line
    count=1
    for i in f.readlines():
        if count==del_num:    #Skip the line to delete
            pass
        elif count==rep_num:   #change the line
            line.append("%d_____%s_____%s"%(count,_pw,_tag))     
        else:
            t=i.split("_____")
            line.append("%d_____%s_____%s"%(count,t[1],t[2]))
        count+=1
    f.close()
    with open(name,"w",encoding="utf-8") as f:    #overwrite file
        for i in line:
            f.write(i)


def new(f,key,_pw=None,_tag=None):
    '''f:file pointer
       key: hexadecimal hash value of the key
       _pw:Incoming password, if empty, enter
       _tag:Incoming tag, if empty, enter
       '''
    if _pw == None or _tag == None:
        pw=input("New password: (cancel if empty) :")
        if len(pw) == 0:
            return
        tag=input("tag:")
    else:
        pw=_pw
        tag=_tag
    for i in f.readlines():                     #Move the file pointer to the end
        pass
    if len(tag)>0:
        print("99_____%s_____%s"%(encryption(pw,key),encryption(tag,key)),file=f)    #reorder the index later
    else:
        print("99_____%s_____%s"%(encryption(pw,key),encryption("无",key)),file=f)
    print("succeed")


def find(f,key):
    '''f:file pointer
       key: hexadecimal hash value of the key'''
    tag=input("tag: (cancel if empty):")
    if len(tag) == 0:
        return
    for i in f.readlines()[1:]:
        t=i.split("_____")
        t[2]=decryption(t[2],key)
        if tag in t[2]:
            print(t[0],decryption(t[1],key),t[2])


def look(f,key):
    '''f:file pointer
       key: hexadecimal hash value of the key'''
    print("index password tag")
    for i in f.readlines()[1:]:
        t=i.split("_____")  
        print(t[0],decryption(t[1],key),decryption(t[2],key))



def del_pw(f,key):
    '''f:file pointer
       key: hexadecimal hash value of the key
       Returns the deleted password index'''
    num=input("Enter the password index to be deleted (return if empty)：")
    if len(num) == 0:
        return -1
    num=int(num)
    if num<1:
        print("wrong")
        return -1
    count=1
    for i in f.readlines()[1:]:
        if count==num:
            t=i.split("_____")
            print("the password is：")
            print(t[0],decryption(t[1],key),decryption(t[2],key))
            print("Enter yes or 1 to confirm, other to cancel")
            choice=input()
            if choice == "yes" or choice == "1":
                print("deleted")
                return num
            else:
                print("cancel")
                return -1
        count+=1
    print("password not found")
    return -1


def rep(f,key):
    '''f:文件指针
       key: hexadecimal hash value of the key
       return changed password and tag
    '''
    num=input("enter the index of password to be changed (cancel if empty)：")
    if len(num) == 0:
        return -1,None,None
    num=int(num)
    if num<1:
        print("wrong")
        return -1,None,None
    count=1
    for i in f.readlines()[1:]:
        if count==num:
            t=i.split("_____")
            print("the password and tag is：")
            print(t[0],decryption(t[1],key),decryption(t[2],key))
            print("1: change password and lag    2: change password only    3: change tag only ")
            choice=input()
            if choice == "1":
                _pw=input("new password：")
                _tag=input("new tag：")
                print("succeed")
                return count,encryption(_pw,key),encryption(_tag,key)+"\n"          
            if choice == "2":                                                       
                _pw=input("new password：")
                print("succeed")
                return count,encryption(_pw,key),t[2]
            if choice == "3":
                _tag=input("new tag：")
                print("succeed")
                return count,t[1],encryption(_tag,key)+"\n"
            else:
                print("back")
                return -1,None,None
        count+=1
    print("password not found")
    return -1,None,None


def gen(f,key):
    '''f:file pointer
       key:The hexadecimal hash value of the key
       Return the generated password and tag
    '''
    num=input("Enter the length of the password (cancel if empty)：")
    if len(num) == 0:
        return None,None
    num=int(num)
    if num<1:
        print("wrong")
        return None,None
    print("Please enter the password specification (multiple choices are available)")
    print("1：0~9     2：A~Z     3：a~z     4：Special symbols")
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
        print("wrong")
        return None,None
    symbol=['+','-','*','_',')','#',"~","`",'.',',','?','}']   
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
        print("The generated password is",out)
        print("Enter yes or 1 to confirm, other to generate another")
        print("If accepted, it is automatically copied to the clipboard and saved to a file")
        choice=input()
        if choice == "yes" or choice == "1" :
            clip=Tk()                             
            clip.withdraw()
            clip.clipboard_clear()
            clip.clipboard_append(out)
            clip.update()
            time.sleep(.2)
            clip.update()
            clip.destroy()
            tag=input("copied, please enter the tag:")
            return out,tag
        else:
            pass


def copy(f,key):
    '''f:file pointer
       key:The hexadecimal hash value of the key
    '''
    num=input("Enter the password index to be copied (cancel if empty)：")
    if len(num) == 0:
        return
    num=int(num)
    if num<1:
        print("wrong")
        return
    count=1
    for i in f.readlines()[1:]:
        if count==num:
            t=i.split("_____")
            print("the password to copy is：")
            print(decryption(t[1],key))
            print("Enter yes or 1 to confirm, other to cancel")
            choice=input()
            if choice == "yes" or choice == "1":
                clip=Tk()                             
                clip.withdraw()
                clip.clipboard_clear()
                clip.clipboard_append(decryption(t[1],key))
                clip.update()
                time.sleep(.2)
                clip.update()
                clip.destroy()
                print("copied")
                return
            else:
                print("cancel")
                return
        count+=1
    print("no password found")
    return


def login():
    """[0]help : 
[1]new : new password
[2]find : find password using tag
[3]look : look all passwords
[4]del : delete password
[5]rep : replace password or tag
[6]gen : generate a new password
[7]copy : copy a password
[8]back : 
[9]exit : """
    name=input("enter the user name：")
    if not os.path.exists(name):     
        f=open(name,"w",encoding='utf-8')
        print("create user success")
        key=hashlib.sha3_256(getpass.getpass("set the key：").encode('utf8')).hexdigest()   
        print(hashlib.sha3_256(key.encode('utf8')).hexdigest(),file=f)               
    else:
        f=open(name,"r+",encoding='utf-8')
        key=hashlib.sha3_256(getpass.getpass("enter the key：").encode('utf8')).hexdigest()
        if hashlib.sha3_256(key.encode('utf8')).hexdigest()[:64]!=f.readline()[:64]:     
            print("key wrong！")
            return
        else:
            print("key right")
    f.close()
    _help=Login_help()
    print(_help)
    flag = 1                
    while True:
        _help=Login_help()
        if flag == 1:
            f=open(name, mode='r+',encoding='utf-8')
            flag = 0
        else:
            f.seek(0)
        _input=input()
        if _input=="help" or _input=="0":                   
            print(_help)    
        elif _input=="new" or _input=="1":                  
            new(f,key)      
            f.close()
            re_sort(name)  
            flag = 1
        elif _input=="find" or _input=="2":                 
            find(f,key)     
        elif _input=="look" or _input=="3":                 
            look(f,key)     
        elif _input=="del" or _input=="4":                  
            num=del_pw(f,key)    
            f.close()
            re_sort(name,del_num=num) 
            flag = 1
        elif _input=="rep" or _input=="5":                  
            num,pw,tag=rep(f,key)      
            if num>0:
                f.close()
                re_sort(name,rep_num=num,_pw=pw,_tag=tag)
                flag=1
        elif _input=="gen" or _input=="6":                  
            pw,tag=gen(f,key)
            if pw != None:
                new(f,key,_pw=pw,_tag=tag)
                f.close()
                re_sort(name)
                flag=1
        elif _input=="copy" or _input=="7":                 
            copy(f,key)
        elif _input=="back" or _input=="8":                 
            f.close()
            break
        elif _input=="exit" or _input=="9":                 
            f.close()
            os._exit(1)
        else:
            print("wrong")
        print()


def del_user():
    name=input("Please enter the user name to be deleted：")
    if not os.path.exists(name):     
        print("The user was not found. Deletion failed")
        return
    else:
        f=open(name,"r+",encoding='utf-8')
        key=hashlib.sha3_256(getpass.getpass("enter the key：").encode('utf8')).hexdigest()
        if hashlib.sha3_256(key.encode('utf8')).hexdigest()[:64]!=f.readline()[:64]:
            print("wrong!")
            f.close()
            return
        else:
            print("sure to delete%s？\nEnter yes or 1 to confirm, other to cancel"%(name))
            f.close()
            choice=input()
            if choice=="yes" or choice=="1":
                os.remove(name)
            else:
                print("cancel")
                return


if __name__ == '__main__':
    """[0]help 
[1]login
[7]del user 
[8][9]exit 
"""
    print("Welcome")
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
            print("wrong")
        print()

