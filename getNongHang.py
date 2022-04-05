# -*- coding: utf-8 -*-
# @Time    : 2021-06-01 11:44
# @Author  : sanclark
# @Mail    : sanclark@qq.com \

import os

def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles

fList = GetFileFromThisRootDir(r'C:\Users\gmcc\Desktop\shua\ljs\0801-1008', 'txt')
rList = []
for fp in fList:
    eList = ['gbk', 'utf-8']
    suc = False
    for e in eList:
        try:
            with open(fp, 'r', encoding=e) as f:
                b = False
                for line in f:
                    if line.startswith('交易日期'):
                        b = True
                        continue
                    if b:
                        rList.append(line)
                suc = True
        except Exception as e:
            # print(repr(e))
            pass
        if suc:
            break
    if not suc:
        print("Fail {}".format(fp))
with open('nonghang1.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(rList))