FROM gcr.io/datamechanics/spark-py-connectors:3.0.0-dm4

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/ src/
COPY main.py .
COPY ValidationDataset.csv .
COPY lrmodel/data ./lrmodel/data
COPY lrmodel/metadata ./lrmodel/metadata

ENV PYSPARK_MAJOR_PYTHON_VERSION=3
