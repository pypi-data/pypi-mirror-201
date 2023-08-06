Antonio San Román 



**pdf_view(self,master,width=1200,height=600,pdf_location="",bar=True,load="after")**
			Crea la interface grafica para moverse por las paginas del documento con dos botones gráficos Avanzar/Retroceder.

**FuncsVisorPDF**

_grid_by_column(cuadro, columns, spacex=6, spacey=6)_

	Distribuye los botones de avanzar y retroceder por las paginas PDF; y la etiqueta que los datos del 	documento obtenidos con otra función de forma autónoma a la visualización del documento.

*metaDataPDF(archivo)*
		 Recoge los metadatos de documento PDF (titulo, autor y fecha de creación) y los devuelve en estructura directory de forma autónoma a la visualización.

*defEstado(archivo)*
		 Recoge en estructura clave-valor el estado de botón (avance/retroceso) y las imágenes que representen estos estados según tenga sólo una pagina o más.
		
*desglosaPDF(archivo)*
			 Crea una imagen jpg por pagina de documento PDF.

*outFondo(origen, destino)*
			Quita fondo a imagen de botón (avance/retroceso)

 *cargaPagPDF(archivo, índice)*
		   Incorpora a visualización de documento PDF la imagen jpg con la pagina indicada por segundo parámetro.





