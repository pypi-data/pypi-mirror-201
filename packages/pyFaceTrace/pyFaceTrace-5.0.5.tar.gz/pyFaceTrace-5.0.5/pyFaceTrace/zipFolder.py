import zipfile
import os

def zip_directory(directory_path, zip_path):
    """
    压缩指定目录

    :param directory_path: 要压缩的目录路径
    :param zip_path: 压缩文件保存路径
    """
    # 创建 ZipFile 对象并打开要写入的压缩文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 遍历指定目录下的所有文件和子目录
        for root, dirs, files in os.walk(directory_path):
            # 遍历当前目录下的所有文件
            for file in files:
                # 获取文件的绝对路径
                file_path = os.path.join(root, file)
                # 将文件添加到压缩文件中
                zip_file.write(file_path, os.path.relpath(file_path, directory_path))

# 示例用法
zip_directory('./train', 'train.zip')


