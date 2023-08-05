import spark_sdk as ss
from spark_sdk.pyspark_add_on import PySpark, PyArrow
from pyspark.sql.types import StructField, StructType, IntegerType, BinaryType, StringType, TimestampType


from spark_sdk.utils import import_or_install
import_or_install("petastorm")

from petastorm.etl.dataset_metadata import materialize_dataset
from petastorm.codecs import ScalarCodec, CompressedImageCodec, NdarrayCodec
from petastorm.unischema import dict_to_spark_row, Unischema, UnischemaField
from petastorm.codecs import ScalarCodec, CompressedImageCodec, NdarrayCodec
from petastorm import make_reader


from glob import glob
import logging
import os
from pathlib import Path, PurePath

try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class ConvertFromFolderImage:
    """
    Create a parquet/delta file given local Image directory
    

    Parameters
    ----------
    input_path : unicode, str 
        The input filename include ``png``, ``jpeg`` image
        User can add system file pattern like *
        Examples:
        input_path="**/*.jpg"
        input_path="**/*.png"
        This pattern get all jpg in folder with different directory levels
        View https://docs.python.org/3/library/glob.html

    output_path : unicode
        Ouput directory location maybe file:/ (local file) or hdfs:/ (datalake path)
        Examples:
        output_path = "file:/home/duyvnc/"
        output_path = "hdfs:/user/duyvnc/"
        
    table_name : str
        Table_name store metadata
        User should input table_name follow dwh convention: img_abc, vid_abc, audio_abc
        Examples: img_abc
        
    database : str
        Database to store metadata
        User should input database follow dwh convention: default
        Examples: default
        

    repartition : bool 
        Default: False
        Data will be repartition to target file size
        
    numPartition : int
        Default None
        Number of part each user want to seperate parquet file into

    file_format : str
        Default: parquet
        File format user want to write parquet/delta
        
    compression: str 
        Default: zstd
        Compression method user want to compress parquet file
        Value: None, zstd, snappy
        See spark.sql.parquet.compression.codec
        https://spark.apache.org/docs/2.4.3/sql-data-sources-parquet.html
        
    image_type : str
        Default: jpg
        Value png or jpg
        
    image_color : int
        Default: 3
        Value 3, 2 or 1, shape of image have color is 3 or 1 if gray image
        
    size : List of Tuple
        Default: jpg
        List size user want to resize or padding
        Examples: size = [(320, 180), (500, 100)]
        
    resize_mode : str
        Default: None
        Value: None, padding, resize
        Mode of image user want to resize
        If in folder user have various size of image, 300, 400 500
        User will add size = 500:
        And resize_mode  = 'padding'
        Then function will convert all image 300, 400, 500 to shape of 500

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        from spark_sdk.nosql.codec import ConvertFromFolderImage

        converter = ConvertFromFolderImage(
                      input_path="/home/duyvnc/image_storage/images/**/*.jpg",
                      input_recursive = True, # will loop through folder to get all pattern
                      #setting output
                      output_path = f"hdfs:/user/duyvnc/image/img_images_jpg.parquet",
                      table_name = 'img_images_jpg',
                      database = 'default',
                      file_format = 'parquet', # delta|parquet
                      compression = 'zstd', # |snappy
                      # setting converter
                      image_type = 'jpg',
                      image_color = 3,
                      resize_mode="padding", # |padding|resize
                      size = [(212,212),
                             (597, 597)],
                     )

        converter.execute()
        
        from spark_sdk.nosql.codec import ConvertFromFolderImage

        converter = ConvertFromFolderImage(
                      input_path="/home/duyvnc/image_storage/device_images/**/*.jpg",
                      input_recursive = True, # will loop through folder to get all pattern

                      #setting output
                      output_path = f"hdfs:/user/duyvnc/image/img_user_device_jpg.delta",
                      table_name = 'img_user_device_jpg',
                      database = 'default',
                      file_format = 'delta', # |parquet
                      compression = 'zstd', # |snappy

                      # setting converter
                      image_type = 'jpg',
                      image_color = 3,
                      resize_mode=None, # |padding|resize
                      size = [(212,212),
                             (597, 597)],
                     )

        converter.execute()
        ```
        
        Function will convert all Image in file:'/home/duyvnc/device_images/' to absolute directory hdfs:/user/duyvnc/image/img_images_jpg.parquet
    """
   
        
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=False,
        numPartition=None,
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
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(input_path.replace("hdfs:", ""))
            else:
                return input_path
        
    def padding(self, img, expected_size, borderType=cv2.BORDER_CONSTANT, value=(255,255,255)):
        delta_width = expected_size[0] - img.shape[0]
        delta_height = expected_size[1] - img.shape[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        # padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
        
        logging.info(f"Padding image: {img.shape[0]}, {img.shape[1]}")
        return cv2.copyMakeBorder(img, pad_width, delta_width - pad_width, pad_height, delta_height - pad_height, borderType, value=value)
    
    
    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)
                
    
    def create_dataframe(self, spark, ImageSchema, image_files,
                        output_path,
                        table_name, 
                        database,
                        size=[(720,360)], 
                        resize_mode='padding',
                        numPartition=8,
                        compression='zstd'):
        ROWGROUP_SIZE_MB = 128
        with materialize_dataset(spark, output_path, ImageSchema, ROWGROUP_SIZE_MB):
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
            UnischemaField('image', np.uint8, (size[0], size[1], image_color), CompressedImageCodec('.png'), False)
        ])
    
    
    
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
            self.output_path = self.convert_to_hdfs_path(self.output_path)
            if "." + self.file_format in self.output_path:
                output_path = self.output_path.replace("." + self.file_format, "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format))
            else:
                output_path = self.output_path + "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format)
            
            if self.table_name:
                table_name = self.table_name + "_{s0}_{s1}".format(s0=str(s[0]), s1=str(s[1]))
            else:
                table_name = ''
            
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
                

        
class ConvertToFolderImage:
    """
    Create a folder Image given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame
    

    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input filename to load Image or dataframe include Image

    input_path : unicode
        Path to a local file or hdfs file containing the Image.
        
    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a Image file (jpg, png) 

    write_mode : str
        Specify the write_mode user want to
        If write_mode = 'recovery' 
        Function will convert Image to a multiple level of directory base on column path
        If write_mode != 'recovery'
        Function will convert all Image in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
        Glob path that user input when use ConvertFromFolderVideo function
        For example: "/home/duyvnc/image_storage/images/**/*.jpg"
        When output it will replace '/home/duyvnc/image_storage/images/'  by ''
        That turn column path from absolute path to relative path
        
    keep_origin_jpg: bool | default False
        JPG is a lossly format when cv2 read jpg convert to array cv2.imread()
        And write back to jpg cv2.imwrite() it will cause 2 array 29% different
        If user want to keep origin array turn it on, but the image after convert will bigger than 400% compare with origin image

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        from spark_sdk.nosql.codec import ConvertToFolderImage

        converter = ConvertToFolderImage(
            input_path = '/user/duyvnc/image/img_user_device_jpg_212_212.parquet',
            raw_input_path = "/home/duyvnc/image_storage/device_images/**/*.jpg",
            output_path = '/home/duyvnc/image_storage/abc/',
            debug = False
        )

        converter.execute()
        ```
        
        Function will convert all Image in hdfs:'/user/duyvnc/image/img_user_device_jpg_212_212.parquet' to absolute directory /home/duyvnc/image_storage/abc/
    """
    def __init__(
        self,
        data = None,
        input_path:str=None,
        output_path:str='./',
        image_type = "jpg",
        write_mode = "recovery",
        raw_input_path = "",
        keep_origin_jpg = False,
        debug = False

    ):
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            
        check_parent_path = self.raw_input_path.split('*')
        if len(check_parent_path) > 1:
            self.raw_input_path = check_parent_path[0]
            
        if keep_origin_jpg and image_type == "jpg":
            self.keep_origin_jpg = True
        else:
            self.keep_origin_jpg = False
            
        if isinstance(data, (Path, PurePath)):
            input_path = str(data)
            data = None
        elif data is not None and ss.exists(data):
            input_path = data
            data = None

            
        self.input_path = input_path
        self.output_path = output_path
        self.image_type = image_type
        self.write_mode = write_mode
        self.raw_input_path = raw_input_path
        self.debug = debug
        

        if data is None:
            spark = self.get_spark()
            if self.check_delta(input_path):
                logging.info("Detect Delta File")
                self.df = ss.sql(f"""select * from delta.`{input_path}`""")
            else:
                self.df = ss.sql(f"""select * from parquet.`{input_path}`""")
                
        else:
            self.df = data
        
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False
        
    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    
    
    def write_to_folder(self, row):
        if self.write_mode == "recovery":
            image_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            image_path = os.path.join(self.output_path, base_path)
        
        if self.debug:
            logging.debug("image_path: {}, row.image: {row.image}")
            
        self.mkdir_folder(os.path.dirname(image_path))
        if self.keep_origin_jpg:
            with open(image_path, 'wb') as f:
                f.write(row.image)
                        
        else:
            img = cv2.imdecode(np.frombuffer(row.image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(image_path, img)
            
    def execute(self):
        self.df.foreach(self.write_to_folder)
        logging.info("Convert to Image folder complete")
        
            # Using Petastorm function but not can read delta
            # self.mkdir_folder(self.output_path)
            # with make_reader(input_path) as reader:
            #     for row in reader:
            #         # Create output_path
            #         self.write_to_folder(row)
        
        
#---------------------------------#     
#------- VIDEO SESSION -----------#
#---------------------------------#
from abc import abstractmethod
from io import BytesIO
import logging

try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

import numpy as np
import zlib


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

class ConvertFromFolderVideo:
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
        thumbnail_width = 256,
        thumbnail_height = 144,

        
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
        
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height
        
        self.debug = debug
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            
            
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(input_path.replace("hdfs:", ""))
            else:
                return input_path

    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)
            
            #     pass
            # spark_df.coalesce(numPartition) \
            #         .write \
            #         .format(file_format) \
            #         .option('compression', compression) \
            #         .mode('overwrite') \
            #         .option("path", output_path) \
            #         .save()
               


            
    def row_generator(self, path):
        """Returns a single entry in the generated dataset. Return a bunch of random values as an example."""
        cap = cv2.VideoCapture(path)
        # size = (int(cap.get(3)), int(cap.get(4)))
        frame_number = cap.get(cv2.CAP_PROP_FRAME_COUNT) / 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1)
        res, frame = cap.read()
        frame = cv2.resize(frame, (self.thumbnail_width, self.thumbnail_height))
        frame = frame[:, :, (2, 1, 0)]
        return {'path': path,
                'thumbnail': frame,
                'video': open(path, "rb").read()}
    
    def create_dataframe(self, spark, VideoSchema, input_files,
                        output_path,
                        table_name, 
                        database,
                        numPartition=8,
                        compression='zstd'):
        ROWGROUP_SIZE_MB = 1024
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
            UnischemaField('thumbnail', np.uint8, (self.thumbnail_height, self.thumbnail_width, 3), CompressedImageCodec('.jpg'), False),
            UnischemaField('video', np.bytes_, (), VideoBinaryEncode(), False)
        ])
    
    def ingest(self):
        input_files = sorted(glob(self.input_path, recursive=self.input_recursive))
        self.output_path = self.convert_to_hdfs_path(self.output_path)
        
        
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
            
            
class ConvertToFolderVideo:
    """
    Create a folder Video given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame
    

    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input filename to load video or dataframe include video

    input_path : unicode
        Path to a local file or hdfs file containing the video.
        
    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a video file (mp4, ts...) 

    write_mode : str
        Specify the write_mode user want to
        If write_mode = 'recovery' 
        Function will convert video to a multiple level of directory base on column path
        If write_mode != 'recovery'
        Function will convert all video in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
        Glob path that user input when use ConvertFromFolderVideo function
        For example: "/home/duyvnc/image_storage/audio_mp3/*.mp3"
        When output it will replace '/home/duyvnc/image_storage/audio_mp3/'  by ''
        That turn column path from absolute path to relative path

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        converter = ConvertToFolderVideo(
        input_path = 'file:/home/duyvnc/image_storage/vid.parquet',
        output_path = './abc'
        )

        converter.execute()
        ```
        
        Function will convert all video in file:/home/duyvnc/image_storage/vid.parquet to relative directory abc
    """

    def __init__(
        self,
        data = None,
        input_path:str=None,
        output_path:str='./',
        image_type = "jpg",
        write_mode = "recovery",
        raw_input_path = "",
        debug = False
    ):
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            
        check_parent_path = self.raw_input_path.split('*')
        if len(check_parent_path) > 1:
            self.raw_input_path = check_parent_path[0]
            
        if isinstance(data, (Path, PurePath)):
            input_path = str(data)
            data = None
        elif data is not None and ss.exists(data):
            input_path = data
            data = None
            
        self.input_path = input_path
        self.output_path = output_path
        self.image_type = image_type
        self.write_mode = write_mode
        self.raw_input_path = raw_input_path
        self.debug = debug
        

        if data is None:
            spark = self.get_spark()
            if self.check_delta(input_path):
                logging.info("Detect Delta File")
                self.df = ss.sql(f"""select * from delta.`{input_path}`""")
            else:
                self.df = ss.sql(f"""select * from parquet.`{input_path}`""")
                
        else:
            self.df = data
        
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False
        
    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
            
    def write_to_folder(self, row):
        if self.write_mode == "recovery":
            image_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            image_path = os.path.join(self.output_path, base_path)
        # self.mkdir_folder(os.path.dirname(image_path))
        with open(image_path, 'wb') as wfile:
            wfile.write(row.video)
            
    def execute(self):
        self.df.foreach(self.write_to_folder)
        logging.info("Convert to Image folder complete")
        
        
