# -*- coding: utf-8 -*-
"""introducao_ML_v1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pZMkkTctw_dHbZUqk7lKXfITx2NZOCzG

# **Redes Neurais e Aprendizado Profundo**
**Autor**: Renan Santos Mendes

**Email**: renansantosmendes@gmail.com

**Descrição**: Este notebook apresenta um exemplo de uma rede neural profunda com mais de uma camada para um problema de classificação.


# **Saúde Fetal**

As Cardiotocografias (CTGs) são opções simples e de baixo custo para avaliar a saúde fetal, permitindo que os profissionais de saúde atuem na prevenção da mortalidade infantil e materna. O próprio equipamento funciona enviando pulsos de ultrassom e lendo sua resposta, lançando luz sobre a frequência cardíaca fetal (FCF), movimentos fetais, contrações uterinas e muito mais.

Este conjunto de dados contém 2126 registros de características extraídas de exames de Cardiotocografias, que foram então classificados por três obstetras especialistas em 3 classes:

- Normal
- Suspeito
- Patológico

# Clonando o conjunto de dados
"""

# !rm -r lectures-cdas-2023
# !git clone https://github.com/renansantosmendes/lectures-cdas-2023.git

"""# Instalando pacotes"""

# !pip install mlflow dagshub gitpython -q

"""# 1 - Importando os módulos necessários"""

import os
import tensorflow
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, InputLayer, Dropout
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from keras.regularizers import l1, l2

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

"""# Definindo funções adicionais"""

import os
import random
import numpy as np
import random as python_random

def reset_seeds():
   os.environ['PYTHONHASHSEED']=str(42)
   tf.random.set_seed(42)
   np.random.seed(42)
   random.seed(42)

"""# 2 - Fazendo a leitura do dataset e atribuindo às respectivas variáveis"""

data = pd.read_csv("https://raw.githubusercontent.com/renansantosmendes/lectures-cdas-2023/master/fetal_health_reduced.csv")

"""# Dando uma leve olhada nos dados"""

data.head()

data.fetal_health.value_counts()

"""# 3 - Preparando o dado antes de iniciar o treino do modelo"""

X=data.drop(["fetal_health"], axis=1)
y=data["fetal_health"]

columns_names = list(X.columns)
scaler = preprocessing.StandardScaler()
X_df = scaler.fit_transform(X)
X_df = pd.DataFrame(X_df, columns=columns_names)

X_train, X_test, y_train, y_test = train_test_split(X_df, y, test_size=0.3, random_state=42)

y_train = y_train - 1
y_test = y_test - 1

y_train.value_counts()

X_train

"""# 4 - Criando o modelo e adicionando as camadas"""

reset_seeds()
model = Sequential()
model.add(InputLayer(input_shape=(4,)))
model.add(Dense(units=10, activation='relu'))
model.add(Dense(units=10, activation='relu'))
model.add(Dense(units=10, activation='relu'))
model.add(Dense(units=3, activation='softmax'))

model.summary()

"""# 5 - Compilando o modelo

"""

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

"""# 6 - Executando o treino do modelo"""

import os
import uuid
import mlflow

uri='https://dagshub.com/renansantosmendes/mlops-arda-t1.mlflow'
username = 'renansantosmendes'
token = 'dde6cf292052d838446b1a3bb55725c02c0735c9'

os.environ['MLFLOW_TRACKING_USERNAME'] = username
os.environ['MLFLOW_TRACKING_PASSWORD'] = token
mlflow.set_tracking_uri(uri)

mlflow.tensorflow.autolog()

with mlflow.start_run(run_name=f"run_{str(uuid.uuid4())}"):
  model.fit(x=X_train,
            y=y_train,
            epochs=60)