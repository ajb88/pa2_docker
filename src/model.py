import pandas as pd
from pyspark.sql import SparkSession
from pyspark.mllib.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

spark = SparkSession.builder.appName("model").getOrCreate()
def preprocess(file):
    pdf = pd.read_csv(file,skiprows=1, sep=";", header=None)
    names = ["fixed acidity","volatile acidity","citric acid", "residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality"]
    pdf.columns = names
    rdd = spark.createDataFrame(pdf)
    featureColumns = [c for c in rdd.columns if c != 'quality']
    assembler = VectorAssembler(inputCols=featureColumns,
                                outputCol="features")
    return assembler.transform(rdd)

df = preprocess("../TrainingDataset.csv")

from pyspark.ml.classification import LogisticRegression
lr = LogisticRegression(featuresCol="features", labelCol="quality")
lrModel = lr.fit(df)
predictionsDF = lrModel.transform(df)
print(predictionsDF.limit(3).toPandas())

lrModel.write().overwrite().save("lrmodel")
