import datetime


def check_type_document(document_id):
    # DNI
    if( document_id == 4):
        return 1
    # Passport
    if( document_id == 2):
        return 7
    # Tax Identification Number -> RUC
    if (document_id == 8):
        return 6
    #Default
    return 1

def check_type_voucher(type_voucher):
    if(type_voucher=='factura'):
        return 1
    elif(type_voucher=='boleta_venta'):
        return 2
    elif(type_voucher == 'nota_credito'):
        return 3
    elif(type_voucher == 'nota_debito'):
        return 4
    return 1

def extract_serial(invoice_name):
    return invoice_name.rpartition("-")[0]

'''Not necesary if had the sequence of invoice'''
def extract_sequence(invoice_name):
    return int(invoice_name.partition("-")[2])

def format_date(date):
    string_date = date.strftime('%d/%m/%Y')
    format_date = datetime.datetime.strptime(string_date.replace('/','-'),'%d-%m-%Y')
    return format_date.strftime('%d-%m-%Y')

def check_currency(currency_id):
    #Check PEN (S/. )
    if(currency_id == 162):
        return 1
    #Check USD $
    elif(currency_id == 2):
        return 2
    #Check EUR
    elif(currency_id == 1):
        return 3
    return 1

def extract_serial_by_type_document(type_voucher):
    if (type_voucher == 'factura'):
        return 'FFF1'
    elif (type_voucher == 'boleta_venta'):
        return 'BBB1'
    return '0000'