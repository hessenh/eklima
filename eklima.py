import pandas as pd
import urllib2
import numpy as np

def main():
    station = "27120"
    from_date = "2010-07-01"
    to_date = "2016-07-30"
    
    #getStationsProperties()
    getMetData(from_date, to_date, station)

def save_dataFrame(df, path):
    df.to_csv(path, index=None)
    print 'Dataframe saved to:',path


def getStationsProperties():
    request = 'http://eklima.met.no/met/MetService?invoke=getStationsProperties&stations=&username='
    response = urllib2.urlopen(request)
    data = response.readlines()
    dataFrame = parese_getStationsProperties(data)
    save_dataFrame(dataFrame, 'stations.csv')


def getMetData(from_date, to_date, station_id):
    timeserietypeID_ = "0"
    format_ = ""
    from_ = from_date #"2005-07-01"
    to_ = to_date #"2005-07-30"
    stations_ = station_id #"18700"
    elements_ = "rr%2Ctan%2Ctax"
    hours_ = ""
    months_ = ""
    username_ = ""

    root_url = "http://eklima.met.no/metdata/MetDataService?invoke="
    method = "getMetData"
    request = root_url + method + \
    '&timeserietypeID='+timeserietypeID_ + \
    '&format=' + format_ + \
    '&from=' + from_ + \
    '&to=' + to_ + \
    '&stations=' + stations_ + \
    '&elements=' + elements_ + \
    '&hours=' + hours_ + \
    '&months=' + months_ + \
    '&username=' + username_


    response = urllib2.urlopen(request)
    data = response.readlines()

    path = 'data/' + station_id + '_' +  from_date + '_' + to_date + '.csv'
    save_dataFrame(parese_getMetaData(data), path)

def decode_general(s, first, second):
    repls = (first, ''), (second, ''), ('\n', '')
    return reduce(lambda a, kv: a.replace(*kv), repls, s)

def parese_getStationsProperties(xml_data):
    started_elemtent = False
    elements = []
    
    for line in xml_data:

        if '<fromDay xsi:type="xsd:int">' in line:
            elements.append(decode_general(line, '<fromDay xsi:type="xsd:int">', '</fromDay>'))
        if '<fromMonth xsi:type="xsd:int">' in line:
            elements.append(decode_general(line, '<fromMonth xsi:type="xsd:int">', '</fromMonth>'))
        if '<fromYear xsi:type="xsd:int">' in line:
            elements.append(decode_general(line, '<fromYear xsi:type="xsd:int">', '</fromYear>'))
        if '<toDay xsi:type="xsd:int">' in line:
            elements.append(decode_general(line, '<toDay xsi:type="xsd:int">', '</toDay>'))
        if '<toMonth xsi:type="xsd:int">' in line:
            elements.append(decode_general(line, '<toMonth xsi:type="xsd:int">', '</toMonth>'))
        if '<toYear xsi:type="xsd:int">' in line:
            elements.append(decode_general(line, '<toYear xsi:type="xsd:int">', '</toYear>'))

        if '<stnr xsi:type="xsd:int">' in line:
            elements.append(decode_general(line, '<stnr xsi:type="xsd:int">', '</stnr>'))
        if '<department xsi:type="xsd:string">' in line:
            elements.append(decode_general(line, '<department xsi:type="xsd:string">', '</department>'))
        if '<department xsi:type="xsd:string" xsi:nil="true"/>' in line:
            elements.append(decode_general(line, '<department xsi:type="xsd:string" ', 'xsi:nil="true"/>'))  
        if '<name xsi:type="xsd:string">' in line:
            elements.append(decode_general(line, '<name xsi:type="xsd:string">', '</name>'))
        if '<latDec xsi:type="xsd:double">' in line:
            elements.append(decode_general(line, '<latDec xsi:type="xsd:double">','</latDec>'))
        if '<lonDec xsi:type="xsd:double">' in line:
            elements.append(decode_general(line, '<lonDec xsi:type="xsd:double">','</lonDec>'))
 
    elements = np.reshape(elements, (len(elements)/11,11))
    df = pd.DataFrame(elements)
    df.columns = ['department', 'from_day','from_month', 'from_year','lat', 'lon','name', 'stnr', 'to_day', 'to_month', 'to_year']
    return df


def parese_getMetaData(xml_data):
    elements = []
    started_elemtent = False

    for line in xml_data:
        if 'from xsi:type="xsd:dateTime' in line:
            elements.append(decode_general(line, '<from xsi:type="xsd:dateTime">', '</from>'))
            started_elemtent = True
      
        if '<quality xsi:type="xsd:int">' in line and started_elemtent:
            elements.append(decode_general(line, '<quality xsi:type="xsd:int">', '</quality>'))

        if 'value xsi:type="xsd:string' in line and started_elemtent:
            elements.append(decode_general(line, '<value xsi:type="xsd:string">', '</value>'))

    elements = np.reshape(elements, (len(elements)/7,7))
    df = pd.DataFrame(elements)
    df.columns = ['date', 'RR_quality','RR_value', 'TAX_quality','TAX_value', 'TAN_quality','TAN_value']
    return df




if __name__ == "__main__":
    main()