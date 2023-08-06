from minio import Minio
from io import BytesIO


class MinioUtility:
    def check_bucket(self, bucket_name):
        """ bucket是否存在
        s.check_bucket('test')"""
        return self.instance.bucket_exists(bucket_name)

    def get_buckets(self):
        """ 获取buckets
        s.get_buckets()    [Bucket('asiatrip'), Bucket('blog'), Bucket('music'), Bucket('resume'), Bucket('test')]
        """
        return self.instance.list_buckets()

    def rm_bucket(self, bucket_name):
        """ 删除bucket
        s.rm_bucket('asiatrip')
        """
        self.instance.remove_bucket(bucket_name)
        return('success')

    def add_bucket(self, bucket_name):
        """ 新增bucket
         s.add_bucket('test2')
        """
        self.instance.make_bucket(bucket_name)
        return 'success'

    def get_objects(self, bucket_name):
        """
        s.get_objects('music')    //object generator
        """
        return self.instance.list_objects(bucket_name)

    def get_object(self, bucket_name, obj_name):
        """
        s.get_object('music','周杰伦-夜曲.mp3')     //urllib3 http response
        """
        return self.instance.get_object(bucket_name,obj_name)

    def get_object_content(self, bucket_name, obj_name):
        """
        s.get_object('music','周杰伦-夜曲.mp3')     //object generator
        """
        return self.instance.select_object_content(bucket_name, obj_name)
    
    def add_object(self,bucket_name,obj_name,data,length=-1, **kwargs):
        """ 上传对象
        s.add_object('test','1.py','C:\\Users\\Administrator\\Desktop\\1.py')
        """
        self.instance.put_object(bucket_name,obj_name,data,length, part_size=6000000, **kwargs)
        return 'success'
    
    def add_object_by_file(self, bucket_name, obj_name,file_path):
        """ 上传对象
        s.add_object_by_file('test','1.py','C:\\Users\\Administrator\\Desktop\\1.py')
        """
        self.instance.fput_object(bucket_name, obj_name, file_path)
        return 'success'

    def get_object_info(self,bucket_name,obj_name):
        """ 上传对象
        s.get_object_info('music','下山.mp3')
        """
        return self.instance.stat_object(bucket_name,obj_name)

    def rm_object(self,bucket_name,obj_name):
        """ 删除对象
        s.rm_object('test','1.py')
        """
        self.instance.remove_object(bucket_name,obj_name)
        return 'success'


class Storage(MinioUtility):
    def __init__(self, minio_config):
        self.instance = Minio(secure=False, **minio_config)

    def upload_file(self, bucket, uri, file):
        self.add_object(bucket, uri, file)
    
    def upload_file_by_bytes(self, bucket, uri, bytes):
        self.add_object(bucket, uri, BytesIO(bytes))

    def download_file(self, path):
        path_layers = path.split('/')
        bucket = path_layers.pop(0)
        uri = ('/').join(path_layers)
        file = self.get_object(bucket, uri)
        return file
    
    def download_file_as_bytes(self, path):
        file = self.download_file(path)
        file_bytes = file.read()
        return file_bytes

    def remove_file(self, path):
        if not path:
            return 
        path_layers = path.split('/')
        bucket = path_layers.pop(0)
        uri = ('/').join(path_layers)
        self.rm_object(bucket, uri)


