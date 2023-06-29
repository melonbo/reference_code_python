import os
import tarfile

def extract_tar_gz_files(directory):
    """
    递归地解压缩一个目录下的所有tar.gz文件
    """
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            # 如果是目录，则递归地处理子目录
            extract_tar_gz_files(filepath)
        elif filename.endswith(".tar.gz"):
            # 如果是tar.gz文件，则解压缩
            with tarfile.open(filepath, "r:gz") as tar_ref:
                for member in tar_ref.getmembers():
                    win_dir = os.path.dirname(filepath).replace('\\', '/')
                    linux_dir = os.path.dirname(member.name)
                    # dst_dir = os.path.join(win_dir, linux_dir)
                    dst_dir = win_dir+linux_dir
                    print(member.name)

                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    tar_ref.extract(member, path=win_dir)
                # print('extract to: ', os.path.dirname(filepath))
                # tar_ref.extractall(os.path.dirname(filepath))

# 指定要解压缩的目录
directory = r"F:\share\log\tj2-211-20230401\211-43.1"

# 解压缩所有tar.gz文件
extract_tar_gz_files(directory)

