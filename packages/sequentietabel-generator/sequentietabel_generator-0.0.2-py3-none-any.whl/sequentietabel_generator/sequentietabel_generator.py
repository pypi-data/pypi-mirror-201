import pandas as pd
import os

# Function to read CSV file and generate sequence table
def generate_table():
    # Open CSV file
    csv_file_pathGekozen = False
    while csv_file_pathGekozen == False:
        csv_file_pathType = (input('Excel (xlxs) of CSV (csv) bestand? (xlxs/csv): ')).lower()
        if(csv_file_pathType == "excel" or csv_file_pathType == "xlxs"):
            csv_file_path = input('Naam van het bestaande bestand (Excel-bestand, zonder .xlxs): ') + '.xlsx'
        elif(csv_file_pathType == "csv"):
            csv_file_path = input('Naam van het bestaande bestand (csv-bestand, zonder .csv): ') + '.csv'
        if(os.path.isfile(csv_file_path)):
            break
        else:
            print("bestand bestaat niet, probeer het opnieuw.")
    
    
    headerPrompt = (input('Heeft het bestand headers? (J(a), N(ee)): ')).lower()
    if(headerPrompt == "ja" or headerPrompt == "j" or headerPrompt == "y" or headerPrompt == "yes"):
        headers = True
    else:
        headers = False

    if(csv_file_pathType == "csv"):
        if(headers):
            df = pd.read_csv(csv_file_path)
            first_column = df.columns[0]
            df = df.drop([first_column], axis=1)
        else:
            df = pd.read_csv(csv_file_path, header=None)
    else:
        if(headers):
            df = pd.read_excel(csv_file_path)
            first_column = df.columns[0]
            df = df.drop([first_column], axis=1)
        else:
            df = pd.read_excel(csv_file_path, header=None)
    
    df = df.to_numpy()

    elements = []
    for row in df:
        for i in row:
            i = (i.lower()).strip()
            try:
                elements.index(i)
            except ValueError:
                elements.append(i)

    gedrag = []
    tabel = []

    for i in range(0,len(elements)):
        gedrag.append(elements[i])

    for i in range(0,len(elements)):
        tabel.append([])
        for j in range(0,len(elements)):
            if(j == i):
                tabel[i].append('-')
            else:
                tabel[i].append(0)

    for row in tabel:
        for colum in row:
            if tabel.index(row) == row.index(colum):
                colum = '-'
        
    currentElement = ''
    lastElement = ''
    
    for row in df:
        for i in row:
            currentElement = (i.lower()).strip()
            if(lastElement != currentElement and lastElement != ''):
                tabel[elements.index(lastElement)][elements.index(currentElement)] = tabel[elements.index(lastElement)][elements.index(currentElement)] + 1
            lastElement = currentElement

    path = input("Naam nieuwe bestand: ") + '.csv'
    
    csv = pd.DataFrame(tabel, index=gedrag, columns=gedrag)
    
    csv.to_csv(path)
    
    print("Sequentietabel gegenereerd!")