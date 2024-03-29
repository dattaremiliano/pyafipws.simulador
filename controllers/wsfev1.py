# coding: utf8
# try something like

def index(): return dict(message="hello from wsfev1.py")


from gluon.tools import Service
service = Service(globals())

@service.soap('FEDummy',returns={'FEDummyResult': {'AppServer': str, 'DbServer': str, 'AuthServer': str}},args={})
def dummy(): 
    "Metodo dummy para verificacion de funcionamiento"
    db.request.insert(method='dummy')
    return {'FEDummyResult': {'AppServer': 'OK', 'DbServer': 'OK', 'AuthServer': 'OK'}}

@service.soap('FECompUltimoAutorizado',
    returns={'FECompUltimoAutorizadoResult': {
         'PtoVta': int, 'CbteTipo': int, 'CbteNro': int,
         'Events': [{'Evt': {'Code': int, 'Msg': unicode}}], 
         'Errors': [{'Err': {'Code': int, 'Msg': unicode}}]}},
    args={
        'Auth': {'Token': str, 'Sign': str, 'Cuit': str},
        'PtoVta': int, 'CbteTipo': int,
        })
def comp_ultimo_autorizado(Auth, PtoVta, CbteTipo): 
    u"Retorna el ultimo comprobante autorizado para el tipo de comprobante / cuit / punto de venta ingresado / Tipo de Emisión"
    try:
        db.request.insert(method='comp_ultimo_autorizado', args=repr({'Auth': Auth, 'PtoVta': PtoVta, 'CbteTipo': CbteTipo}))
        return {'FECompUltimoAutorizadoResult': {
             'PtoVta': PtoVta, 'CbteTipo': CbteTipo, 'CbteNro': 9999,
             'Events': [{'Evt': {'Code': 0, 'Msg': 'Esto es una SIMULACION!!!'}}], 
             'Errors': [{'Err': {'Code': 10001, 'Msg': 'Datos no validos - simulados'}}],
             }}
    except Exception, e:
        #raise
        ##raise RuntimeError(repr(e) + repr({'Auth': Auth, 'FeCAEReq': FeCAEReq}))
        raise RuntimeError("%s" % f['FECAEDetRequest'].keys())
 
@service.soap('FECAESolicitar',
    returns={'FECAESolicitarResult': {
        'FeCabResp': {'Cuit': long, 'PtoVta': int, 'CbteTipo': int, 
                      'FchProceso': str, 'CantReg': int, 'Resultado': unicode, 
                      'Reproceso': unicode}, 
        'FeDetResp': [{'FECAEDetResponse': 
            {'Concepto': int, 'DocTipo': int, 'DocNro': long, 
             'CbteDesde': long, 'CbteHasta': long, 'CbteFch': unicode, 
             'CAE': str, 'CAEFchVto': str,
             'Resultado': str, 
             'Observaciones': [{'Obs': {'Code': int, 'Msg': unicode}}]}}], 
         'Events': [{'Evt': {'Code': int, 'Msg': unicode}}], 
         'Errors': [{'Err': {'Code': int, 'Msg': unicode}}]}},
    args={
        'Auth': {'Token': str, 'Sign': str, 'Cuit': str},
        'FeCAEReq': {
            'FeCabReq': {'CantReg': int, 'PtoVta': int, 'CbteTipo': int},
            'FeDetReq': [{'FECAEDetRequest': {
                'Concepto': int,
                'DocTipo': int,
                'DocNro': long,
                'CbteDesde': long,
                'CbteHasta': long,
                'CbteFch': str,
                'ImpTotal': float,
                'ImpTotConc': float,
                'ImpNeto': float,
                'ImpOpEx': float,
                'ImpTrib':  float,
                'ImpIVA': float,
                'FchServDesde': str,
                'FchServHasta': str,
                'FchVtoPago': str,
                'MonId': str,
                'MonCotiz': float,
                'CbtesAsoc': [
                {'CbteAsoc': {'Tipo': int, 'PtoVta': int, 'Nro': long}}
                ],
                'Tributos': [
                {'Tributo': {
                    'Id': int, 
                    'Desc': unicode,
                    'BaseImp': float,
                    'Alic': float,
                    'Importe': float,
                    }}
                ],
                'Iva': [ 
                {'AlicIva': {
                    'Id': int,
                    'BaseImp': float,
                    'Importe': float,
                    }}
                ],
                },
            }],
        }})
