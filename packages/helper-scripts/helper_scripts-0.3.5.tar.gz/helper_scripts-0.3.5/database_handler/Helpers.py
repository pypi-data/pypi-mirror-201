import pandas as pd
import datetime
import uuid
import base64
import pytz
import gzip
import zlib
from string import ascii_lowercase
import itertools
import math
from decimal import Decimal,ROUND_UP

class Helpers:
    def convert_dataframe_to_string(self, dataframe):
        df = pd.DataFrame(dataframe)
        df = df.to_string(header=False, index=False, index_names =False).split('\n')
        df = [','.join(ele.split()) for ele in df]
        return df
    
    def current_datetime_24hrs(self):
        today = datetime.datetime.now(tz=pytz.timezone('Africa/Nairobi'))
        date_time = today.strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    def current_date_yymmdd(self):
        today = datetime.datetime.now(tz=pytz.timezone('Africa/Nairobi'))
        tdate = today.strftime("%y%m%d")
        return tdate

    def current_date_yy_mm_dd(self):
        today = datetime.datetime.now(tz=pytz.timezone('Africa/Nairobi'))
        tdate = today.strftime("%y-%m-%d")
        return tdate
    
    def data_exchange_id(self):
        id = uuid.uuid1()
        return id.hex
    
    def generate_content_json_file(self, content, mode):
        with open('json_output/content.json', mode) as f:
            print(content, file=f)
    
    def generate_request_json_file(self, request, mode):
        with open('json_output/request.json', mode) as f:
            print(request, file=f)

    def generate_response_json_file(self, response, mode):
        with open('json_output/response.json', mode) as f:
            print(response, file=f)

    def generate_response_content_file(self, response, mode):
        with open('json_output/output.txt', mode) as f:
            print(response, file=f)
    
    def encode_json_to_base64(self, json_data):
        return base64.b64encode(bytes(json_data,encoding="utf8"))
    
    def decode_base64(self, encoded_data):
        return base64.b64decode(encoded_data).decode('utf8')

    def decode_base64_2(self, encoded_data):
        return base64.b64decode(encoded_data)

    def decompress_string(self,data):
        data = self.decode_base64_2(data)
        return gzip.decompress(data).decode('utf8')

    def has_excise_tax(self, data):
        returnvalue = None
        if data in ('no','No','NO'):
            returnvalue = '102' 
        elif data in ('yes','Yes','YES'):
            returnvalue = '101'
        else:
            returnvalue = '102'

        return returnvalue
    
    def get_currency(self, data):
        returnvalue = None
        if data == 'USD':
            returnvalue = 'USD' 
        elif data == 'UGX':
            returnvalue = 'UGX'
        elif data == 'EUR':
            returnvalue = 'EUR'
        elif data == 'GBP':
            returnvalue = 'GBP'
        elif data == 'ZAR':
            returnvalue = 'ZAR'
        else:
            returnvalue = data
            
        return returnvalue
    
    def get_currency_2(self, data):
        returnvalue = None
        if data == 'USD':
            returnvalue = '102' 
        elif data == 'UGX':
            returnvalue = '101'
        elif data == 'EUR':
            returnvalue = '104'
        elif data == 'GBP':
            returnvalue = '103'
        elif data == 'ZAR':
            returnvalue = '107'
        else:
            returnvalue = data
            
        return returnvalue
    
    def get_unit_measure(self, data):
        returnvalue = None
        if data in ('PP-Piece','Piece','piece'):
            returnvalue = 'PP' 
        elif data in ('UN-Unit','unit','Unit'):
            returnvalue = 'UN'
        elif data in ('Kit','KI-Kit', 'kit'):
            returnvalue = 'KI'
        elif data in ('kg','Kg','kgs','KGs'):
            returnvalue = '103'
        elif data in ('Litre','litre','L','l'):
            returnvalue = '102'
        elif data in ('SET-Set','Set','set'):
            returnvalue = 'SET'
        elif data in ('Manhours','manhours'):
            returnvalue = '205'
        elif data in ('Minute','minute'):
            returnvalue = '105'
        elif data in ('Hours','hours','HR','hr'):
            returnvalue = '207'
        elif data in ('HR-Hamper','hr-hamper','Hamper','hamper'):
            returnvalue = 'HR'
        elif data in ('Per annum', 'per annum', 'Per Annum'):
            returnvalue = '116'
        elif data in ('Per month', 'per month', 'Per Month'):
            returnvalue = '115'
        elif data in ('Metre', 'metre','Meter', 'meter'):
            returnvalue = '200'
        elif data in ('Time of use', 'time of use'):
            returnvalue = '203'
        else:
            returnvalue = data
            
        return returnvalue
    
    def get_buyer_type(self, data):
        returnvalue = None
        if data in ('B2B','B2G'):
            returnvalue = '0' 
        elif data == 'B2C':
            returnvalue = '1'
        elif data in ('B2Foreigner','B2F'):
            returnvalue = '2'
        else:
            returnvalue = '0'
            
        return returnvalue

    def get_max_value_from_array(self, array_name, column_number):
       
        #return str(max(row[column_number] for row in array_name if row[column_number] != None))
        '''
        Return thr first None Value or None if all values are None
        '''
        return next((row[column_number] for row in array_name if row[column_number] != None), None)
        
        
    
    def get_sum_from_array(self, array_name, column_number):
       
            return sum(row[column_number] for row in array_name)

    def get_tax_category_code(self, taxAmount):
        returnValue = None
        if taxAmount == 0 :
            returnValue = '02'
        elif not taxAmount:
            returnValue = '03'
        else:
            returnValue = '01'

        return returnValue
    
    def get_tax_rate(self, taxAmount):
        returnValue = None
        if taxAmount == 0 :
            returnValue = '0'
        elif not taxAmount:
            returnValue = '-'
        else:
            returnValue = '0.18'
            
        return returnValue

    
    def generate_the_alphabet(self):
        for size in itertools.count(1):
            for s  in itertools.product(ascii_lowercase, repeat=size):
                yield "".join(s)
    
    def get_the_alphabet(self):
        alphabet_array = []
        for s in self.generate_the_alphabet():
            alphabet_array.append(s)
            if s == 'zzz':
                break
        return alphabet_array
    
    def round_2dp(self, f, location='everywhere'):
        if not f:
            return 0
        else:
            return "{:.2f}".format(float(f))
            #return (Decimal(f).quantize(Decimal('0.01'),rounding=ROUND_UP))
    
    def round_2dp_corrected_rounding_error(self, f, location='everywhere'):
        if not f:
            return 0
        
        elif Decimal(f).as_tuple().exponent * -1 <= 2:
            #print ('Am using normal rounding on %s'%(location))
            return "{:.2f}".format(float(f))
            #return float(f)
        else:
            #return "{:.2f}".format(float(f))
            #print ('Am using special rounding on %s'%(location))
            return (Decimal(f).quantize(Decimal('1.00')))
        
    def truncate(self, f, n):
        return str(math.floor(float(f) * 10 ** int(n)) / (10 ** int(n)))

    def round(self, the_number,n):
        return "{:.2f}".format(float(the_number))
    
    def convert_dataframe_to_string(self, dataframe):
        df = pd.DataFrame(dataframe)
        df = df.to_string(header=False, index=False, index_names =False).split('\n')
        df = [','.join(ele.split()) for ele in df]
        return df
    
    def get_material_code_from_error_msg(self, failure_reason):

        y = failure_reason

        print(y)

        pos1 = 18+y.index('proceed.item code')

        pos2 = y.index(', item')
 
        z = y[pos1:pos2]

        #print(pos1)

        #print(pos2)

       

        return z
    
    def get_material_name_from_error_msg_for_unit_of_measure(self, failure_reason):

        y = failure_reason

        pos1 = 13+y.index('maintenance.(')

        pos2 = y.index('s unit of measure')

        z = y[pos1:pos2]

        #print(pos1)

        #print(pos2)

        #print(z)

        return z
        