
from calendar import month
import csv
import json
import requests
from distutils.dep_util import newer
import os
from datetime import datetime
from pickle import FALSE
from stringprep import in_table_a1
from time import time
import codecs
import sys, ctypes as ct

dictCurrency = {'NGN':0,'EUR':0,'INR':0,'SEK':0,'BRL':0,'PHP':0,'GBP':0,'SGD':0,'AUD':0,'AD':0,'NZD':0,'MXN':0}

def getExperienceLevel(str1,str2):
    toret = ""

    str1 = str1.lower()
    str2 = str2.lower()

    if ("senior" in str1) | ("senior" in str2):
        toret = "SE"
    elif ("entry-level" in str1) | ("entry level" in str1) | ("entry-level" in str2) | ("entry level" in str2):
        toret = "EN"
    elif ("mid-level" in str1) | ("mid level" in str1) | ("junior" in str1) | ("mid-level" in str2) | ("mid level" in str2) | ("junior" in str2):
        toret = "MI"
    elif ("expert " in str1) | ("expert " in str2):
        toret = "EX"

    
    if toret == "":
        if "1 year experience" in str2:
            toret =  'EN'
        if "2 years experience" in str2:
            toret =  'EN'
        if "3 years experience" in str2:
            toret =  'MI'
        if "5 years experience" in str2:
            toret =  'SE'
        if "more than 10 years experience" in str2:
            toret =  'EX'
        if "+ 10 years experience" in str2:
            toret =  'EX'

    return toret

#convert currency to ISO encoding
def getCurrencyISO(salary):

    toret = ""

    if ("£" in salary) | ("GBP" in salary.upper()):
        toret = "GBP"
    elif  "SGD" in salary.upper():
        toret = "SGD"
    elif  ("₦" in salary) | ("NGN" in salary.upper()):
        toret = "NGN"
    elif  ("€" in salary) | ("EUR" in salary.upper()):
        toret = "EUR"
    elif  ("₹" in salary) | ("INR" in salary.upper()):
        toret = "INR"
    elif  ("kr" in salary) | ("SEK" in salary.upper()):
        toret = "SEK"
    elif  ("R$" in salary) | ("BRL" in salary.upper()):
        toret = "BRL"
    elif  ("₱" in salary) | ("PHP" in salary.upper()):
        toret = "PHP"
    elif ("A$" in salary) | ("AUD" in salary.upper()):
        toret = "AUD"
    elif ("CA$" in salary) | ("CAD" in salary.upper()):
        toret = "CAD"
    elif ("NZ$" in salary) | ("NZD" in salary.upper()):
        toret = "NZD"
    elif ("MX$" in salary) | ("MXN" in salary.upper()):
        toret = "MXN"
    elif ("$" in salary) | ("USD" in salary.upper()):
        toret = "USD"

    return toret

#convert salary to USD
def getSalaryUSD(salary,currency):

    salary_usd = salary

    if currency != "USD":
        c = dictCurrency[currency]
        salary_usd = salary_usd * c


    return round(salary_usd)




#connection with api (API COIN)
def getCoinApi():

    list = {"NGN","EUR","INR","SEK","BRL","PHP","GBP","SGD","AUD","CAD","NZD","MXN"}
    for c in list:

        url = f'https://rest.coinapi.io/v1/exchangerate/{c}/USD'
        #headers = {'X-CoinAPI-Key' : 'F01970E9-69D0-406C-8F09-B3C29AC12CFE'} #aacuquejo
        headers = {'X-CoinAPI-Key' : 'BC46E15B-3051-4CBA-98E0-A41BBB8D1862'}
        response = requests.get(url, headers=headers)
        dict = json.loads(response.text)


        print(f"Response {c}: {dict['rate']}")
        dictCurrency[c] = dict['rate']



def getAverege(salary1,salary2):

    
    salary1 = ''.join(char for char in salary1 if char.isdigit())
   
    avg = int(salary1)

    if salary2 != 0:
        salary2 = ''.join(char for char in salary2 if char.isdigit())
       
        if int(salary1) != 0 and int(salary2) != 0 :
            avg = (int(salary1) + int(salary2)) / 2
            avg = round(avg)

    return avg    

