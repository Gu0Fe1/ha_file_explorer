from qiniu import Auth, put_file, etag, BucketManager
import os, qiniu.config
from asgiref.sync import sync_to_async

class Qn():

    def __init__(self, access_key, secret_key, bucket_name, prefix, download):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.download = download
        self.q = Auth(access_key, secret_key)

    # 获取列表
    async def get_list(self, prefix):
        bucket = BucketManager(self.q)
        bucket_name = self.bucket_name
        # 前缀
        prefix = 'HomeAssistant/' + self.prefix
        # 列举条目
        limit = 50
        # 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
        delimiter = None
        # 标记
        marker = None
        ret, eof, info = await sync_to_async(bucket.list)(bucket_name, prefix, marker, limit, delimiter)
        # print(info)
        return {
            'download': self.download,
            'list': ret
        }

    # 上传
    async def upload(self, localfile):
        key = 'HomeAssistant/' + self.prefix + os.path.basename(localfile)
        token = self.q.upload_token(self.bucket_name, key, 3600)
        res = await sync_to_async(put_file)(token, key, localfile)
        print(res)
    
    # 删除
    async def delete(self, key):
        bucket = BucketManager(self.q)
        ret, info = await sync_to_async(bucket.delete)(self.bucket_name, key)
        print(info)