class AudioBinaryEncode(DataframeColumnCodec):
    """Encodes numpy ndarray into, or decodes an ndarray from, a spark dataframe field."""

    def encode(self, unischema_field, value):
#         expected_dtype = unischema_field.numpy_dtype
#         if isinstance(value, np.ndarray):
#             expected_dtype = " ".join(re.findall("[a-zA-Z]+", str(expected_dtype)))
#             value_dtype = " ".join(re.findall("[a-zA-Z]+", str(value.dtype.type)))
#             if expected_dtype != value_dtype:
#                 raise ValueError('Unexpected type of {} feature. '
#                                  'Expected {}. Got {}'.format(unischema_field.name, expected_dtype, value.dtype))

#             expected_shape = unischema_field.shape
            # if not _is_compliant_shape(value.shape, expected_shape):
            #     raise ValueError('Unexpected dimensions of {} feature. '
            #                      'Expected {}. Got {}'.format(unischema_field.name, expected_shape, value.shape))
        # else:
        #     raise ValueError('Unexpected type of {} feature. '
        #                      'Expected ndarray of {}. Got {}'.format(unischema_field.name, expected_dtype, type(value)))

        # memfile = BytesIO()
        # np.save(memfile, value)
        # return bytearray(memfile.getvalue())
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

#---------------------------------#     
#------- AUDIO SESSION -----------#
#---------------------------------#

