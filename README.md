
# Programming Assignment 2
**Allen Blount**
**CS643-Cloud Computing, Fall 2020**
**Dr. Borcea**

### Cloud Environment  
I used a [cluster](https://imgur.com/sL8F99D) of 4 EC2 instances running Ubuntu Server 18.04:
TODO:PIC

Spark must be set up on each node. 
#### Install Java and scala:
 ```
$ sudo apt update
$ sudo apt install openjdk-8-jre-headless
$ sudo apt install scala
```
#### Set up keyless ssh by generating a key pair:
```
$ cd ~/.ssh
~/.ssh: $ **ssh-keygen -t rsa -P
cat id_rsa.pub
```
Copy the public key (.pub) to each node's .ssh/authorized_keys file.  
#### Install spark:
```
$ wget https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
$ tar xvf spark-2.4.3-bin-hadoop2.7.tgz  
$ sudo mv spark-2.4.3-bin-hadoop2.7/ /usr/local/spark
```
Add the following to ~/.profile:
```
export PATH=/usr/local/spark/bin:$PATH
```
#### Configure Spark 
Edit  `/usr/local/spark/conf/spark-env.sh`
```
# contents of conf/spark-env.sh  
export SPARK_MASTER_HOST=_<master-private-ip>_  
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64# For PySpark use  
export PYSPARK_PYTHON=python3
```
Edit `/usr/local/spark/conf/slaves`
```
# contents of conf/slaves  
_<worker-private-ip1>  
<worker-private-ip2>  
<worker-private-ip3>_
```
#### Start Spark
```
$ sh /usr/local/spark/sbin/start-all.sh
```


### Machine Learning Model
I used spark to create a very simple Logistic Regression Model. If I had more time, I would have tried to improve the model more, but for now a simple model will work. 

To start, create a directory with /src/model.py and TrainingDataset.csv. We can then run the model with:
```
$ spark-submit model.py
```
This will create ./lrmodel/, which is our MLLib model we will import to the prediction application. 


### Prediction Application
Make a director with validation data and /lrmodel/. We can run the application on any EC2 with spark, since we need a spark context to establish the MLLib/pyspark environment. (I used my master node)
```
spark-submit main.py ValidationDataset.csv
```
Known issues: the output is quite verbal, and I had difficulty trying to drop some of spark's log messages. I tried to make the F1 score visible towards the [end](https://imgur.com/66M2HnY) of the script.

### Docker
Pull my Docker repo:
```
$ sudo docker pull ajb88/pa2_predict
```
To pass a local file from your EC2, we need to evoke the -v switch on docker's run command:
```
sudo docker run -v /full/local/path/to/validationdata.csv:/mnt/mydata/ -t ajb88/pa2_predict:latest driver main.py validationdata.csv
```
Do not change the container's mapped director, /mnt/mydata/. Also use the full local path to your validation dataset. 
The output should be similar to running it through spark-submit. I tested this on a new EC2 instance that did not have spark installed. 

### References/Acknowledgements:
https://blog.insightdatascience.com/simply-install-spark-cluster-mode-341843a52b88
https://towardsdatascience.com/how-to-containerize-models-trained-in-spark-f7ed9265f5c9
https://piotrszul.github.io/spark-tutorial/notebooks/3.1_ML-Introduction.html
https://stackoverflow.com/questions/44876778/how-can-i-use-a-local-file-on-container


