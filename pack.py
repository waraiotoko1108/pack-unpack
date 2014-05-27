#coding=utf-8
import os,struct,re,fnmatch,sys

def walk(dirname):
	filelist=[]
	for root,dirs,files in os.walk(dirname):
		for filename in files:
			fullname=os.path.join(root,filename) 
			filelist.append(fullname)
	return filelist

def getDirList(path):
	path = str(path)
	if bool(path) is False:
		return []
	path = path.replace("/","\\")
	if path[-1] != "\\":
		path = path+"\\"
	filelist = os.listdir(path)
	dirlist = [x for x in filelist if os.path.isdir(path+x)]
	return dirlist

if __name__ == "__main__":
	dirlist = getDirList('.')
	for i in xrange(len(dirlist)):
		if re.search('event2d',dirlist[i]):
			filestartPtr = 0xF8
			split_str = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		elif re.search('MENU',dirlist[i]):
			filestartPtr = 0x80
			split_str = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		elif re.search('TITLE',dirlist[i]):
			filestartPtr = 0x80
			split_str = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		elif re.search('battle',dirlist[i]):
			filestartPtr = 0xF8
			split_str = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		else:
			continue
		dfile = open(dirlist[i]+'.dat','wb')
		dfile.write('\x53\x53\x41\x4D')
		filelist = os.listdir('./'+dirlist[i])
		count = len(filelist)
		dfile.write(struct.pack('<L',count))
		fileaddresslist =['\x00\x00\x00\x00']
		total_filesize = 0
		for x in xrange(len(filelist)):
			dfile.write(fileaddresslist[x])
			filesize = os.path.getsize('./'+dirlist[i]+'/'+filelist[x])
			total_filesize += filesize+len(split_str)
			print ('filename:%s \r\nsize:%d' %(filelist[x],filesize))
			if re.search('.png',filelist[x]):
				filename = filelist[x][:-4]
			else:
				filename = filelist[x]
			dfile.write(struct.pack('<L',filesize)+filename)
			dfile.write(split_str)
			# dfile.seek(filestartPtr)
			fileaddresslist.append(struct.pack('<L',total_filesize))
		dfile.seek(filestartPtr)
		for z in xrange(len(filelist)):
			byte = open('./'+dirlist[i]+'/'+filelist[z],'rb').read()
			dfile.write(byte+split_str)
		dfile.close()
	quit()

