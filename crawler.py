import requests
from bs4 import BeautifulSoup
import re
import csv

salesGrowthThreshold = float(15)
ROCCustomThreshold = float(10)
debtEquityThreshold = float(0.8)
PATMarginThreshold = float(6)
CFOThreshold = float(0.85)
ROEThreshold = float(15)
ROCEThreshold = float(15)
ProfitGrowthThreshold = float(6)
companyList = []
selectedCompanyName = []
selectedCompanyRating = []
with open('equity.csv','r') as data:
    csvr = csv.reader(data)
    fields = next(csvr)
    for row in csvr:
        companyList.append(row[0])

count = 0
ac = open("AllCompanies.txt", 'w')
for company in companyList:
    try:
        voting = 0
        ratios = {}
        url = 'https://ticker.finology.in/company/'+company+'?mode=C'
        print(url)
        res = requests.get(url)
        print(res.status_code)
        soup = BeautifulSoup(res.text, 'html.parser')
        CompanyEssentials = str(soup.find(id='mainContent_updAddRatios'))

        #search for market capitalisation
        i = re.compile(r'Market Cap')
        i = i.search(CompanyEssentials).start()
        while i<len(CompanyEssentials):
            if CompanyEssentials[i:i+6] == "Number":
                if i+50 < len(CompanyEssentials):
                    temp = CompanyEssentials[i:i+50]
                else:
                    temp = CompanyEssentials[i:]
                break
            else:
                i = i + 1
        getMarketCap = re.compile(r'[0-9]+\.[0-9]*')
        getMarketCap = getMarketCap.search(temp)
        ratios["Market Capitalisation"] = float(getMarketCap.group())

        #search for enterprise value
        i = re.compile(r'Enterprise Value')
        i = i.search(CompanyEssentials).start()
        while i<len(CompanyEssentials):
            if CompanyEssentials[i:i+6] == "Number":
                if i+50 < len(CompanyEssentials):
                    temp = CompanyEssentials[i:i+50]
                else:
                    temp = CompanyEssentials[i:]
                break
            else:
                i = i + 1
        getEnterpriseVal = re.compile(r'[0-9]+\.[0-9]*')
        getEnterpriseVal = getEnterpriseVal.search(temp)
        ratios["Enterprise Value"] = float(getEnterpriseVal.group())

        #search for sales growth
        i = re.compile(r'Sales Growth')
        i = i.search(CompanyEssentials).start()
        while i<len(CompanyEssentials):
            if CompanyEssentials[i:i+6] == "Number":
                if i+50 < len(CompanyEssentials):
                    temp = CompanyEssentials[i:i+50]
                else:
                    temp = CompanyEssentials[i:]
                break
            else:
                i = i + 1
        getSalesGrowth = re.compile(r'[0-9]+\.[0-9]*')
        getSalesGrowth = getSalesGrowth.search(temp)
        ratios["Sales Growth"] = float(getSalesGrowth.group())
        if ratios["Sales Growth"] > salesGrowthThreshold:
            voting = voting + 1

        #search for ROE
        i = re.compile(r'ROE')
        i = i.search(CompanyEssentials).start()
        while i<len(CompanyEssentials):
            if CompanyEssentials[i:i+6] == "Number":
                if i+50 < len(CompanyEssentials):
                    temp = CompanyEssentials[i:i+50]
                else:
                    temp = CompanyEssentials[i:]
                break
            else:
                i = i + 1
        getROE = re.compile(r'[0-9]+\.[0-9]*')
        getROE = getROE.search(temp)
        ratios["ROE"] = float(getROE.group())
        if ratios["ROE"] > ROEThreshold:
            voting = voting + 1

        #search for ROCE
        i = re.compile(r'ROCE')
        i = i.search(CompanyEssentials).start()
        while i<len(CompanyEssentials):
            if CompanyEssentials[i:i+6] == "Number":
                if i+50 < len(CompanyEssentials):
                    temp = CompanyEssentials[i:i+50]
                else:
                    temp = CompanyEssentials[i:]
                break
            else:
                i = i + 1
        getROCE = re.compile(r'[0-9]+\.[0-9]*')
        getROCE = getROCE.search(temp)
        ratios["ROCE"] = float(getROCE.group())
        if ratios["ROCE"] > ROCEThreshold:
            voting = voting + 1

        #calculating PAT Margin
        pnl = str(soup.find(id='profit'))
        i = re.compile(r'Consolidated Net Profit')
        i = i.search(pnl).start()
        netProfit = float(0)
        sales = float(0)
        while i<len(pnl):
            if pnl[i:i+6] == "Number":
                j = 0
                i = i + 6
                while j<4:
                    if pnl[i:i+6] == "Number":
                        i = i + 6
                        j = j + 1
                    else:
                        i = i + 1
                if i+50 < len(pnl):
                    temp = pnl[i:i+50]
                else:
                    temp = pnl[i:]
                break
            else:
                i = i+1
        t = re.compile(r'[0-9]+\.*[0-9]*')
        t = t.search(temp)
        netProfit = float(t.group())

        i = re.compile(r'Net Sales')
        i = i.search(pnl).start()
        while i<len(pnl):
            if pnl[i:i+6] == "Number":
                j = 0
                i = i + 6
                while j<4:
                    if pnl[i:i+6] == "Number":
                        i = i + 6
                        j = j + 1
                    else:
                        i = i + 1
                if i+50 < len(pnl):
                    temp = pnl[i:i+50]
                else:
                    temp = pnl[i:]
                break
            else:
                i = i+1
        t = re.compile(r'[0-9]+\.*[0-9]*')
        t = t.search(temp)
        sales = float(t.group())
        ratios["PAT Margin"] = float((netProfit/sales)*100)
        if ratios["PAT Margin"] > PATMarginThreshold:
            voting = voting + 1

        #Calculating custom ROC
        i = re.compile(r'Total Expenditure')
        i = i.search(pnl).start()
        expenditure = float(0)
        while i<len(pnl):
            if pnl[i:i+6] == "Number":
                j = 0
                i = i + 6
                while j<4:
                    if pnl[i:i+6] == "Number":
                        i = i + 6
                        j = j + 1
                    else:
                        i = i + 1
                if i+50 < len(pnl):
                    temp = pnl[i:i+50]
                else:
                    temp = pnl[i:]
                break
            else:
                i = i+1
        t = re.compile(r'[0-9]+\.*[0-9]*')
        t = t.search(temp)
        expenditure = float(t.group())
        ratios["ROC (Custom)"] = float((netProfit/expenditure)*100)
        if ratios["ROC (Custom)"] > ROCCustomThreshold:
            voting = voting + 1

        #getting debt/equity ratio
        der = str(soup.find(id='mainContent_divDebtEquity'))
        i = re.compile(r'Debt/Equity')
        i = i.search(der).start()
        while i<len(der):
            if der[i:i+6] == "Number":
                if i+50 < len(der):
                    temp = der[i:i+50]
                else:
                    temp = der[i:]
                break
            else:
                i = i + 1
        getDER = re.compile(r'[0-9]+\.[0-9]*')
        getDER = getDER.search(temp)
        ratios["Debt/Equity Ratio"] = float(getDER.group())
        if ratios["Debt/Equity Ratio"] < debtEquityThreshold:
            voting = voting + 1

        #getting CFO/PAT ratio
        cfo = str(soup.find(id='mainContent_divCFOPAT'))
        i = re.compile(r'CFO/PAT')
        i = i.search(cfo).start()
        while i<len(cfo):
            if cfo[i:i+6] == "Number":
                if i+50 < len(cfo):
                    temp = cfo[i:i+50]
                else:
                    temp = cfo[i:]
                break
            else:
                i = i + 1
        getCFO = re.compile(r'[0-9]+\.[0-9]*')
        getCFO = getCFO.search(temp)
        ratios["CFO/PAT Ratio"] = float(getCFO.group())
        if ratios["CFO/PAT Ratio"] > CFOThreshold:
            voting = voting + 1

        #search for profit growth
        i = re.compile(r'Profit Growth')
        i = i.search(CompanyEssentials).start()
        while i<len(CompanyEssentials):
            if CompanyEssentials[i:i+6] == "Number":
                if i+50 < len(CompanyEssentials):
                    temp = CompanyEssentials[i:i+50]
                else:
                    temp = CompanyEssentials[i:]
                break
            else:
                i = i + 1
        getProfitGrowth = re.compile(r'[0-9]+\.[0-9]*')
        getProfitGrowth = getProfitGrowth.search(temp)
        ratios["Profit Growth"] = float(getProfitGrowth.group())
        if ratios["Profit Growth"] > ProfitGrowthThreshold:
            voting = voting + 1
        
        print("Company: " + str(company) + " - Rating: " + str(voting))
        ac.write("Company: " + str(company) + " - Rating: " + str(voting) + "\n")
        
        if voting > 5:
            selectedCompanyName.append(company)
            selectedCompanyRating.append(voting)
            count = count + 1
    except Exception as e:
        print("Company missed: " + str(company))
        print("Reason: " + str(e))
        
print("Count: " + str(count))
f = open('list.txt','w')
for i in range(len(selectedCompanyName)):
    print("Company: " + selectedCompanyName[i] + " - Rating: " + str(selectedCompanyRating[i]))
    f.write("Company: " + selectedCompanyName[i] + " - Rating: " + str(selectedCompanyRating[i]) + "\n")
ac.close()
f.close()