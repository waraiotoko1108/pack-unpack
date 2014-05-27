#coding=utf-8
import os,struct,re,fnmatch

def walk(dirname):
	filelist=[]
	for root,dirs,files in os.walk(dirname):
		for filename in files:
			fullname=os.path.join(root,filename) 
			filelist.append(fullname)
	return filelist

filelist = walk('.')
for filename in filelist:
	if not fnmatch.fnmatch(filename,'*.dat'):
		continue
	print filename
	if re.search('event2d',filename):
		filestartPtr = 0xF8
		split_str = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		minus = 22
	elif re.search('language',filename):
		continue
	elif re.search('MENU',filename):
		filestartPtr = 0x80
		split_str = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		minus = 31
	elif re.search('TITLE',filename):
		filestartPtr = 0x80
		split_str ='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		minus = 23
	elif re.search('battle',filename):
		filestartPtr = 0xF8
		split_str = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		minus = 22
	else:
		continue
	if(os.path.isdir(filename[:-4]) is False):
		os.makedirs(filename[:-4])
	sfile = open(filename,'rb')
	count = struct.unpack('<LL',sfile.read(8))[1]
	sfile.seek(8)
	# 分割出文件名及长度位置
	files_in_pack_list = sfile.read(filestartPtr - minus).rsplit(split_str)
	for x in xrange(len(files_in_pack_list)):
		if re.search('battle_pause.NCGR',files_in_pack_list[x]) and files_in_pack_list[x][7] is not '\x00':
			address,length = struct.unpack('<LL',('\x00'+files_in_pack_list[x])[0:8])
			files_in_pack_name=files_in_pack_list[x][7:]
		elif re.search('.NCBR',files_in_pack_list[x]):
			address,length = struct.unpack('<LL',files_in_pack_list[x][0:8])
			files_in_pack_name=files_in_pack_list[x][8:]+'.png'
		else:
			address,length = struct.unpack('<LL',files_in_pack_list[x][0:8])
			files_in_pack_name=files_in_pack_list[x][8:]
		print('filename:%s \r\nsize:%s' %(files_in_pack_name,str(length)))
		try:
			dfile = open(filename[:-4]+'\\'+files_in_pack_name.strip('\x00'),'wb')
		except Exception, e:
			print files_in_pack_list[x][8:]
			print e
			quit()
		sfile.seek(filestartPtr + address)
		byte = sfile.read(length)
		dfile.write(byte)
		dfile.close()
	sfile.close()
raw_input('type enter to exit')