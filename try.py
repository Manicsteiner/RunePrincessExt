import sys, os
import struct

def read_arc_file(filename):
    with open(filename, 'rb') as file:
        # 检查文件头部是否为 'ARC\20'
        file_header = file.read(4)
        if file_header != b'ARC\x20':
            print("Invalid file format")
            return

        # 读取filenum和filename_end
        filenum = struct.unpack('<I', file.read(4))[0]
        filename_end = struct.unpack('<I', file.read(4))[0]

        for i in range(1, filenum + 1):
            # 读取namestart, pagenum和filesize
            offset = 16 * i
            file.seek(offset)
            namestart, pagenum, filesize = struct.unpack('<III', file.read(12))

            # 读取filename
            file.seek(namestart)
            filename_bytes = b''
            while True:
                byte = file.read(1)
                if byte == b'\x00' or file.tell() > filename_end:
                    break
                filename_bytes += byte
            
            # 将filename按sjis编码解读为字符串
            filename = filename_bytes.decode('sjis')

            # 创建目录和文件并写入内容
            file_dir = os.path.join('ARC', os.path.dirname(filename))
            os.makedirs(file_dir, exist_ok=True)
            file_path = os.path.join(file_dir, os.path.basename(filename))
            with open(file_path, 'wb') as output_file:
                file.seek(pagenum * 2048)
                file_body = file.read(filesize)
                output_file.write(file_body)

            print(f"File {filename} extracted successfully.")

        print("Extraction completed.")

def cstr(s):
    p = "{}s".format(len(s))
    s = struct.unpack(p,s)[0]
    return str(s.replace(b"\x00",b"").replace(b"\xFE",b""),encoding = "sjis")

# 示例用法
# filename = input("请输入文件名：")
# read_arc_file(filename)
if __name__ =="__main__":
	if len(sys.argv) < 2 :
		print("usage: python ",sys.argv[0]," mpkfiles ")
		exit()
	files=[]
	files=sys.argv[1:]
	for k in files:
		read_arc_file(k)