import pandas as pd
import sqlite3

def dataFetch(url, skip):
    data = pd.read_csv(url, skiprows=skip)   
    return pd.DataFrame(data)

def columnSelector(data, selection):
    return data[selection]

def dropNull(data):
    return data.dropna(how = "any", axis = 0) 

def yearSelector(data, f, t):
    return data[(data["Year"] >= f) & (data["Year"] <= t)]

def dataMerge(t1, t2, key, t1S, t2S):
    return pd.merge(t1, t2, how ='left', on = key, suffixes=(t1S, t2S))

def tempAverage(data):
    subset = data[["Jan",   "Feb",   "Mar",   "Apr",   "May",   "Jun",   "Jul",   "Aug",   "Sep",   "Oct",   "Nov",   "Dec"]]
    subset = subset.apply(pd.to_numeric)
    data["Average"] = subset.mean(axis = 1, skipna = True)
    return data

def save(data, path, file, table):
    try:
        conn = sqlite3.connect(path+file)
        data.to_sql(table, conn, if_exists='replace', index=False)
        conn.close()
    
    except:
        conn = sqlite3.connect("../data/"+file)
        data.to_sql(table, conn, if_exists='replace', index=False)
        conn.close()


def main():
    url1 = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    data1 = dataFetch(url1, [0])
    data1Header = [ "Year",   "Jan",   "Feb",   "Mar",   "Apr",   "May",   "Jun",   "Jul",   "Aug",   "Sep",   "Oct",   "Nov",   "Dec",]
    data1 = columnSelector(data1, data1Header)
    data1 = dropNull(data1)
    data1 = yearSelector(data1, 1995, 2010)
    data1 = tempAverage(data1)

    url2 = "https://www.epa.gov/system/files/other-files/2022-07/sea-level_fig-1.csv"
    data2 = dataFetch(url2, [0,1,2,3,4,5])
    data2 = columnSelector(data2, ["Year", "CSIRO - Adjusted sea level (inches)", "NOAA - Adjusted sea level (inches)"])
    data2 = dropNull(data2)
    data2 = yearSelector(data2, 1995, 2010)

    finalData = dropNull(dataMerge(data1, data2, ["Year"], "T", "S"))

    targetedPath = "./data/" 
    fileName = "Data.sqlite"
    dbName = "TempSeaLevel"
    save(finalData, targetedPath, fileName, dbName)

if __name__ == "__main__":
    main()