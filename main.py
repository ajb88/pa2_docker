import pandas as pd
from pyspark.sql import SparkSession
from pyspark.mllib.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
import sys


def preprocess(file):
    pdf = pd.read_csv(file,skiprows=1, sep=";", header=None)
    names = ["fixed acidity","volatile acidity","citric acid", "residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality"]
    pdf.columns = names
    rdd = spark.createDataFrame(pdf)
    featureColumns = [c for c in rdd.columns if c != 'quality']
    assembler = VectorAssembler(inputCols=featureColumns,
                                outputCol="features")
    return assembler.transform(rdd)

spark = SparkSession.builder.appName("prediction").getOrCreate()
spark.sparkContext.setLogLevel('WARN')

file = sys.argv[1]

df = preprocess(file)

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import LogisticRegressionModel

trainedmodel = LogisticRegressionModel.load("lrmodel")

predictionsDF = trainedmodel.transform(df)

from pyspark.ml.evaluation import MulticlassClassificationEvaluator
evaluatorMulti = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction")
predictionAndTarget = predictionsDF.select("quality", "prediction")
f1 = evaluatorMulti.evaluate(predictionAndTarget, {evaluatorMulti.metricName: "f1"})
print("\n\n\nf1 score: " + str(f1) + "\n\n\n")
