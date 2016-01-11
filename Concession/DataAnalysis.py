#This program will extract valuable insights from a file containing business transactions.
from Results import GroupNames, CategoryNames, StandNames, TotalTime
from operator import itemgetter

def extractData(newFile):
  catgroups = GroupNames()
  catnames = CategoryNames()
  stands = StandNames()
  time = TotalTime()

  numlines = 0
  
  thefile = open(newFile, "r")
  
  for line in thefile:
    words = line.strip().split(',')
    if numlines >= 1:
      if numlines == 1:
        getTime(time, words)
      groupData(catgroups, words) 
      categoryName(catnames, words) 
      standName(stands, words)        
      
    numlines += 1
    
  getTime(time, words) 
  categoryGroupTotal(catgroups)
  categoryNameTotal(catnames)
  standTotal(stands)
  nameStandTotal(catnames)
  sortCategoryNames(catnames)
  sortStandNames(stands)
  bestProductGroup(catnames)
  
  print numlines  
    
def groupData(Group, newLine):
  name = newLine[3] 
  quant = int(newLine[6])
  revenue = float(newLine[7].strip('$()'))
  
  if name not in Group.namesQuantity:
    Group.addNameQuant(name, quant) 
    Group.addNameRev(name, revenue)
  else: 
    newQuantity = Group.getNameQuantity(name) + quant
    Group.addNameQuant(name, newQuantity) 
    newRevenue = Group.getNameRevenue(name) + revenue 
    Group.addNameRev(name, newRevenue)
  Group.addTotalR(revenue)
  Group.addTotalQ(quant)
    
def categoryName(Group, newLine):
  gname = str(newLine[3])
  item = str(newLine[4])
  stand = str(newLine[5])
  quant = int(newLine[6])
  revenue = float(newLine[7].strip('$()')) 
  
  if item not in Group.catNameall:
    Group.addAll(item, gname, quant, revenue)
    Group.addNameStand(item, stand, quant, revenue)
    Group.addCount()
  else:
    Group.updateAll(item, gname, quant, revenue)
    Group.updateNameStand(item, stand, quant, revenue)
    
def sortCategoryNames(Group):
  topQ = sorted(Group.catNameall.items(), key=lambda quant: quant[1][1])
  top5 = sorted(Group.catNameall.items(), key=lambda rev: rev[1][2])
  
  print "\nTop 5 products purchased:"
 
  '''  
  print topQ[len(topQ)-5:]
  for i in topQ[len(topQ)-5:]:
    Group.fiveQ.append(i[0])
    print i[0], i[1][1] '''

  '''print top5[len(top5)-5:]
  for i in top5[len(top5)-5:]:
    print i[0] , i[1][2]
    Group.fiveR.append(i[0])'''
  
def sortStandNames(Group):
  topStand = sorted(Group.standQuantity.items(), key=lambda quant: quant[1])
  print "\nTop Stand names sorted by items purchased:"
  #print topStand[len(topStand)-5:]
  for key, value in topStand[len(topStand)-5:]:
    print key, value
  
  topStandRev = sorted(Group.standRevenue.items(), key=lambda revenue: revenue[1])
  print "\nTop Stand names sorted by revenue:"
  print topStandRev[len(topStandRev)-5:]
  #for key, value in topStandRev:
  #  print key, value 
  
def bestProductGroup(Group):
  topP = {}
  topName = {}
  topRev = {}
  topQ = sorted(Group.catNameall.items(), key=lambda quant: quant[1][1])
  for index in reversed(topQ): 
    if index[1][0] not in topP:
      topP[index[1][0]] = index[1][1] 
      topName[index[0]] = index[1][1]
      topRev[index[0]] = index[1][2]
  print "\nTop products per group:"
  print topName
  print topRev
  
def standName(Group, newLine):
  gname = str(newLine[3])
  cname = str(newLine[4])
  sname = str(newLine[5])
  quant = int(newLine[6])
  revenue = float(newLine[7].strip('$()'))
  
  if sname not in Group.stands:    
    Group.addStand(sname)
    Group.addStandQuant(sname, quant) 
    Group.addStandRev(sname, revenue) 
  else:
    Group.updateQuant(sname, quant)
    Group.updateRev(sname, revenue) 

