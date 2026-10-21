import sys
import os

os.environ["PYSPARK_PYTHON"]=sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"]=sys.executable


from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").master("local[*]").getOrCreate()

df = spark.createDataFrame([(1, "Laptop"), (2, "Mouse")], ["id", "product"])
df.show()

spark.stop()