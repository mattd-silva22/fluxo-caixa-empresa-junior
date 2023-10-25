import sys
import os
import pandas as pd
from datetime import datetime


def getMonth(month):
    meses = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
    }

    return meses.get(month, 'null')

def openFile(filePath):
    return pd.read_csv(filePath)

def createEntry(row):
    return (row[1],row[4],"-","Cora",abs(row[5]),row[3],"-")

def calculateFluxo(df):
    income = []
    outcome = []

    incomeList = []
    outcomeList = []

    for row in df.itertuples():
        _,  mes, _ = map(int, row[1].split('/'))
        mesAtual = mes
        if row[3] == "CRÉDITO":
            income.append(row[5])
            incomeList.append(createEntry(row))
        elif row[3] == "DÉBITO":
            outcome.append(row[5])
            outcomeList.append(createEntry(row))

    
    totalOutcome = sum(outcome)
    totalIncome = sum(income)

    outcomeTable = pd.DataFrame(outcomeList,columns=["DATA","Destinatário","Descrição","Conta","Valor","Tipo","Comprovante"])
    incomeTable = pd.DataFrame(incomeList,columns=["DATA","Destinatário","Descrição","Conta","Valor","Tipo","Comprovante"])
    
    if not os.path.exists("relatorios"):
        os.mkdir("relatorios")
    REPORTMONTH = getMonth(mesAtual)
    
    outcomeTable.to_csv(f"./relatorios/{REPORTMONTH}_fluxo_saida.csv")
    incomeTable.to_csv(f"./relatorios/{REPORTMONTH}_fluxo_entrada.csv")

def main():
    if os.path.exists("extratos"):
        reports = os.listdir("extratos")
        for report in reports:
              df = openFile(f"./extratos/{report}")
              calculateFluxo(df)



main()