def getTime(Time, newLine):
  tmp = newLine[0].split()
  newdate = tmp[0]
  newTime = tmp[1].split(':')
  hrs = newTime[0]
  mins = newTime[1]
  theTime = str(hrs) + "." + str(mins) 
  if Time.begin:
    if Time.begin > theTime:
      Time.addTimeBegin(theTime)
    else:
      Time.addTimeEnd(theTime) 
      Time.calcTotal()
  else:
    Time.addTimeBegin(theTime)
    
  print Time.begin, Time.end, Time.total
################################################# Display Functions
#Display in stats.txt file: total product sales, total revenue, each group's product sales and revenue.
def categoryGroupTotal(Group):
  newFile = open('stats.txt', 'w')
  rev = Group.getRev()
  quant = Group.getQuant()
  totalstr = "Total Revenue: $" + str(rev) + " Total Number of Products Sold: " + str(quant) + "\n\n"
  newFile.write(totalstr)
  newFile.write("Category Groups: Number of items purchased per group \n\n")
  for key, value in Group.namesQuantity.iteritems():
    tmpstr = "Group: " + key + " Quantity: " + str(value) + " \n"
    newFile.write(tmpstr)
  newFile.write("\nCategory Groups: Total revenue per group \n\n")
  for key, value in Group.namesRevenue.iteritems():
    tmpstr = "Group: " + key + " Revenue: " + str(value) + " \n"
    newFile.write(tmpstr)  
  newFile.close()
  
#Display/concatenate to stats.txt file: Category Names total, each category name and product sales (descending order),
# each category name and revenue (descending order).
def categoryNameTotal(Group):
  newFile = open('stats.txt', 'a')
  newFile.write("\n******************************************************\n")
  newFile.write("Category Names: Number of items purchased per product \n\n")
  num = Group.getCount()
  newFile.write("Total Number of Products: " + str(num) + "\n\n")
  topQ = sorted(Group.catNameall.items(), key=lambda quant: quant[1][1])
  topR = sorted(Group.catNameall.items(), key=lambda rev: rev[1][2])
  newFile.write("(Category Name: Quantity)\n")
  for i in reversed(topQ):
    tmpstr = i[0] + ": " + str(i[1][1]) + "\n" 
    newFile.write(tmpstr)
  newFile.write("\nCategory Names: Total revenue per product \n\n")
  newFile.write("(Category Name: Revenue)\n")
  for i in reversed(topR):
    tmpstr = i[0] + ": $" + str(i[1][2]) + "\n" 
    newFile.write(tmpstr)      
  newFile.close()

#Display/concatenate to stats.txt file: Total number of stands, top 25 stand name and number of purchases, top 25 stand names and revenue.
def standTotal(Group):
  newFile = open('stats.txt', 'a')
  newFile.write("\n******************************************************\n")
  topStand = sorted(Group.standQuantity.items(), key=lambda quant: quant[1])
  newFile.write("Stand Names: Top 25 sorted by items purchased:\n\n")
  num = Group.getCount()
  newFile.write("Total Number of Stands: " + str(num) + "\n\n")
  newFile.write("(Stand Name: Quantity)\n")
  for key, value in reversed(topStand[len(topStand)-25:]):
    tmpstr = key + ": " + str(value) + "\n"
    newFile.write(tmpstr)
  topStandRev = sorted(Group.standRevenue.items(), key=lambda revenue: revenue[1])
  newFile.write("\nStand Names: Top 25 sorted by revenue:\n\n")
  newFile.write("(Stand Name: Revenue)\n")
  for key, value in reversed(topStand[len(topStandRev)-25:]):
    tmpstr = key + ": $" + str(value) + "\n"
    newFile.write(tmpstr)  
  newFile.close()
  
def nameStandTotal(Group):
  newFile = open('stats.txt', 'a')
  newFile.write("\n******************************************************\n")  
  newFile.write("Category Names: Names per stand: \n")
  for key, value in Group.namesStand.items():
    tmpA = "\n\nName: " + key
    count = 0
    newFile.write(tmpA)
    for s, v in value.items():
      count += 1
      tmpB = "\nStand: " + s + " ="
      newFile.write(tmpB)
      for k, r in v.items():
        tmpC = " " + k + ":" + str(r)
        newFile.write(tmpC)
    newFile.write("\nCount = " + str(count))        
  newFile.close()
 
if __name__ == '__main__':
  extractData("concessions.csv") 
  
  