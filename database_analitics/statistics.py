
import sys
sys.path.append('../')
import database.databaseCRUD as databaseCRUD
import database.months as months

databaseCRUD.db_connect("baza_res", "res", "localhost/xe")
cursor = databaseCRUD.connection.cursor()

# potrosnja po mesecima za odredjeni grad 

def potrosnjaGrad():
    print("Unesite grad za koji vas zanima potrosnja:")
    result = ""
    grad = input()
    query = f"""select mesec, potrosnja from brojilo inner join potrosnja
            on brojilo.idbrojila = potrosnja.idbrojila
            where grad='{grad}'
            order by mesec"""
    
    cursor.execute(query)

    for mesec, potrosnja in cursor:
       result += f"{mesec} : {potrosnja}|"

    result = result[:-1]

    grad = grad.split(' ')
    nazivFajla = ""
    for s in grad:
        nazivFajla += s
    
    nazivFajla = nazivFajla + ".txt"
    fajl = open(nazivFajla, "w")

    txtReportGrad(result, fajl)

def txtReportGrad(result, fajl):
    result = result.split('|')
    for r in result:
        mesec = int(r.split(':')[0])
        potrosnja = (r.split(':')[1])
        fajl.write(f"{months.Months(mesec).name} - {potrosnja}")
        fajl.write("\n")
    
    fajl.close()

# potrosnja po mesecima za odredjeno brojilo

def potrosnjaBrojila():
    print("Unesite id brojila za koje vas zanima potrosnja:")
    id = int(input())
    query = f"""select mesec, potrosnja from brojilo inner join potrosnja
            on brojilo.idbrojila = potrosnja.idbrojila
            where brojilo.idbrojila='{id}'
            order by mesec"""
    cursor.execute(query)
    result = ""
    for mesec, potrosnja in cursor:
        result += f"{mesec} : {potrosnja}|"

    result = result[:-1]

    nazivFajla = "brojilo" + str(id) + ".txt"

    fajl = open(nazivFajla, "w")
    txtReportBrojilo(result, fajl)


def txtReportBrojilo(result, fajl):
    result = result.split('|')
    for r in result:
        mesec = int(r.split(':')[0])
        potrosnja = (r.split(':')[1])
        fajl.write(f"{months.Months(mesec).name} - {potrosnja}")
        fajl.write("\n")

    fajl.close()