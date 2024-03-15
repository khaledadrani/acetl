# Example usage:
from source.common.gateways.file_systems.base import LocalFileSystem

local_fs = LocalFileSystem("D:\\Books\\")

# Getting data
# data = local_fs.get(list(local_fs.get_list())[0])
# print(data[:100])
ls = list(local_fs.get_list(pattern="*numpy*"))[:10]

for l in ls:
    print(l)