def getCompanySize(number):

    if number == "1 to 50 Employees":
        return 'S'
    if number == "51 to 200 Employees":
        return 'M'
    if number == "NaN":
        return "nan"
    if number == "Unknown":
        return "nan"
    else:
        return 'L'

    
#extract annual salary
def salaryYear(salary):
    
    salary_usd = salary.strip().lower()

    salary_split = salary.strip().split(" ")
    #year = False
    month = False
    other = False
    month_list = {"month","mois","mes","bulan","månad","บาทต่อเดือน","mês","měsíčně","Monat","Ayda","maand"}
    #year_list= {"year","año","Jahr","jaar","jahr"," ano " ," an"}
    other_list= {"week","hour","heure","hora","per uur","stunde"}

    for m in month_list:
        if m in salary_usd:
            month = True
    
    
    if month == False:
        for o in other_list:
            if o in salary_usd:
                other = True

    
    if other == False:

        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        
        for s in salary_split:
            if any(map(str.isdigit, s)) and d1 == 0:
                d1 = s
            elif any(map(str.isdigit, s)) and d1 != 0:
                d2 = s
            elif any(map(str.isdigit, s)) and d2 != 0:
                d3 = s
            elif any(map(str.isdigit, s)) and d3 != 0:
                d4 = s

        
        if d3 != 0 and d4 != 0:
            d1 = str(d1) + str(d2) 
            d2 = str(d3) + str(d4) 

        avg = getAverege(d1,d2)

        if month:
            avg *= 12 
        
       
        salary_usd =  avg
    else:
        salary_usd = 0
    


    return salary_usd



def getEmployementType(emp_type, emp_type2):

    newType = ""

    if ("full time" in emp_type.lower()) | ("full-time" in emp_type.lower()) | ("temps plein" in emp_type.lower()) | ("cu normă întreagă" in emp_type.lower()) | ("fuldtid" in emp_type.lower()) | ("heltid" in emp_type.lower()) | ("jornada completa" in emp_type.lower()) | ("tiempo completo" in emp_type.lower()) | ("vollzeit" in emp_type.lower()) | ("tempo pieno" in emp_type.lower()) | ("Tam zamanl" in emp_type.lower()) | ("plný úvazek" in emp_type.lower()) | ("período integral" in emp_type.lower()) | ("full time" in emp_type2.lower()) | ("full-time" in emp_type2.lower()) | ("temps plein" in emp_type2.lower()) | ("cu normă întreagă" in emp_type2.lower()) | ("fuldtid" in emp_type2.lower()) | ("heltid" in emp_type2.lower()) | ("jornada completa" in emp_type2.lower()) | ("tiempo completo" in emp_type2.lower()) | ("vollzeit" in emp_type2.lower()) | ("tempo pieno" in emp_type2.lower()) | ("Tam zamanl" in emp_type2.lower()) | ("plný úvazek" in emp_type2.lower()) | ("período integral" in emp_type2.lower()):
        newType= "FT"
        
    elif ("part time" in emp_type.lower()) | ("part-time" in emp_type.lower()) | ("deeltijds" in emp_type.lower()) | ("deltid" in emp_type.lower()) | ("teilzeit" in emp_type.lower()) | ("media jornada" in emp_type.lower()) | ("part time" in emp_type2.lower()) | ("part-time" in emp_type2.lower()) | ("deeltijds" in emp_type2.lower()) | ("deltid" in emp_type2.lower()) | ("teilzeit" in emp_type2.lower()) | ("media jornada" in emp_type2.lower()):
        newType= "PT"
    elif ("contract" in emp_type.lower()) | ("contract" in emp_type2.lower()):
        newType= "CT"
    else:
        newType = "FT"


    return newType

def getRemoteRatio(text1, text2):

    ratio = "0"

    if ("remote" in text1.lower()) | ("remoto" in text1.lower()) | ("remote" in text2.lower()) | ("remoto" in text2.lower()):
        ratio = "100"

    return ratio

