import json

class CityDashboard:
    cityID = ""
    cityName = ""
    area = 0
    cityPopulation = 0
    lastProfileUpdateDate = ""
    cityCouncilData = None
    finalIndex = None
    categories = None

    def returnJson(self):
        return {
            'cityID' : self.cityID,
            'cityName' : self.cityName,
            'area' : float(self.area),
            'cityPopulation' : float(self.cityPopulation),
            'lastProfileUpdateDate' : self.lastProfileUpdateDate,
            'cityCouncilData' : self.cityCouncilData.returnJson(),
            'categories' : json.dumps(i.returnJson() for i in self.categories)
        }

class CityCouncil:
    name = ""
    address = ""
    contact = None
    def returnJson(self):
        return {
            'name' : self.name,
            'address' : self.address,
            'contactInfo' : self.contact.returnJson()
        }

class ContactInfo:
    name = ""
    phone = ""
    email = ""
    def returnJson(self):
        return {
            'name' : self.name,
            'phone' : self.phone,
            'email' : self.email
        }

class FinalIndex:
    id = ""
    name = ""
    indexIDValue = ""
    lastUpdateDate = ""
    def returnJson(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'indexIDValue' : self.indexIDValue,
            'lastUpdateDate' : self.lastUpdateDate
        }

class Categories:
    categoryId = ""
    categoryName = ""
    categoryScore = 0.0
    categoryWeight = 0.0
    indicators = None
    def returnJson(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'indexIDValue' : self.indexIDValue,
            'lastUpdateDate' : self.lastUpdateDate,
            'indicators' : json.dumps(i.returnJson() for i in self.indicators)
        }

class IndicatorData:
    indicatorId = ""
    indicatorName = ""
    originScore = 0.0
    scaledScore = 0.0
    def returnJson(self):
        return {
            'indicatorId' : self.indicatorId,
            'indicatorName' : self.indicatorName,
            'originScore' : self.originScore,
            'scaledScore' : self.scaledScore
        }
