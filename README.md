# Topjob
<br/>
Proyecto final - IX Bootcamp - Big data, Machine Learning y IA - Keepcoding <br/>
URL de la web: https://secret-descent-361716.ey.r.appspot.com/ <br/>
<br/>
Colab modelo: Topjob.ipynb <br/>
<br/>
Colab NLP: nlp-analysis-keyword-extraction/nlp_keyword_extraction.ipynb <br/>
<br/>
El objetivo de este proyecto es crear un modelo que pueda predecir salarios en la industria de IT, basado en varias características como año de la oferta, nivel de experiencia, país de la compañía, etc.<br/>
-El dataset principal utilizado fue extraído de kaggle (https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries?datasetId=2268489&searchQuery=prediction). <br/>
-Luego se desarrollaron 2 scrypts para realizar scrappeo de los portales de búsqueda de empleo Indeed y Glassdoor.<br/>
<br/>
Una vez conseguidos los datasets, se procedió a realizar la limpieza y preprocesamiento: remover outliers, codificar variables categóricas, normalizar/escalar, transformar la variable objetivo.<br/>
Los modelos de regresión probados fueron: Ridge, Lasso, SVR (kernel lineal), gradient boosting, decision trees y random forest (el cual fue elegido).<br/>
Paralelamente, se utilizó la columna "job description" (descripción del empleo) para el análisis de NLP, extrayendo topics/temas y otras características del dataset.<br/>
Luego, se creó y subió la aplicación a Google Cloud para general la URL a la que se puede acceder para realizar predicciones en tiempo real con el modelo entrenado.<br/>
