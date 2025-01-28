# Reparto de mercancias perecederas (VRP)
> Proyecto 1 - Master IADB

## Que hace este proyecto?
El objetivo de esta herramienta es generar las rutas que sean más eficientes en cuanto a coste de entrega y la predicción de la demanda mensual a traves de los datos historicos de demanda de cada cliente.
Esta herramienta será útil para el negocio ya que podrá minimizar costes de reparto mediante las rutas eficientes y la posible reducción de flota, tambien podrán tener mejor gestión del inventario al poder predecir la demanda del mes siguiente.
La herramienta será desarrollada con inteligencia artificial tanto para la predicción de demanda como para la eficiencia de rutas.

## Configuración y ejecución del proyecto
> No comprendo muy bien que empezar a escribir aqui XD



## Estructura del proyecto
El proyecto está dividido en diferentes carpetas y archivos que guardan desde los datos para entrenar y probar los modelos, la documentación y los diferentes archivos con código sobre modelos.
- Carpeta Datos_P1: 
    Carpeta que contiene los diferentes archivos .csv que aportan los datos principalmente para la generación del rutas eficientes.
    > No se si tengo que explicar aqui los datos de cada archivo
- Carpeta Documentación:
    En esta carpeta están los archivos de documentación del proyecto como el analisis de los datos y el pdf de documentación general con la descripción de la tecnologias, analisis de las tecnologias de IA usadas y demás detalles tecnicos.
- Carpeta Notebooks:
    En esta carpeta tenemos una imagen png con las localizaciones de los clientes en un mapa basado en los datos de localización que hay en uno de los archivos .csv.
    * Carpeta data_analyze: 
        Esta subcarpeta contiene un notebook con el analisis y representación de los datos del proyecto en diferentes gráficas y matrices de correlación.
    * Carpeta modeling: 
        Subcarpeta donde hemos estado guardando los diferentes notebooks con los modelos que hemos estado probando para la creación de rutas eficientes. 
        > No se si esto lo tendré que cambiar cuando metamos los notebooks finales o si tengo que explicar el contenido de los notebooks.
- Archivo README.md:
    Archivo que estas leyendo ahora mismo con la explicación de lo que hace el proyecto, la configuración y ejecución y la estrcutura de las carpetas del proyecto.
- Archivo requirements.txt: 
    Archivo .txt con las diferentes librerias de python y sus versiones usadas en el proyecto. Usando las versiones escritas en el archivo todo el proyecto deberia funcionar sin problemas.