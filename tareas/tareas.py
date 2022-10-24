import os
from ..modelos import db, Tarea 




for tarea in Tarea.query.all():
    os.system('ffmpeg -i ~/Documents/Maestria/II_semestre/cloud_desarrollo/proyecto/Api_SistemaConversionClud_MVTQN/archivos_originales/{} ~/Documents/Maestria/II_semestre/cloud_desarrollo/proyecto/Api_SistemaConversionClud_MVTQN/archivos_procesados/{}'.format(tarea.nombre_archivo,tarea.nombe_archivo.split(".")[0]+tarea.nuevo_formato))