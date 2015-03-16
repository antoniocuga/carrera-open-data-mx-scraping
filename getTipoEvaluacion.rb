require 'nokogiri'
require 'open-uri'
require 'csv'

CSV.open("tipoevaluacion.csv", "w") do |csv|
	csv << ['id','evaluacion']
    url = 'http://201.175.44.214/SNRSPD/Basica/SNRSPDresultadosbasica/ConsultaPublica.aspx'
    page = Nokogiri::HTML(open(url))	
    page.css("select[id='ddlExamen'] option").each do |option|
        #Aquí pueden escribir validaciones para evitar
        #obtener el primer valor del option: "--seleccionar .... ---"
        csv << [option["value"],(option.content).strip]
    end
end

