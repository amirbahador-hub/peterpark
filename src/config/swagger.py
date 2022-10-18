template = {
    "swagger": "2.0",
    "info": {
        "title": "Bookmarks API",
        "description": "API for PeterPark",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "amirbahador.develop@gmail.com",
        },
        "version": "1.0"
    },
    "basePath": "/",  
    "schemes": [
        "http",
        "https"
    ],
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
