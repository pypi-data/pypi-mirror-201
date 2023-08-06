import requests

PROJECTS='/projects'
STUDIES='/studies'
EXPRESSIONS='/expressions'
CONTINUOUS='/continuous'
TICKET='/ticket'
FILTER='/filters'
BYTES='/bytes'
FORMATS='/formats'
UNITS='/units'

gtex = 'http://gtexportal.org/rnaget'
encode = 'https://rnaget.encodeproject.org'

FILTER_TYPES = {
    'projects': PROJECTS+FILTER,
    'studies':STUDIES+FILTER,
    'expressions':EXPRESSIONS+FILTER,
    'conitnuous':CONTINUOUS+FILTER
}

def get_response(request_dict):
    try:
        response = requests.get(**request_dict)
        is_json = 'stream' not in request_dict.keys()
        ##clean extra request params after successfull request
        for param in ['stream', 'params']:
            if param in request_dict.keys():
                del request_dict[param]

        if is_json:
            return response.json()
        else:
            return response.iter_content()

    except requests.exceptions.RequestException as e:
        print('Error requesting the URI:',request_dict['url'])
        print('Error message:',e)

class RnaGet:
    """
    A python RNAget Client class.
    Attributes
    ----------
    host : string (required)
        The RNAget host server URL
    token : string
        The access token used to access protected data (if implemented by the host server)
    """
    def __init__(self, host, token=None, service_info=False):

        ##set host
        if host == 'gtex':
            self.host = gtex
        elif host == 'encode':
            self.host = encode
        else:
            self.host=host

        self.request_dict = dict()

        ##set token
        if token:
            self.request_dict['headers']={"Authorization": f"Bearer {token}"}

        #print host service-info
        if service_info:
            self.request_dict['url']=f"{host}/service-info"
            response = get_response(self.request_dict)
            print(response)

    """
    Get model filters, accepted values are: projects, studies, expressions or continuous.
    Attributes
    ----------
    type : string (required)
        Accepted values are projects, studies, expressions or continuous
    params: dict
        In case of expressions, filters can be further queried by feature or sample
        example value: {'type':'feature'} or {'type':'sample'}

    """
    def get_filters(self, type, params=None):
        if not type in FILTER_TYPES.keys():
            print('type must be one of:',FILTER_TYPES.keys())
            return
        endpoint = FILTER_TYPES[type]
        self.request_dict['url'] = self.host+endpoint
        if params:
            self.request_dict['params']=params
        return get_response(self.request_dict)

    """
    Get project list
    Attributes
    ----------
    version : number
        version to filter by
    """
    def get_projects(self, version=None):
        if version:
            self.request_dict['params'] = {'version':version}
        self.request_dict['url'] = self.host+PROJECTS
        return get_response(self.request_dict)

    """
    Get project by id
    Attributes
    ----------
    id : string (required)
        project id
    """
    def get_project(self, id):
        self.request_dict['url'] = f"{self.host+PROJECTS}/{id}"
        return get_response(self.request_dict)

    """
    Get study by id
    Attributes
    ----------
    id : string (required)
        study id
    """
    def get_study(self,id):
        self.request_dict['url'] = f"{self.host+STUDIES}/{id}"
        return get_response(self.request_dict)

    """
    Get study list
    Attributes
    ----------
    version : number
        version to filter by
    """
    def get_studies(self, version=None):
        if version:
            self.request_dict['params'] = {'version':version}
        self.request_dict['url'] = self.host+STUDIES
        return get_response(self.request_dict)

    """
    Get expression list
    Attributes
    ----------
    format: string (required)
        response format type (this may be different between data providers)
    download : boolean (default: False)
        True --> request the /bytes endpoint
        False --> request the /ticket endpoint
    **kwargs:
        extra request params, may be different between data providers
    """
    def get_expression_list(self, format, download=False, **kwargs):
        self.request_dict['params'] =  dict(format=format, **kwargs)
        if download:
            self.request_dict['stream'] = True
            url = self.host+EXPRESSIONS+BYTES
        else:
            url = self.host+EXPRESSIONS+TICKET
        self.request_dict['url'] = url
        return get_response(self.request_dict)

    """
    Get expression object
    Attributes
    ----------
    id : string (required)
    download : boolean (default: False)
        True --> request the /bytes endpoint
        False --> request the /ticket endpoint
    **kwargs:
        extra request params, may be different between data providers
    """
    def get_expression(self, id, download=False, **kwargs):
        if kwargs.keys():
            self.request_dict['params'] = dict(**kwargs)
        if download:
            self.request_dict['stream'] = True
            url = f"{self.host+EXPRESSIONS}/{id+BYTES}"
        else:
            url = f"{self.host+EXPRESSIONS}/{id+TICKET}"
        self.request_dict['url'] = url
        return get_response(self.request_dict)

    """
    Get data formats
    """
    def get_expression_formats(self):
        self.request_dict['url'] = self.host+EXPRESSIONS+FORMATS
        return get_response(self.request_dict)

    """
    Get units
    """
    def get_expression_units(self):
        self.request_dict['url'] = self.host+EXPRESSIONS+UNITS
        return get_response(self.request_dict)

    """
    Get continuous list
    Attributes
    ----------
    format: string (required)
        response format type (this may be different between data providers)
    download : boolean (default: False)
        True --> request the /bytes endpoint
        False --> request the /ticket endpoint
    **kwargs:
        extra request params, may be different between data providers
    """
    def get_continuous_list(self, format, download=False, **kwargs):
        self.request_dict['params'] =  dict(format=format, **kwargs)
        if download:
            self.request_dict['stream'] = True
            url = self.host+CONTINUOUS+BYTES
        else:
            url = self.host+CONTINUOUS+TICKET
        self.request_dict['url'] = url
        return get_response(self.request_dict)

    """
    Get continuous object
    Attributes
    ----------
    id : string (required)
    download : boolean (default: False)
        True --> request the /bytes endpoint
        False --> request the /ticket endpoint
    **kwargs:
        extra request params, may be different between data providers
    """
    def get_continuous(self, id, download=False, **kwargs):
        if kwargs.keys():
            self.request_dict['params'] = dict(**kwargs)
        if download:
            self.request_dict['stream'] = True
            url = f"{self.host+CONTINUOUS}/{id+BYTES}"
        else:
            url = f"{self.host+CONTINUOUS}/{id+TICKET}"
        self.request_dict['url'] = url
        return get_response(self.request_dict)