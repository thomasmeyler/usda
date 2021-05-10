import pandas as pd
import requests

apiKey = 'APIKEYHERE'

class esrClient:

    def __init__(self,apiKey):

        self.url = 'https://apps.fas.usda.gov/OpenData/api/esr/'
        self.headers_dict =  {"API_KEY":apiKey}
        list_endpoints = ['commodities','countries','regions','unitsOfMeasure','datareleasedates'] 
        all_endpoints = [pd.DataFrame.from_dict(requests.get(url=self.url+_, headers=self.headers_dict).json()) for _ in list_endpoints]
        all_endpoints = zip(list_endpoints,all_endpoints)
        self.all_endpoints = dict(all_endpoints)

        
    def all_countries(self,commod,year,names=False):
        cDict = self.all_endpoints['commodities']
        cCode = cDict[cDict['commodityName'].str.lower().str.contains(commod)].commodityCode
        url2 = self.url + 'exports/commodityCode/'+str(cCode.item())+'/allCountries/marketYear/'+str(year)
        data = pd.DataFrame.from_dict(requests.get(url=url2, headers=self.headers_dict).json())
        if names is True:
            dt = self.all_endpoints['countries']
            nameDict = dict(zip(dt.countryCode,dt.countryName))
            data['countryCode'] = [nameDict[_] for _ in data.countryCode]
        return(data)

    def country_sales(self,commod,country,year,names=False):
        cDict = self.all_endpoints['commodities']
        cCode = cDict[cDict['commodityName'].str.lower().str.contains(commod)].commodityCode

        cnDict = self.all_endpoints['countries']
        cnCode = cnDict[cnDict['countryName'].str.lower().str.contains(country)].countryCode
        
        url2 = self.url + 'exports/commodityCode/'+str(cCode.item())+'/countryCode/'+str(cnCode.item())+'/marketYear/'+str(year)
        data = pd.DataFrame.from_dict(requests.get(url=url2, headers=self.headers_dict).json())
        if names is True:
            dt = self.all_endpoints['countries']
            nameDict = dict(zip(dt.countryCode,dt.countryName))
            data['countryCode'] = [nameDict[_] for _ in data.countryCode]
        return(data)

