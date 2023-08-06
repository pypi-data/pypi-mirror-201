from gestionatr.cli import request_p0

P0_DEMO = {
    # Funcionen
    "Cadiz": {
        'url': "https://portaldistribucion.electricadecadiz.es/Sync?WSDL",
        'user': "0971",
        'password': "pmV9Cv3FkcEK",
        'cups': "ES0034111000013959YS0F",
        'emisora': "0971",
        'destino': "0034",
    },
    "Iberdrola": {
        'url': "https://www.i-de.es/cnmcws/agentes/sync?wsdl",
        'user': "EC980Y4",
        'password': "9UWyvGv39D",
        'cups': "ES0021000008103774WC0F",
        'emisora': "0373",
        'destino': "0021",
    },
    "Iberdrola - Lucera": {
        'url': "https://www.i-de.es/cnmcws/agentes/sync?wsdl",
        'user': "EC980CB",
        'password': "vxchsN7mi7",
        'cups': "ES0021000005075210RG",
        'emisora': "0971",
        'destino': "0021",
    },
    "Iberdrola - Gaba": {
        'url': "https://www.i-de.es/cnmcws/agentes/sync",
        'user': "EC9800N",
        'password': "^LZg$9J0[T",
        'cups': "ES0021000007770630PP",
        'emisora': "1664",
        'destino': "0021",
    },
    "Morella": {
        'url': "https://ov.maestrazgodistribucion.es/Sync?WSDL",
        'user': "0373",
        'password': "0373_aeQuee3F",
        'cups': "ES0189000038091476YE0F",
        'emisora': "0373",
        'destino': "0189",
    },
    "Endesa": {
        'url': "http://trader-eapi.de-c1.eu1.cloudhub.io/api/P0?wsdl",
        'user': "ea1f02cb9ed04a1da80496255df63870",
        'password': "78415Cd1a3e44798A87d642EF0171517",
        'cups': "ES0031300002599001TX0F",
        'emisora': "0706",
        'destino': "0031",
    },
    "Fenosa - Gaba": {
        'url': "https://sctd.gasnaturalfenosa.com/sctd/ws/Sync?wsdl",
        'user': "1664WSSAP",
        'password': "2022Mayo",
        'cups': "ES0022000004952905WA1P",
        'emisora': "1664",
        'destino': "0022",
    },
    "Fenosa": {
        'url': "https://sctd.gasnaturalfenosa.com/sctd/ws/Sync?wsdl",
        'user': "1664WSSAP",
        'password': "2022Mayo",
        'cups': "ES0022000006704409RB1P",
        'emisora': "1664",
        'destino': "0022",
    },
    "Viesgo": {
        'url': "https://viesgop0.app.viesgo.com/syncRequest.wsdl",
        'user': "0706",
        'password': "ENE190#06",
        'cups': "ES0027700037401002ZB0F",
        'emisora': "0706",
        'destino': "0282",
    },
    "ELECTRICA DE LA SERRANIA DE RONDA, S.L": {
        'url': "https://intercambioxml.electricaserraniaderonda.com/Sync/Sync.svc",
        'user': "0971",
        'password': "ef8d6c83-7",
        'cups': "ES0225000050200275EL0F",
        'emisora': "0971",
        'destino': "0225",
    },
    "Agri distri": {
        'url': "https://clients.agrienergiaelectrica.com/Sync?WSDL",
        'user': "0108",
        'password': "aks!AP2dmmm9",
        'cups': "ES0112000000015671QS0F",
        'emisora': "0108",
        'destino': "0112",
    },
    "Avellana": {
        'url': "https://gestioatr.electraavellana.com/Sync?WSDL",
        'user': "0091",
        'password': "JeeF>ah8",
        'cups': "ES0176000001900674NB0F",
        'emisora': "0091",
        'destino': "0176",
    },
    # # No funcionen encara
    #"Dielsur": {
    #    'url': "http://wsp0dielesur.portalswitching.com/WSCurvas.asmx?wsdl",
    #    'user': "1440",
    #    'password': "Test1440",
    #    'cups': "ES0143000000203855EW0F",
    #    'emisora': "1440",
    #    'destino': "0143",
    #},
    "CIDE": {
        'url': "https://switchingsync.sercide.com/BasicSYNCService.svc",
        'user': "0370_i1C6N",
        'password': "=mYow<umQV`aq",
        'cups': "ES0614000000000035ZJ0F",
        'emisora': "0706",
        'destino': "0614",
    },
    "SAN MIGUEL 2000 DISTRIBUCION ELECTRICA, S.L.U - Gaba": {
        'url': "https://switching.datacenter.gl/wsdl?",
        'user': "sw_gaba_1664",
        'password': "N2Y0ZWI4",
        'cups': "ES0350000005600013QS",
        'emisora': "1664",
        'destino': "0350",
    },
    "Mercedes": {
        'url': "https://switchingsync.sercide.com/BasicSYNCService.svc",
        'user': '0971_B5tGR',
        'password': 'l59?U~CfP:%s1',
        'cups': 'ES0148000000010108KA0F',
        'emisora': "0971",
        'destino': "0148"
    },
}

import sys
for distri in P0_DEMO:
    sys.stdout.write(("Testing {}...".format(distri)))
    try:
        res = request_p0(url=P0_DEMO[distri]["url"], user=P0_DEMO[distri]["user"], password=P0_DEMO[distri]["password"], params=P0_DEMO[distri])
        if "CodigoDePaso>02" not in res:
            print "ERROR"
        else:
            print "OK"
    except Exception as e:
        print "ERROR"
        # print e
