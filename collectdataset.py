!pip install kaggle

from google.colab import files  #Import kaggle.json
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d moltean/fruits  #Download dataset

!unzip fruits.zip -d my_data  #Unzip the dataset
