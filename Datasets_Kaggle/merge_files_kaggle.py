
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

code_country = {'AE':"United Arab Emirates",'AF':"Afghanistan",'AR':"Argentina",'AS':"American Samoa",'AT':"Austria",'AU':"Australia",'AZ':"Azerbaijan",'BE':"Belgium",'BG':"Bulgaria",'BR':"Brazil",'BW':"Botswana",'CA':"Canada",'CH':"Switzerland",'CL':"Chile",'CN':"China",'CO':"Colombia",'CR':"Costa Rica",'CZ':"Czech Republic",'DE':"Germany",'DK':"Denmark",'DZ':"Argel",'EE':"Estonia",'EG':"Egypt",'ES':"Spain",'ET':"Ethiopia",'FR':"France",'GB':"United Kingdom",'GH':"Ghana",'GR':"Greece",'HN':"Honduras",'HR':"Croatia",'HU':"Hungary",'ID':"Indonesia",'IE':"Ireland",'IL':"Israel",'IN':"India",'IQ':"Iraq",'IR':"Iran",'IT':"Italy",'JP':"Japan",'KE':"Kenya",'KG':"Kyrgyzstan",'LT':"Lithuania",'LU':"Luxembourg",'MD':"Moldova",'MT':"Malta",'MX':"Mexico",'MY':"Malaysia",'NG':"Nigeria",'NL':"Netherlands",'NO':"Norway",'NZ':"New Zealand",'PK':"Pakistan",'PL':"Poland",'PT':"Portugal",'RO':"Romania",'RU':"Russia",'SA':"Saudi Arabia",'SE':"Sweden",'SG':"Singapore",'SI':"Slovenia",'TR':"Turkey",'TW':"Taiwan",'UA':"Ukraine",'US':"United States",'VN':"Vietnam",'ZA':"South Africa"}

def getCountry(name):

    country = ""

    if name in code_country:
        country = code_country[name]

    return country

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
    filenames = os.listdir('./')
    contFiles = 0
    contRowsFiles= 0
    now = datetime.now() 
    file = "merge_kaggle_" + now.strftime("%d%m%Y%H%M%S") + ".csv"

    print("eeeeeeeeeeeeeeean")

    with open("./merge/" + file, "w", newline="", encoding="utf8") as new_file:
        writer = csv.writer(new_file)
        
        writer.writerow(["work_year", "experience_level", "employment_type","job", "job_title", "salary", "salary_currency", "salary_in_usd", "employee_residence", "remote_ratio", "company_location","company_size","job_summary"])
        print("222222222222222222222222222222 ")
        for name in filenames:
            
            if "merge" not in name:
                
                csv.field_size_limit(int(ct.c_ulong(-1).value // 2))

                contRows = 0
                if name.endswith('.csv'):
                    contFiles += 1
                    print(f"fichero: {name} ")
                    with open("./" + name, "r", encoding="utf8") as f:
                        
                        reader = csv.reader(f, delimiter=",")

                        next(reader, None) #without header

                        for row in reader:
                            try:
                                
                                contRows +=1
                                contRowsFiles +=1
                                

                                if name == "Data_Science_Salaries.csv":
                                    jobs = job(row[4].strip())
                                    name_country = getCountry(row[8].strip())
                                    newRoW = [row[1].strip().replace("e",""),row[2].strip(),row[3].strip(),jobs,row[4].strip(),int(row[5].strip()),row[6].strip(),int(row[7].strip()),name_country,row[9].strip(),name_country,row[11].strip(),""]
                                else:
                                    jobs = job(row[3].strip())
                                    name_country = getCountry(row[7].strip())
                                    newRoW = [row[0].strip().replace("e",""),row[1].strip(),row[2].strip(),jobs,row[3].strip(),int(row[4].strip()),row[5].strip(),int(row[6].strip()),name_country,row[8].strip(),name_country,row[10].strip(),""]
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



