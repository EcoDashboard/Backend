class CityDashboard:
    cityID = ""
    cityName = ""
    area = 0
    cityPopulation = 0
    lastProfileUpdateDate = ""
    cityCouncilData = None
    finalIndex = None

    def returnJson(self):
        return {
            'cityID' : self.cityID,
            'cityName' : self.cityName,
            'area' : float(self.area),
            'cityPopulation' : float(self.cityPopulation),
            'lastProfileUpdateDate' : self.lastProfileUpdateDate,
            'cityCouncilData' : self.cityCouncilData.returnJson()
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