from ..utils import import_or_install

import_or_install("petastorm")

from .pyspark_add_on import PySpark, PyArrow


from petastorm.etl.dataset_metadata import materialize_dataset
from petastorm.codecs import ScalarCodec, CompressedImageCodec, NdarrayCodec
from petastorm.unischema import dict_to_spark_row, Unischema, UnischemaField
from petastorm.codecs import ScalarCodec, CompressedImageCodec, NdarrayCodec

from glob import glob
import cv2
import logging


class ConvertFolderImage:
    """
    ConvertFolderImage would conver folder jpg/png to parquet/delta format.
    :param input_path: folder include ``png``, ``jpeg`` need to be convert
    :param output_path: output hdfs path maybe file: (local file) or hdfs: (datalake path)
    :param table_name: table_name store metadata ex: table1
    :param database: database datalake house ex: ftel_dwh_insights
    :param repartition: data will be repartition to target file size
    :param numPartition: number of part each user want to seperate
    :param file_format: parquet/delta
    :param compression: compression method for parquet file (zstd or default snappy)
    :param image_type: png or jpg
    :param image_color: size 3,2 or 1, shape of image have color is 3 or ...
    :param size: list size user want to resize or padding
    :param resize_mode: Default None not resize, if resize choosing padding or resize method
    
    Return:
    parquet/delta file at output_path
    
    # Test case 1, write with file:
    converter = ConvertFolderImage(
                  input_path="**/*.jpg",
                  input_recursive = True,
                  output_path = f"file:/home/duyvnc/image_storage/img_user_device_jpg",
                  image_type = 'jpg',
                  image_color = 3,
                  size = [(212,212),
                         (597, 597)],
                  resize_mode=None,
                 )

    converter.execute()

    # Test case 2, write with hdfs:
    converter = ConvertFolderImage(
                  input_path="**/*.jpg",
                  input_recursive = True,
                  output_path = f"hdfs://hdfs-cluster.datalake.bigdata.local:8020/user/duyvnc/image/img_user_device_jpg.parquet",
                  database = 'default',
                  table_name = 'img_user_device_jpg',
                  image_type = 'jpg',
                  image_color = 3,
                  size = [(212,212),
                         (597, 597)],
                 resize_mode=None,
                 )

    converter.execute()
    """
        
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=True,
        numPartition=4,
        file_format = 'parquet',
        compression = 'zstd',
        
        image_type = 'jpg',
        image_color = 3,
        size=[(720,360)],
        resize_mode=None,
        
        input_recursive = False,
        debug=False
    ):
        
        self.input_path = input_path
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.input_recursive = input_recursive
        self.image_type = image_type
        self.image_color = image_color
        self.size = size
        self.resize_mode = resize_mode
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
            
        
        
    def padding(self, img, expected_size, borderType=cv2.BORDER_REPLICATE):
        delta_width = expected_size[0] - img.shape[0]
        delta_height = expected_size[1] - img.shape[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        # padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
        
        logging.info(f"Padding image: {img.shape[0]}, {img.shape[1]}")
        return cv2.copyMakeBorder(img, pad_width, delta_width - pad_width, pad_height, delta_height - pad_height, borderType)
    
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if 'file:' in output_path:
            spark_df.coalesce(numPartition) \
                    .write \
                    .format(file_format) \
                    .option('compression', compression) \
                    .mode('overwrite') \
                    .option("path", output_path) \
                    .save()
        else:
            
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            spark_df.coalesce(numPartition) \
                    .write \
                    .format(file_format) \
                    .option('compression', compression) \
                    .mode('overwrite') \
                    .option("path", output_path) \
                    .saveAsTable(database + '.' + table_name)       
                
    
    def create_dataframe(self, spark, ImageSchema, image_files,
                        output_path,
                        table_name, 
                        database,
                        size=(720,360), 
                        resize_mode='padding',
                        numPartition=8,
                        compression='zstd'):
        ROWGROUP_SIZE_MB = 128
        # with materialize_dataset(spark, output_path, ImageSchema, ROWGROUP_SIZE_MB):
        if resize_mode == 'padding':
            input_rdd = spark.sparkContext.parallelize(image_files) \
                .map(lambda image_path:
                        {ImageSchema.path.name: image_path,
                         ImageSchema.size.name: f"{cv2.imread(image_path).shape[0]}, {cv2.imread(image_path).shape[1]}",
                         ImageSchema.image.name: self.padding(cv2.imread(image_path), (size[0], size[1]))})

            rows_rdd = input_rdd.map(lambda r: dict_to_spark_row(ImageSchema, r))

            self.write_to_path(
                spark_df = spark.createDataFrame(rows_rdd, ImageSchema.as_spark_schema()),
                output_path = output_path,
                table_name=table_name, 
                database=database,
                numPartition=numPartition,
                compression=compression)

        elif resize_mode == 'resize':
            input_rdd = spark.sparkContext.parallelize(image_files) \
                .map(lambda image_path:
                        {ImageSchema.path.name: image_path,
                         ImageSchema.size.name: f"{cv2.imread(image_path).shape[0]}, {cv2.imread(image_path).shape[1]}",
                         ImageSchema.image.name: cv2.resize(cv2.imread(image_path), size[0], size[1])})

            rows_rdd = input_rdd.map(lambda r: dict_to_spark_row(ImageSchema, r))

            self.write_to_path(
                spark_df = spark.createDataFrame(rows_rdd, ImageSchema.as_spark_schema()),
                output_path = output_path,
                table_name=table_name, 
                database=database,
                numPartition=numPartition,
                compression=compression)

        else:
            try:
                logging.warning(f"Not resize image")
                input_rdd = spark.sparkContext.parallelize(image_files) \
                    .map(lambda image_path:
                            {ImageSchema.path.name: image_path,
                             ImageSchema.size.name: f"{cv2.imread(image_path).shape[0]}, {cv2.imread(image_path).shape[1]}",
                             ImageSchema.image.name: cv2.imread(image_path)})

                rows_rdd = input_rdd.map(lambda r: dict_to_spark_row(ImageSchema, r))

                self.write_to_path(
                    spark_df = spark.createDataFrame(rows_rdd, ImageSchema.as_spark_schema()),
                    output_path = output_path,
                    table_name=table_name, 
                    database=database,
                    numPartition=numPartition,
                    compression=compression)
            except Exception as e: 
                print(e)
                print("If get size error try to turn resize_mode='padding' or resize_mode='resize'")

                
                    
    def create_image_schema(self, size, image_type, image_color):
        """
        :param size: Image size, schema need to be consistency
        :param image_type: Image type is compress JPG or PNG
        :param image_color: 3 dimention color or 1 dimention colors
        """
        return Unischema('ImageSchema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('image', np.uint8, (size[0], size[1], image_color), CompressedImageCodec(image_type), False)
        ])
    
        # return Unischema('ImageSchema', [
        #     UnischemaField('path', np.string_, (), None, False),
        #     UnischemaField('image', np.uint8, (size[0], size[1], image_color), CompressedImageCodec(image_type), False)
        # ])
    
    
    def get_spark(self):
        return ss.PySpark(driver_memory='8G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
    
    def check_size(self, img, list_size):
        for s in list_size:
            if img.shape[0] <= s[0] and img.shape[1] <= s[1]:
                return s
        self.size.append(s)
        self.dict_image[(img.shape[0], img.shape[1])] = []
        return a
        #return (img.shape[0], img.shape[1])
    
    
    def execute(self):
        self.dict_image = {}
        for s in self.size:
            self.dict_image[s] = []
        
        if self.resize_mode and len(self.size) > 1:
            for p in sorted(glob(self.input_path, recursive=self.input_recursive)):
                img = cv2.imread(p)
                self.dict_image[self.check_size(img, self.size)].append(p)
        else:
            self.dict_image[self.size[0]] = sorted(glob(self.input_path, recursive=self.input_recursive))

        for s in self.size:
            if "." + self.file_format in self.output_path:
                output_path = self.output_path.replace("." + self.file_format, "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format))
            else:
                output_path = self.output_path + "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format)
            
            table_name = self.table_name + "_{s0}_{s1}".format(s0=str(s[0]), s1=str(s[1]))
            spark = self.get_spark()

            ImageSchema = self.create_image_schema(s, self.image_type, self.image_color)
            if self.dict_image[s]:
                logging.info(f"Write at path: {output_path}")
                logging.info(f"Save metadata at: {table_name}")
                self.create_dataframe(spark=spark,
                                      output_path=output_path,
                                      ImageSchema=ImageSchema,
                                      image_files=self.dict_image[s],
                                      size=s,
                                      table_name = table_name, 
                                      database=self.database,
                                      numPartition=self.numPartition,
                                      compression=self.compression)
                
class ConvertParquetToImage:
    """
    ConvertParquetToImage would conver folder parquet/delta format back to Image folder
    :param input_path: path to parquet file
    :param output_path: path user want to store image at
    :param write_mode: recovery convert back like original folder, all_in_one convert back all image in one folder
    :param database: database datalake house ex: ftel_dwh_insights
    :param table_name: table datalake house ex: table1
    
    Return:
    parquet/delta file at output_path    
    
    converter = ConvertParquetToImage(
    input_path = '/user/duyvnc/image/img_user_device_jpg_212_212.parquet',
    output_path = './abc'
    )

    converter.execute()
    """
    def __init__(
        self,
        input_path:str, 
        output_path:str,
        image_type = "jpg",
        write_mode = "recovery"
        debug = False
    ):
        
        self.input_path = input_path
        self.output_path = output_path
        self.image_type = image_type
        self.write_mode = write_mode
        self.debug = debug
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def check_delta(self, input_path):
        if "file:" in input_path:
            import os
            list_file = os.listdir(input_path)
            for f in list_file:
                if '_delta_log' in f:
                    return True
            return False
        else:
            list_file = ss.ls(input_path)
            for f in list_file:
                if '_delta_log' in f:
                    return True
            return False
        
    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
    def write_image_to_folder(self, row):
        if self.write_mode == "recovery":
            image_path = os.path.join(self.output_path, row.path)
        else:
            base_path = os.path.basename(str(row.path))
            image_path = os.path.join(self.output_path, base_path)
        self.mkdir_folder(os.path.dirname(image_path))
        img = cv2.imdecode(np.frombuffer(row.image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        cv2.imwrite(image_path, img)
            
    def execute(self):
        input_path = self.convert_to_hdfs_path(self.input_path)
        
        if self.check_delta(input_path):
            print("Delta File")
            df = ss.sql(f"""select * from delta.`{input_path}`""")
            df.foreach(self.write_image_to_folder)
        else:
            self.mkdir_folder(self.output_path)
            with make_reader(input_path) as reader:
                for row in reader:
                    # Create output_path
                    if self.write_mode == "recovery":
                        image_path = os.path.join(self.output_path, row.path)
                    else:
                        base_path = os.path.basename(str(row.path))
                        image_path = os.path.join(self.output_path, base_path)
                    self.mkdir_folder(os.path.dirname(image_path))
                    cv2.imwrite(image_path, row.image)
                
        print("Complete")
        
        
        
from abc import abstractmethod
from io import BytesIO
import logging

try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

import numpy as np


class DataframeColumnCodec(object):
    """The abstract base class of codecs."""

    @abstractmethod
    def encode(self, unischema_field, value):
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def decode(self, unischema_field, value):
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def spark_dtype(self):
        """Spark datatype to be used for underlying storage"""
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def __str__(self):
        """String representation sufficient to re-construct this Codec"""
        raise RuntimeError('Abstract method was called')
        
        
class VideoBinaryEncode(DataframeColumnCodec):
    """Encodes numpy ndarray into, or decodes an ndarray from, a spark dataframe field."""

    def encode(self, unischema_field, value):

        return bytearray(value)


    def decode(self, unischema_field, value):
        memfile = BytesIO(value)
        return np.load(memfile)

    def spark_dtype(self):
        # Lazy loading pyspark to avoid creating pyspark dependency on data reading code path
        # (currently works only with make_batch_reader). We should move all pyspark related code into a separate module
        import pyspark.sql.types as sql_types

        return sql_types.BinaryType()

    def __str__(self):
        """Represent this as the following form:
        >>> NdarrayCodec()
        """
        return f'{type(self).__name__}()'

class VideoCompress:
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=True,
        numPartition=1,
        file_format = 'parquet',
        compression = 'zstd',
        input_recursive = False,

        
        debug=False
    ):
        
        self.input_path = input_path
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.input_recursive = input_recursive
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        self.debug = debug
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if 'file:' in output_path:
            spark_df.coalesce(numPartition) \
                    .write \
                    .format(file_format) \
                    .option('compression', compression) \
                    .mode('overwrite') \
                    .option("path", output_path) \
                    .save()
        else:
            
            if table_name == '' or database == '':
                pass
            spark_df.coalesce(numPartition) \
                    .write \
                    .format(file_format) \
                    .option('compression', compression) \
                    .mode('overwrite') \
                    .option("path", output_path) \
                    .save()
                # raise ValueError("You must add table_name and database")
            # spark_df.coalesce(numPartition) \
            #         .write \
            #         .format(file_format) \
            #         .option('compression', compression) \
            #         .mode('overwrite') \
            #         .option("path", output_path) \
            #         .saveAsTable(database + '.' + table_name)  

            
    def row_generator(self, path):
        """Returns a single entry in the generated dataset. Return a bunch of random values as an example."""
        print(path)
        return {'path': path,
                'video': open(path, "rb").read()}
    
    def create_dataframe(self, spark, VideoSchema, input_files,
                        output_path,
                        table_name, 
                        database,
                        numPartition=8,
                        compression='zstd'):
        ROWGROUP_SIZE_MB = 1024
        # cap = cv2.VideoCapture(input_files)
        # size = (cap.get(3), cap.get(4))
        # total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    


        with materialize_dataset(spark, output_path, VideoSchema, ROWGROUP_SIZE_MB):
            rows_rdd = spark.sparkContext.parallelize(input_files) \
                .map(self.row_generator) \
                .map(lambda x: dict_to_spark_row(VideoSchema, x))

            self.write_to_path(
                        spark_df = spark.createDataFrame(rows_rdd, VideoSchema.as_spark_schema()),
                        output_path = output_path,
                        table_name = table_name, 
                        database = database,
                        numPartition = numPartition,
                        compression = compression
                    )
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
    def get_schema(self):
        return Unischema('VideoShema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('video', np.bytes_, (), VideoBinaryEncode(), False)
        ])
    
    def ingest(self):
        input_files = sorted(glob(self.input_path, recursive=self.input_recursive))
        
        spark = self.get_spark()
        VideoSchema = self.get_schema()
        
        if input_files:
            logging.info(f"Write at path: {self.output_path}")
            logging.info(f"Save metadata at: {self.table_name}")
            
            self.create_dataframe(spark=spark,
                                  VideoSchema=VideoSchema,
                                  input_files=input_files,
                                  output_path=self.output_path,
                                  table_name = self.table_name, 
                                  database=self.database,
                                  numPartition=self.numPartition,
                                  compression=self.compression)