#categorize offers
def job(title):
    title = title.lower()
    devOps_list = {"devops","azure","aws","cloud","devops","dev-ops","ops","systems","system"}
    mobileDeveloper_list = {"mobile","android","ios","app","react native","flutter"}
    cyberSecurity_list = {"cyber","security"}
    dataScientist_list = {"consultant","manager", "product manager","bi developer","power bi","tableau","visualization","kafka","salesforce","algorithms & optimization","algorithms","optimization","nlp","scientist","audit","ai & automation","analytics","oracle","qa","business","analyst","data","ml","learning"," ai ","intelligence","artificial","big","dig data"}
    webDeveloper_list = {"developer","reactjs","php","symfony","python","java","web","full stack","full-stack","front end","frontend","back end","backend","front-end","back-end","ui","ux","ui-ux","ui ux",".net","angular","programmer","node","nodejs","node.js","c#","aem","vuejs","vue"}

    job= ""

    for dev in devOps_list:
        if  dev in title:
            return "DevOps"
    for mob in mobileDeveloper_list:
        if  mob in title:
            return "Mobile Developer"
            
    for cyb in cyberSecurity_list:
        if  cyb in title:
            return "Cyber Security"
       
    for ds in dataScientist_list:
        if  ds in title:
            return "Data Scientist"
       
    for wd in webDeveloper_list:
        if  wd in title:
            return "Web Developer"
          
    return job

def main():

    types_of_encoding = ["utf8", "cp1252"]
    dirnames = os.listdir('./')
    contFiles = 0
    contRowsFiles= 0
    now = datetime.now() 
    file = "merge_glassdoor_" + now.strftime("%d%m%Y%H%M%S") + ".csv"

  

    with open("./merge/" + file, "w", newline="", encoding="utf8") as new_file:
        writer = csv.writer(new_file)
        getCoinApi()
        writer.writerow(["work_year", "experience_level", "employment_type","job", "job_title", "salary", "salary_currency", "salary_in_usd", "employee_residence", "remote_ratio", "company_location","company_size","job_summary"])
        
        for dir in dirnames:
            
            if "merge" not in dir:
                filenames =  os.listdir("./" + dir + "/")
                for name in filenames:
                    
                    csv.field_size_limit(int(ct.c_ulong(-1).value // 2))

                    country = name.split("_")
                    name_country= country[len(country)-1].replace(".csv","")
                    contRows = 0
                    if name.endswith('.csv'):
                        contFiles += 1
                        print(f"fichero: {name} ")
                        with open("./" + dir + "/" + name, "r", encoding="utf8") as f:
                            
                            reader = csv.reader(f, delimiter=",")

                            next(reader, None) #without header

                            for row in reader:
                                try:
                                    
                                    contRows +=1
                                    contRowsFiles +=1

                                    description = row[4].replace("\n"," ")

                                    exp_lvl = getExperienceLevel(description,row[2].strip())
                                    emp_type = getEmployementType(description,row[2].strip())
                                    salary = salaryYear(row[5].strip())
                                    currency = getCurrencyISO(row[5].strip())
                                    salaryUSD = salary
                                    
                                    if salary != 0:
                                        salaryUSD = getSalaryUSD(salary,currency)
                                    
                                    company_size = getCompanySize(row[8].strip())
                                    remote_ratio = getRemoteRatio(description,row[2].strip())
                                    jobs = job(row[2].strip())
                                    if salary != "" and salary != 0:
                                        newRoW = ["2022",exp_lvl,emp_type,jobs,row[2].strip(),int(salary),currency,int(salaryUSD),name_country.strip().replace(".csv",""),remote_ratio,name_country.strip().replace(".csv",""),company_size,description]

                                        writer.writerow(newRoW)

                                    print(f"Rows: {contRows}******************************************************")
                                    print(f"Rows_summary: {contRowsFiles}******************************************************")

                                except Exception as e:
                                    print(f"ERROR: {e}")
    return contFiles

if __name__ == '__main__':
    print("START")
    files = main()
    print(f"END n_files: {files} ")



