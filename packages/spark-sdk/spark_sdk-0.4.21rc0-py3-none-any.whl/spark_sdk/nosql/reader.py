try:
    from PIL import Image
except:
    pass


try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    
import base64
import io


def cvtColor(binary):
    b,g,r = Image.open(io.BytesIO(binary)).split()
    return Image.merge("RGB", (r, g, b))

def get_thumbnail(i):
    i.thumbnail((100, 100), Image.LANCZOS)
    return i

def image_base64(im):
    # if isinstance(im, str):
    #     im = get_thumbnail(im)
    im = get_thumbnail(im)    
    with io.BytesIO() as buffer:
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'
    # return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'

    
def toPandasImage(self, limit:int = 100):
    if limit > 100:
        limit = 100
    pdf = self.limit(limit).toPandas()
    
    need_convert_dict = {}
    for c in self.schema:
        if "BinaryType" in str(c.dataType):
            c_name = c.name
            # pdf[c_name] = pdf[c_name].apply(lambda x: Image.open(io.BytesIO(x)))
            pdf[c_name] = pdf[c_name].apply(cvtColor) 
            need_convert_dict[c_name] = image_formatter
    DataFrame.need_convert_dict = need_convert_dict
    pdf.need_convert_dict = need_convert_dict
    return pdf


from pyspark.sql import DataFrame as SparkDataFrame
SparkDataFrame.toPandasImage = toPandasImage

from pandas._config import get_option
from io import StringIO
from pandas.io.formats import format as fmt
from typing import Optional

def _repr_html_(self) -> Optional[str]:
    """
    Return a html representation for a particular DataFrame.
    Mainly for IPython notebook.
    """
    if self._info_repr():
        buf = StringIO()
        self.info(buf=buf)
        # need to escape the <class>, should be the first line.
        val = buf.getvalue().replace("<", r"&lt;", 1)
        val = val.replace(">", r"&gt;", 1)
        return f"<pre>{val}</pre>"

    if get_option("display.notebook_repr_html"):
        max_rows = get_option("display.max_rows")
        min_rows = get_option("display.min_rows")
        max_cols = get_option("display.max_columns")
        show_dimensions = get_option("display.show_dimensions")
        
        if 'need_convert_dict' not in self.__dict__:
            if self._is_copy:
                pass
            else:
                self.need_convert_dict = {}
                
        formatter = fmt.DataFrameFormatter(
            self,
            columns=None,
            col_space=None,
            na_rep="NaN",
            formatters=self.need_convert_dict,
            float_format=None,
            sparsify=None,
            justify=None,
            index_names=True,
            header=True,
            index=True,
            bold_rows=True,
            escape=False,
            max_rows=max_rows,
            min_rows=min_rows,
            max_cols=max_cols,
            show_dimensions=show_dimensions,
            decimal=".",
        )
        
        return fmt.DataFrameRenderer(formatter).to_html()
    else:
        return None

from pandas import DataFrame
DataFrame._repr_html_ = _repr_html_

import os
import mimetypes
from sys import getsizeof
import tempfile
from binascii import b2a_hex, b2a_base64, hexlify


from spark_sdk.utils import import_or_install
import_or_install("ipywidgets")
try:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 ipywidgets")
except:
    os.system("jupyter nbextension enable --py --sys-prefix widgetsnbextension")
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 ipywidgets")
from ipywidgets.widgets import Box
from ipywidgets import widgets
from traitlets import traitlets

from spark_sdk import PySpark
import spark_sdk as ss

import numpy as np

class LoadedButton(widgets.Button):
    """A button that can holds a value as a attribute."""

    def __init__(self, value=None, *args, **kwargs):
        super(LoadedButton, self).__init__(*args, **kwargs)
        # Create the value attribute.
        self.add_traits(value=traitlets.Any(value))