def cae_solicitar(Auth, FeCAEReq): 
    "Solicitud de Codigo de Autorizacion Electronico (CAE)"
    try:
        
        FeCabReq = FeCAEReq['FeCabReq']
        FeDetReq = FeCAEReq['FeDetReq']
        db.request.insert(method='cae_solicitar', args=repr({'Auth': Auth, 'FeCAEReq': FeCAEReq}))
        return {'FECAESolicitarResult': {
            'FeCabResp': {'Cuit': Auth['Cuit'], 
                          'PtoVta': FeCabReq['PtoVta'], 'CbteTipo': FeCabReq['CbteTipo'], 
                          'CantReg': FeCabReq['CantReg'], 
                          'FchProceso': "20101006", 
                          'Resultado': "A", 
                          'Reproceso': "N"}, 
            'FeDetResp': [{'FECAEDetResponse': 
                {'Concepto': f['FECAEDetRequest']['Concepto'], 
                 'DocTipo': f['FECAEDetRequest']['DocTipo'], 'DocNro': f['FECAEDetRequest']['DocNro'], 
                 'CbteDesde': f['FECAEDetRequest']['CbteDesde'], 'CbteHasta': f['FECAEDetRequest']['CbteHasta'], 
                 'CAE': "123456789012345",
                 'CbteFch': f['FECAEDetRequest']['CbteFch'], 
                 'CAEFchVto': f['FECAEDetRequest']['CbteFch'], 
                 'Resultado': "A", 
                 'Observaciones': [{'Obs': {'Code': 00, 'Msg': "Todo bien"}}]}} 
                      for f in FeDetReq], 
             'Events': [{'Evt': {'Code': 0, 'Msg': 'Esto es una SIMULACION!!!'}}], 
             'Errors': [{'Err': {'Code': 10001, 'Msg': 'Datos no validos - simulados'}}],
             }}
    except Exception, e:
        #raise
        ##raise RuntimeError(repr(e) + repr({'Auth': Auth, 'FeCAEReq': FeCAEReq}))
        raise RuntimeError("%s" % f['FECAEDetRequest'].keys())
    
def call():
    response.title = u"Simulador Factura Electronica"
    response.subtitle = u"Simil Servicios Web AFIP Argentina"
    return service()

def test_dummy():
    from gluon.contrib.pysimplesoap.client import SoapClient

    WSDL="https://www.sistemasagiles.com.ar/simulador/wsfev1/call/soap?WSDL=None"
    client = SoapClient(wsdl = WSDL)
    
    try:
        ret = client.FEDummy()
    except:
        ret = client.xml_response
        
    response.view = "generic.html"
    return dict(ret=ret)

def test_ult():
    from gluon.contrib.pysimplesoap.client import SoapClient

    WSDL="https://www.sistemasagiles.com.ar/simulador/wsfev1/call/soap?WSDL=None"
    client = SoapClient(wsdl = WSDL)
    
    try:
        ret = client.FECompUltimoAutorizado(
                        Auth={'Token': 'token', 'Sign': 'sign', 'Cuit': '20267565393'},
                        PtoVta=1, CbteTipo=10
                        )
    except:    
        raise
        ret = client.xml_response
        
    response.view = "generic.html"
    return dict(ret=ret)
     

def test():
    from pysimplesoap.client import SoapClient

    WSDL="https://www.sistemasagiles.com.ar/simulador/wsfev1/call/soap?WSDL=None"
    client = SoapClient(wsdl = WSDL)
    
    try:
        ret = client.FECAESolicitar(
                    Auth={'Token': 'token', 'Sign': 'sign', 'Cuit': '20267565393'},
                    FeCAEReq={
                        'FeCabReq': {'CantReg':1, 'PtoVta': 1, 'CbteTipo': 10},
                        'FeDetReq': [{'FECAEDetRequest': {
                            'Concepto': 1,
                            'DocTipo': 80,
                            'DocNro': 20111111119,
                            'CbteDesde': 1,
                            'CbteHasta': 2,
                            'CbteFch': '20101006',
                            'ImpTotal': '1000.10',
                            'ImpTotConc': "10.00",
                            'ImpNeto': "100.00",
                            'ImpOpEx': "0.00",
                            'ImpTrib':  "1.00",
                            'ImpIVA': "21.00",
                            'FchServDesde': '20101101',
                            'FchServHasta': '20101130',
                            'FchVtoPago': '20101014',
                            'MonId': 'DOL',
                            'MonCotiz': '3.985',
                            'CbtesAsoc': [
                            {'CbteAsoc': {'Tipo': 19, 'PtoVta': 2, 'Nro': 1234}}
                            ],
                            'Tributos': [
                            {'Tributo': {
                                'Id': 0, 
                                'Desc': 'Impuesto Municipal Matanza',
                                'BaseImp': 150,
                                'Alic': 5.2,
                                'Importe': 5.8,
                                }}
                            ],
                            'Iva': [ 
                            {'AlicIva': {
                                'Id': 5,
                                'BaseImp': 100,
                                'Importe': 21,
                                }}
                            ],
                            }
                        }]
                    })
    except Exception, e:
        #ret = client.xml_response
        ret = repr(e) # # e.faultstring
    response.view = "generic.html"
    return dict(ret=ret)
