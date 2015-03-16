# carrera-open-data-mx-scraping
Sesión de introducción de scrapeo de páginas web en la Carrera Open Data MX

###Página de extracción
**http://201.175.44.214/SNRSPD/Basica/SNRSPDresultadosbasica/ConsultaPublica.aspx**


##Python
import.py > Script en python usando TOR para anonimizar los request, este script es básico, aun pueden optimizar los request y añadir validaciones. Otra cosa es que pueden explorar mucho más la web y ver si requiere que se añada más funcionalidades para la extracción. Todo lo descargado es guardado en un archivo CSV, tambien podrian agregar una base de datos si así lo requieren.

##Ruby
getTipoEvaluacion.rb >> Script básico de extracción con Ruby usando la gema Nokigiri. Hemos sacado los valores del Select de Tipos de Evaluación. Pueden seguir el ejemplo del Script en Python para hacer lo mismo pero en Ruby.