import pydub
from scipy.io import wavfile

class ConvertFromFolderAudio:
    """
    # Test case 2, write with PCM audio:
    converter = ConvertFromFolderAudio(
                  input_path='./audio_pcm/*.pcm',
                  input_recursive = False,
                  output_path = f"file:/home/duyvnc/image_storage/audio_pcm.parquet",
                 )

    converter.execute()
    
    # Test case 3, write with Wav audio:
    converter = ConvertFromFolderAudio(
                  input_path='./audio_wav/*.wav',
                  input_recursive = False,
                  output_path = f"file:/home/duyvnc/image_storage/audio_wav.parquet",
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
            
    def guess_type(self, input_path):
        dict_type = {
            'wav': np.float64,
            'pcm': np.float64,
            'mp3': np.int16,
            'mp4': np.bytes_,
            'jpg': np.uint8,
            'png': np.uint8
        }
        
        for t in dict_type.keys():
            if "." + t in input_path:
                return t
            
    def numpy_map_type(self, input_path):
        dict_type = {
            'wav': np.bytes_,
            'pcm': np.bytes_,
            'mp3': np.bytes_,
            'mp4': np.bytes_,
            'jpg': np.uint8,
            'png': np.uint8
        }
        
        return dict_type[self.guess_type(input_path)]
    
    def read_mp3(self, f, normalized=False):
        """MP3 to numpy array"""
        
        a = pydub.AudioSegment.from_mp3(f)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
            y = y.reshape((-1, 2))
        if normalized:
            return a.frame_rate, np.float32(y) / 2**15
        else:
            return a.frame_rate, y
        
    def read_pcm(self, input_path, dtype='float64'):
        with open(input_path, 'rb') as file:
            y = file.read()
            y = np.frombuffer(y, dtype = 'int16')
            i = np.iinfo(y.dtype)
            abs_max = 2 ** (i.bits - 1)
            offset = i.min + abs_max
            y = (y.astype(dtype) - offset) / abs_max
        return 8000, y.tobytes()
    
    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)

            
    def row_generator(self, path):
        """Returns a single entry in the generated dataset. Return a bunch of random values as an example."""
        if self.guess_type(path) == 'pcm':
            samplerate, data = self.read_pcm(path)
            channels = 1
            
        elif self.guess_type(path) == 'wav':
            samplerate, data = wavfile.read(path)
            if len(data.shape) == 2:
                data = data.T
                channels = 2
            else:
                channels = 1
                
            with open(path, 'rb') as file:
                data = file.read()
        if self.guess_type(path) == 'pcm':
            samplerate, data = self.read_pcm(path)
            channels = 1
            
        elif self.guess_type(path) == 'mp3':
            samplerate, data = self.read_mp3(path)
            if len(data.shape) == 2:
                data = data.T
                channels = 2
            else:
                channels = 1
                
            with open(path, 'rb') as file:
                data = file.read()
            
        return {'path': path,
                'samplerate': samplerate,
                'channels': channels,
                'audio': data}
    
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
    def create_dataframe(self, spark, VideoSchema, input_files,
                        output_path,
                        table_name, 
                        database,
                        numPartition=8,
                        compression='zstd'):
        ROWGROUP_SIZE_MB = 128
    
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
        return Unischema('Audio', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('samplerate', np.int_, (), ScalarCodec(IntegerType()), False),
            UnischemaField('channels', np.int_, (), ScalarCodec(IntegerType()), False),
            UnischemaField('audio', self.numpy_map_type(self.input_path), (1000,), AudioBinaryEncode(), False)
        ])
    
    def execute(self):
        input_files = sorted(glob(self.input_path, recursive=self.input_recursive))
        self.output_path = self.convert_to_hdfs_path(self.output_path)
        
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
            
            
import spark_sdk as ss

import os, sys
import numpy as np

from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructField, StructType, IntegerType, BinaryType, StringType, TimestampType

from petastorm import make_reader

from glob import glob
import cv2
from PIL import Image

import logging


class ConvertToFolderAudio:
    """
    Create a folder Audio given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame
    

    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input filename to load Audio or dataframe include Audio

    input_path : unicode
        Path to a local file or hdfs file containing the audio.
        
    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a video file (pcm, mp3, wav...) 

    write_mode : str
        Specify the write_mode user want to
        If write_mode = 'recovery' 
        Function will convert audio to a multiple level of directory base on column path
        If write_mode != 'recovery'
        Function will convert all audio in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
        Glob path that user input when use ConvertFromFolderVideo function
        For example: "/home/duyvnc/image_storage/audio_mp3/*.mp3"
        When output it will replace '/home/duyvnc/image_storage/audio_mp3/'  by ''
        That turn column path from absolute path to relative path

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        converter = ConvertToFolderAudio(
        input_path = 'file:/home/duyvnc/image_storage/audio_mp3.parquet',
        raw_input_path = '/home/duyvnc/image_storage/audio_mp3/*.mp3',
        output_path = './abc',
        write_mode = "recovery"
        )

        converter.execute()
        ```
        
        Function will convert all audio in file:/home/duyvnc/image_storage/audio_mp3.parquet to relative directory abc
    """
    def __init__(
        self,
        data = None,
        input_path:str=None,
        output_path:str='./',
        image_type = "jpg",
        write_mode = "recovery",
        raw_input_path = "",
        debug = False
    ):
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            
        check_parent_path = self.raw_input_path.split('*')
        if len(check_parent_path) > 1:
            self.raw_input_path = check_parent_path[0]
            
        if isinstance(data, (Path, PurePath)):
            input_path = str(data)
            data = None
        elif data is not None and ss.exists(data):
            input_path = data
            data = None
            
        self.input_path = input_path
        self.output_path = output_path
        self.image_type = image_type
        self.write_mode = write_mode
        self.raw_input_path = raw_input_path
        self.debug = debug
        

        if data is None:
            spark = self.get_spark()
            if self.check_delta(input_path):
                logging.info("Detect Delta File")
                self.df = ss.sql(f"""select * from delta.`{input_path}`""")
            else:
                self.df = ss.sql(f"""select * from parquet.`{input_path}`""")
                
        else:
            self.df = data
        
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False
        
    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
            
    def write_to_folder(self, row):
        if self.write_mode == "recovery":
            ouput_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            ouput_path = os.path.join(self.output_path, base_path)
        # self.mkdir_folder(os.path.dirname(image_path))
        print(ouput_path)
        with open(ouput_path, 'wb') as wfile:
            wfile.write(row.audio)
            
    def execute(self):
        self.df.foreach(self.write_to_folder)
        logging.info("Convert to Image folder complete")