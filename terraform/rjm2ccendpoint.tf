
resource "kong_service" "mainurl_service" {
	count = var.mainurl_include ? 1 : 0

	name     	= format("TF_%s_MAINURL", var.ws_name)
	protocol 	= "http"
	host     	= format("TF_%s_%s", var.ws_name, var.mainurl_majorversion)
  # host     	= kong_upstream.upstream[count.index].name
	port     	= 80
	path     	= var.mainurl_destpath
	retries  	= 5
	connect_timeout = 60000
	write_timeout 	= 60000
	read_timeout  	= 60000
}

resource "kong_route" "mainurl_route" {
	count = var.mainurl_include ? 1 : 0

	protocols 	    = [ "http", "https" ]
	hosts 		    = [ var.mainurl ]
	paths 		    = [ ]
	strip_path 	    = false
	preserve_host 	= false
	regex_priority 	= 0
	service_id 	    = kong_service.mainurl_service[count.index].id
}

