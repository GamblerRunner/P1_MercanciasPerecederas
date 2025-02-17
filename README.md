# Reparto de mercancias perecederas (VRP)
> Proyecto 1 - Master IADB
> Video demostración: https://www.youtube.com/watch?v=9pYW6RixiMk

## Que hace este proyecto?
El objetivo de esta herramienta es generar las rutas que sean más eficientes en cuanto a coste de entrega y la predicción de la demanda mensual a traves de los datos historicos de demanda de cada cliente.  
Esta herramienta será útil para el negocio ya que podrá minimizar costes de reparto mediante las rutas eficientes y la posible reducción de flota, tambien podrán tener mejor gestión del inventario al poder predecir la demanda del mes siguiente.  
La herramienta será desarrollada con inteligencia artificial tanto para la predicción de demanda como para la eficiencia de rutas.

## Configuración y ejecución del proyecto
Para ejecutar este proyecto lo primero que se debe hacer es descargar el repositorio para tenerlo en local. Descomprimirlo con algun programa para ello y una vez se tienen las carpetas de una forma accesible hay 2 formas de lanzarlo.  
Antes de poder lanzar los notebooks se deben tener descargadas las diferentes librerias usadas en el proyecto, estas librerias y sus versiones estan escritas en el archivo requirements.txt  
La primera sería abrir los notebooks que estan en la carpeta Notebooks/modeling_final, cada notebook contiene uno de los casos a resolver en el proyecto. Abre el que quieras probar y dale al boton de run all.  
La segunda forma seria lanzar la página web creada para visualizar el proyecto, para lanzar la página debes usar el archivo .... y una vez puedas entrar a la página verás 4 botones, uno para cada caso del proyecto, y si clickas en esos botones verás la solucion al caso despues de unos segundos.

## Estructura del proyecto
El proyecto está dividido en diferentes carpetas y archivos que guardan desde los datos para entrenar y probar los modelos, la documentación y los diferentes archivos con código sobre modelos.
- Carpeta Datos_P1:   
    Carpeta que contiene los diferentes archivos .csv que aportan los datos principalmente para la generación del rutas eficientes.
    Los contenidos de cada archivo de datos junto con su desglose están en la documentación del proyecto.  
- Carpeta Documentación:  
    En esta carpeta están los archivos de documentación del proyecto como el analisis de los datos y el pdf de documentación general con la descripción de la tecnologias, analisis de las tecnologias de IA usadas y demás detalles tecnicos.
- Carpeta Notebooks:  
    En esta carpeta tenemos una imagen png con las localizaciones de los clientes en un mapa basado en los datos de localización que hay en uno de los archivos .csv.
    * Carpeta data_analyze: 
        Esta subcarpeta contiene un notebook con el analisis y representación de los datos del proyecto en diferentes gráficas y matrices de correlación.
    * Carpeta modeling_final:
        En esta carpeta están los notebooks con los que hemos acabado resolviendo los casos pedidos, estos notebooks deberían estar explicados en la documentación y con comentarios dentro de ellos. 
    * Carpeta modeling_pruebas: 
        Subcarpeta donde hemos estado guardando los diferentes notebooks con los modelos que hemos estado probando para la creación de rutas eficientes. 
- Carpetas de la página web:
    * Carpeta templates:
        En esta carpeta están los diferentes archivos .html que conforman la página web.
    * Carpeta static:
        En esta carpeta y las que haya dentro estan datos estaticos que se usarán en la visualización de la página web, desde los estilos de la página hasta los excels de datos para poder mostrarlos.
- Archivo README.md:  
    Archivo que estas leyendo ahora mismo con la explicación de lo que hace el proyecto, la configuración y ejecución y la estrcutura de las carpetas del proyecto.
- Archivo requirements.txt:   
    Archivo .txt con las diferentes librerias de python y sus versiones usadas en el proyecto. Usando las versiones escritas en el archivo todo el proyecto deberia funcionar sin problemas.
