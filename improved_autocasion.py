from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

class AUTOCASION:
    
    def __init__(self):
        page = 1
        #Preguntar cuantas paginas se quiere scrapear
        num_of_pages = input("Cuantas páginas quieres scrapear?")
        num_of_pages = int(num_of_pages)
        global cars_info
        cars_info = {}
        while page <= num_of_pages:
            url = f"https://www.autocasion.com/coches-ocasion?page={page}"
            self.scrap_page(url)
            page += 1
            print(len(cars_info))
            
        self.dict_to_exccel()
    
    
        
    def scrap_page(self, url):
        headers = {"Accept-Language": "es-ES,es;q=0.9", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
        r = requests.get(url = url, headers=headers)
        global s
        s = bs(r.text, "html.parser")
        
        # Trobar els anuncis per pagina
        anuncios = s.find_all("article", class_= "anuncio")
        
        
        for num_coche, anuncio in enumerate(anuncios):
            fuel = None
            año = None
            cv = None
            km = None
            provincia = None
            
            #Descripció
            desc = anuncio.find("h2", itemprop="name").text.strip()
            
            #Precio
            price = anuncio.find("p", class_="precio")
            price = price.text.strip()
            price = price.split("\n")[0].replace(".","")
            price = int(price.replace(" €", ""))
            
            #Otros datos
            otros = anuncio.find("ul").find_all("li")
            for index, info in enumerate(otros):
                
                #Si està en la llista de combustible és el combustible
                if info.text in ["Gasolina", "Diésel", "Gas", "Eléctrico", "Híbrido", "Híbrido Enchufable"]:
                    fuel = info.text
                    
                else:
                    #Si es pot convertir a número és l'any
                    try:
                        int(info.text)
                        año = int(info.text)
                    except:
                        
                        try:
                            info.text.split(" ")
                            #Si la segona paraula és km és el kmetratge
                            if info.text.split(" ")[-1] == "km":
                                km = int(info.text.split(" ")[0].replace(".",""))

                            #Si la segona paraula és cv són els cavalls
                            elif info.text.split(" ")[-1] == "cv":
                                cv = int(info.text.split(" ")[0].replace(".",""))
                                
                        except:
                            provincia = info.text.strip()

                    provincia = info.text
                    
            cars_info[desc] = [price, fuel, año, km, cv, provincia]

    def dict_to_exccel(self):
        df = pd.DataFrame.from_dict(cars_info)
        df = df.transpose()
        df = df.reset_index()
        df.columns = ["Descripción", "Precio", "Combustible", "Año", "Km", "Cv", "Provincia"]
        df.to_excel("autocasion_millorat.xlsx")
        
        
if __name__ == "__main__":
    bot = AUTOCASION()