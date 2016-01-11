class GroupNames:

  def __init__(self):
    self.namesQuantity = {}
    self.namesRevenue = {}
    self.count = 0
    self.totRev = 0
    self.totQuant = 0

  def getNameQuantity(self, name):
    return self.namesQuantity[name]
    
  def getNameRevenue(self, name):
    return self.namesRevenue[name] 
    
  def getCount(self):
    return self.count
    
  def getRev(self):
    return self.totRev
    
  def getQuant(self):
    return self.totQuant
    
  def addNameQuant(self, newKey, newValue):
    self.namesQuantity[newKey] = newValue
    
  def addNameRev(self, newKey, newValue):
    self.namesRevenue[newKey] = newValue
    
  def addTotalR(self, newRev):
    self.totRev += newRev
    
  def addTotalQ(self, newQ):
    self.totQuant += newQ 
    
class CategoryNames:

  def __init__(self):
    self.namesStand = {}
    self.catNameall = {}
    self.count = 0
    
  def getNameStandQuant(self, key, stand):
    return self.namesStand[key][stand]["Q"]
    
  def getNameStandRev(self, key, stand):
    return self.namesStand[key][stand]["R"]
    
  def addAll(self, newKey, newGroup, newQuant, newRev):
    self.catNameall[newKey] = []
    self.catNameall[newKey].append(newGroup)
    self.catNameall[newKey].append(newQuant)
    self.catNameall[newKey].append(newRev)
    
  def updateAll(self, key, group, newQuant, newRev):
    if self.catNameall[key]:
      newlist = self.catNameall[key] 
      totalQ = newlist[1] + newQuant
      totalR = newlist[2] + newRev
      del self.catNameall[key] 
      self.catNameall[key] = []
      self.catNameall[key].append(group)  
      self.catNameall[key].append(totalQ)
      self.catNameall[key].append(totalR)
    
  def addNameStand(self, newKey, newStand, newQuant, newRev):
    self.namesStand.update({newKey:{newStand:{"Q":newQuant, "R":newRev}}})
    
  def updateNameStand(self, key, stand, newQuant, newRev):
    if self.namesStand[key]:
      if stand in self.namesStand[key]:
        self.namesStand[key][stand]["Q"] += newQuant 
        self.namesStand[key][stand]["R"] += newRev 
      else:
        self.namesStand[key].update({stand:{"Q": newQuant, "R": newRev}})
    
  def addCount(self):
    self.count += 1 
  
  def getCount(self):
    return self.count

class StandNames:

  def __init__(self):
    self.stands = []
    self.standQuantity = {}
    self.standRevenue = {}
    self.count = 0 
    
  def getStandQuantity(self, key):
    return self.standQuantity[key]
    
  def getStandRevenue(self, key):
    return self.standRevenue[key] 
    
  def getCount(self):
    return self.count
    
  def addStand(self, newName):
    self.stands.append(newName)
    self.count += 1
  
  def updateQuant(self, stand, quant):
    if self.standQuantity[stand]:
      self.standQuantity[stand] += quant
      
  def updateRev(self, stand, rev):
    if self.standRevenue[stand]:
      self.standRevenue[stand] += rev 
    
  def addStandQuant(self, newKey, newValue):
    self.standQuantity[newKey] = newValue
    
  def addStandRev(self, newKey, newValue):
    self.standRevenue[newKey] = newValue
     
class TotalTime:
 
  def __init__(self):
    self.begin = ""
    self.end = ""
    self.total = 0
    
  def getTotalTime(self):
    return self.total
    
  def addTimeBegin(self, newTime):
    self.begin = newTime 
    
  def addTimeEnd(self, newTime):
    self.end = newTime 
    
  def calcTotal(self):
    self.total = float(self.end) - float(self.begin)
    