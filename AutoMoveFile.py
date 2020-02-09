#! /usr/bin/env python
#-*- coding:utf-8 -*-
# coding: utf-8
# Author ：fireice
# Date ：2020/2/9 19:10
# Tool ：PyCharm

import os
import logging
import sys
import datetime
import shutil

class filemange:
    logfile = 'log.txt'
    filepath = '.'
    fileprefix = ['.mkv', '.mp4', '.rmvb']
    tmpfileprefix = ['.td', '.td.cfg', '.aria2', '.cfg']
    nottmpfilelist=[]
    def __init__(self, logfile, filepath, destfilepath,fileprefix=None,tmpfileprefix=None):
        time1_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        self.logfile = logfile + "_" + time1_str + ".log"
        self.filepath = filepath
        self.destfilepath = destfilepath
        if(fileprefix):
            self.fileprefix = fileprefix
        else:
            self.fileprefix = ['.mkv', '.mp4', '.rmvb']
        if (tmpfileprefix):
            self.tmpfileprefix = tmpfileprefix
        else:
            self.tmpfileprefix = ['.td', '.td.cfg', '.aria2', '.cfg']
    def printinfo(self):
        log = "\nFile Path is "+self.filepath +"\n"
        log = log + "File dest Path is "+self.destfilepath
        self.logoutput(log,"I")

    def mymovefile(self, srcfile, dstfile):
        if not os.path.isfile(srcfile):
            self.logoutput(("%s not exist!" % (srcfile)), 'I')
        else:
            fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
            if not os.path.exists(fpath):
                os.makedirs(fpath)  # 创建路径
            shutil.move(srcfile, dstfile)  # 移动文件
            self.logoutput(("move %s -> %s" % (srcfile, dstfile)), 'I')

    def istmpfile(self,filename):
        self.fuctionbegin(sys._getframe().f_code.co_name)
        print(os.path.splitext(filename))
        if(filename in self.nottmpfilelist or os.path.splitext(filename)[0] in self.nottmpfilelist):
            self.logoutput("    "+filename + " have been processed.", 'I')
            return False
        for tmppreifx in self.tmpfileprefix:
            if(os.path.exists(filename+tmppreifx)):
                self.logoutput("    "+filename+" is a tmp file.",'I')
                self.fuctionend(sys._getframe().f_code.co_name)
                return True
        self.nottmpfilelist.append(filename)
        self.logoutput("    "+filename + " is not a tmp file.",'I')
        self.fuctionend(sys._getframe().f_code.co_name)
        return False
    def fileid(self):
        self.fuctionbegin(sys._getframe().f_code.co_name)
        filelist = os.listdir(self.filepath)
        for file in filelist:
            self.logoutput("    Begin to process "+file + ".", 'I')
            if(file =="." or file ==".."):
                continue
            #print (os.path.splitext(file))
            if(os.path.splitext(file)[1] is not None and os.path.splitext(file)[1] in self.fileprefix):
                self.istmpfile(file)
            else:
                self.logoutput("        "+file + " dont math fileprefix .", 'I')
            self.logoutput("    End to process " + file + ".", 'I')
        self.fuctionend(sys._getframe().f_code.co_name)
    def fuctionbegin(self,fuctionname):
        log = "Begin Fuction "+ fuctionname +" "
        self.logoutput(log, 'I')
    def fuctionend(self,fuctionname):
        log = "End Fuction " + fuctionname +" "
        self.logoutput(log, 'I')

    def movefile(self):
        for file in self.nottmpfilelist:
            destpath = self.destfilepath +"/"+file
            self.mymovefile(file,destpath)

    def automovefile(self):
        file = open(self.logfile, encoding="gbk", mode="a")
        file.close()
        self.fuctionbegin(sys._getframe().f_code.co_name)
        self.printinfo()
        self.fileid()
        self.movefile()
        self.fuctionend(sys._getframe().f_code.co_name)
    def logoutput(self,content,level):
        #file = open(self.logfile, encoding="utf-8", mode="a")
        ''''' Output log to file and console '''
        # Define a Handler and set a format which output to file
        logging.basicConfig(
            level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
            #stream=file,
            format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
            datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
            filename=self.logfile,  # log文件名
            filemode='w')  # 写入模式“w”或“a”
        # Define a Handler and set a format which output to console

        console = logging.StreamHandler()  # 定义console handler
        console.setLevel(logging.INFO)  # 定义该handler级别
        formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
        console.setFormatter(formatter)
        # Create an instance
        logging.getLogger().addHandler(console)  # 实例化添加handler
        if(level=='D'):
            logging.debug(content)
        elif (level == 'W'):
            logging.warning(content)
        elif (level == 'E'):
            logging.error(content)
        elif (level == 'C'):
            logging.critical(content)
        else:
            logging.info(content)
        #file.close()

if __name__ == '__main__':
    path = '/srv/dev-disk-by-label-MEDIA/Download/TDDOWNLOAD'#"."
    destpath = '/srv/dev-disk-by-label-MEDIA/MOVIE' #"../MOVIE"
    p = filemange('automovefile',path,destpath)
    p.automovefile()
    print (p.nottmpfilelist)
    #logoutput('log.txt',"test",'D')