class Video(object):
    def __init__(self, input_path=None, video=None, data=None, url=None, filename=None, embed=False,
                 mimetype="video/mp4", width=None, height=None, html_attributes="controls"):
        
        self.input_path = input_path
        self.video = video
        self.mimetype = mimetype
        self.embed = embed
        self.width = width
        self.height = height
        self.html_attributes = html_attributes
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False

        
    def generate_sql(self, columns):
        spark = self.get_spark()
        if self.check_delta(self.input_path):
            df = spark.sql(f"""select {columns} from delta.`{self.input_path}` """)
        else:
            df = spark.sql(f"""select {columns} from parquet.`{self.input_path}`""")
        return df
    
    
    def write_to_folder(self, row):
        with open(self.tmp_file, 'wb') as wfile:
            wfile.write(row.video)
            
    def displayVideo(self, ex):
        get_value = ex.description
        df = self.generate_sql("*").filter(f"path = '{get_value}'").limit(1)

        self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')

        # self.temp_folder = './tmp_sdk'
        self.base_path = os.path.basename(str(get_value))
        self.tmp_file = os.path.join(self.temp_folder.name, self.base_path)

        _ = [self.write_to_folder(row) for row in df.collect()]

        from IPython.display import Video
        self.output.append_display_data(Video(self.tmp_file, width=self.width, height=self.height))

        
    def _repr_html_(self):
        width = height = ''
        if self.width:
            width = ' width="%d"' % self.width
        if self.height:
            height = ' height="%d"' % self.height
            
        if isinstance(self.input_path, str):
            df_path = self.generate_sql("path").toPandas()
        
        
        selection_box = widgets.VBox()
        selection_toggles = []
        selected_labels = {}
        labels = {}
        
        for p in df_path['path'].values:
            labels[p] = p
        
        import pandas as pd
        layout = widgets.Layout(width=str(pd.options.display.max_colwidth*5)+'px', height='40px')
        
        for k in sorted(labels):
            o = LoadedButton(description=k, value=k,layout=layout)
            o.on_click(self.displayVideo)
            selection_toggles.append(o)

        selection_box.children = selection_toggles
        self.output = widgets.Output()
        return display(selection_box, self.output)
    
    def __repr__(self):
        return ""
    

class Audio(object):
    def __init__(self, input_path=None, video=None, data=None, url=None, filename=None, embed=False,
                 mimetype="wav", width=None, height=None, html_attributes="controls"):
        
        self.input_path = input_path
        self.video = video
        self.mimetype = mimetype
        self.embed = embed
        self.width = width
        self.height = height
        self.html_attributes = html_attributes
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False

    def generate_sql(self, columns):
        spark = self.get_spark()
        if self.check_delta(self.input_path):
            df = spark.sql(f"""select {columns} from delta.`{self.input_path}` """)
        else:
            df = spark.sql(f"""select {columns} from parquet.`{self.input_path}`""")
        return df
    
    def read_mp3(self, f, normalized=False):
        """MP3 to numpy array"""
        import pydub
        a = pydub.AudioSegment.from_mp3(f)
        y = np.array(a.get_array_of_samples())
        if a.channels == 2:
            y = y.reshape((-1, 2))
        if normalized:
            return a.frame_rate, np.float32(y) / 2**15
        else:
            return a.frame_rate, y
    
    def write_to_folder(self, row):
        if '.pcm' in row['path']:
            data = np.frombuffer(row['audio'], dtype = 'float64')
            from IPython.display import Audio, display
            self.output.append_display_data(Audio(data, rate=int(row['samplerate'])))
            
        elif '.wav' in row.path:
            from scipy.io import wavfile
            samplerate, data = wavfile.read(BytesIO(row.audio))
            from IPython.display import Audio, display
            self.output.append_display_data(Audio(data.T, rate=samplerate))
            
        elif 'mp3' in row.path:
            samplerate, data = self.read_mp3(BytesIO(row.audio))
            from IPython.display import Audio, display
            self.output.append_display_data(Audio(data.T, rate=samplerate))
            
    def displayAudio(self, ex):
        get_value = ex.description
        df = self.generate_sql("*").filter(f"path = '{get_value}'").limit(1)
        
        _ = [self.write_to_folder(row) for row in df.collect()]
        
        # df.foreach(self.write_to_folder)
        
    def _repr_html_(self):
        width = height = ''
        if self.width:
            width = ' width="%d"' % self.width
        if self.height:
            height = ' height="%d"' % self.height
            
        if isinstance(self.input_path, str):
            df_path = self.generate_sql("path").toPandas()
        
        
        selection_box = widgets.VBox()
        selection_toggles = []
        selected_labels = {}
        labels = {}
        for p in df_path['path'].values:
            labels[p] = p
        
        import pandas as pd
        layout = widgets.Layout(width=str(pd.options.display.max_colwidth*5)+'px', height='40px')
        
        for k in sorted(labels):
            o = LoadedButton(description=k, value=k,layout=layout)
            o.on_click(self.displayAudio)
            selection_toggles.append(o)

        selection_box.children = selection_toggles
        self.output = widgets.Output()
        return display(selection_box, self.output)
    
    def __repr__(self):
        return ""