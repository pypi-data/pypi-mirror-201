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


class ConvertToFolderVideo:
    """
    ConvertToFolderVideo would conver folder parquet/delta format back to Video folder
    :param input_path: path to parquet file
    :param output_path: path user want to store image at
    :param write_mode: recovery convert back like original folder, all_in_one convert back all image in one folder
    :param database: database datalake house ex: ftel_dwh_insights
    :param table_name: table datalake house ex: table1
    
    Return:
    parquet/delta file at output_path    
    
    converter = ConvertToFolderVideo(
    input_path = '/user/duyvnc/image/img_user_device_jpg_212_212.parquet',
    output_path = './abc'
    )

    converter.execute()
    """
    def __init__(
        self,
        input_path:str, 
        output_path:str,
        video_type = "mp4",
        write_mode = "recovery"
    ):
        
        self.input_path = input_path
        self.output_path = output_path
        self.video_type = video_type
        self.write_mode = write_mode
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        
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
        with open(image_path, 'wb') as wfile:
            wfile.write(row.video)
            
    def execute(self):
        input_path = self.convert_to_hdfs_path(self.input_path)
        
        if self.check_delta(input_path):
            logging.info("Detect Delta File")
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
                    with open(image_path, 'wb') as wfile:
                        wfile.write(row.video)
                
        logging.info("Convert to Image folder complete")