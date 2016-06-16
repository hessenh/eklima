
import urllib2
import numpy as np

def main():
    url = "http://eklima.met.no/metdata/MetDataService?invoke=getMetData&timeserietypeID=0&format=&from=2005-07-01&to=2005-07-02&stations=18700&elements=rr%2Ctan%2Ctax&hours=&months=&username="
    getMetData()


def getMetData():
    timeserietypeID_ = "0"
    format_ = ""
    from_ = "2005-07-01"
    to_ = "2005-07-03"
    stations_ = "18700"
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

    parese_xml(data)

def decode_id(s):
    repls = ('<id xsi:type="xsd:string">', ''), ('</id>', ''), ('\n', '')
    return reduce(lambda a, kv: a.replace(*kv), repls, s)
  
def decode_q(s):
    repls = ('<quality xsi:type="xsd:int">', ''), ('</quality>', ''), ('\n', '')
    return float(reduce(lambda a, kv: a.replace(*kv), repls, s))

def decode_v(s):
    repls = ('<value xsi:type="xsd:string">', ''), ('</value>', ''), ('\n', '')
    return float(reduce(lambda a, kv: a.replace(*kv), repls, s))

def decode_d(s):
    repls = ('<from xsi:type="xsd:dateTime">', ''), ('</from>', ''), ('\n', '')
    return reduce(lambda a, kv: a.replace(*kv), repls, s)

def parese_xml(xml_data):
    element_id = ""
    element_q = ""
    element_v = ""
    element_d = ""
    elements = []
    started_elemtent = False

    for line in xml_data:

        if '<item xsi:type="ns2:no_met_metdata_WeatherElement">\n' in line:
            started_elemtent = True

        if 'from xsi:type="xsd:dateTime' in line:
            element_d = decode_d(line)

        if 'id xsi:type="xsd:string' in line and started_elemtent:
            element_id = decode_id(line)
        
        if 'quality xsi:type="xsd:int' in line and started_elemtent:
            element_q = decode_q(line)

        if 'value xsi:type="xsd:string' in line and started_elemtent:
            element_v = decode_v(line)
            elements.append([element_id, element_q, element_v, element_d])
            started_elemtent = False

    print elements




if __name__ == "__main__":
    main()