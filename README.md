# BotDocente

## Autor:
Ezequiel Binker

## Fecha:
Julio 2020

## Versión:
1.0

## Estado:
En desarrollo

## Descripción:
La inteligencia artificial permite resolver diversos problemas del humano en su vida cotidiano, como puede ser la **desorganización, la presencia física o la falta de productividad**. En este caso, el proyecto está orientado a resolver una problemática de tiempos, en los cuales utilizando ciertas técnicas de aprendizaje automático, se puede **facilitar el trabajo de los trabajadores de la educación**, en lo que respecta principalmente la misma a distancia. 

## Identificación del Problema:
Un evento bastante que ocurre frecuentemente en la educación a distancia, y mayor aún en las épocas que hemos vivido y vivimos en cuarentena, es la aparición de preguntas durante todo el día de los estudiantes hacia docentes, no importa qué rama de conocimiento conozca, o en qué materia/s está dictando clases. 

## Objetivo:
Desarrollar un **bot** alojado en la plataforma Telegram que pueda entrenarse en el conocimiento de una materia, y que pueda funcionar **como asistente de dichas consultas en todo momento 24x7**, para alivianar la carga del docente, o derivar las preguntas que son realmente de un nivel de comprensión y análisis mayor, liberándose de aquellas simples como, por ejemplo: "¿Qué significa MVC?”, “Características de un sistema”, entre otras. 

## Tecnologías implementadas
* Python
* Pandas
* Flask Framework
* Telegram Bot API
* SQLite
* NLTK
* Python-pptx
* PyPDF2
* SpaCy

## Ejecución
Para ejecutar este proyecto: 
1. Clonar el repositorio ```git clone https://github.com/ezebinker/BotDocente-Telegram.git```
2. Posicionarse en la raíz ```cd BotDocente-Telegram```
3. Iniciar el servidor Flask ```python app.py```
4. Levantar una URL pública con ngrok ```./ngrok http 5000```
5. Ingresar a la URL provista por ngrok y al final escribir /setwebhook para que el bot escuche ese endpoint