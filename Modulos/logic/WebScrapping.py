from playwright.sync_api import sync_playwright
from Modulos.Err.ErrorScrapping import anotExceptionRaisenScrapp as anotExRaiScrap
import polars as pl
from typing import List,Dict
from Modulos.Func.valCalCont import calCont

class WebScrapping:
    def __init__(self, urlWeb, rechParam, cant:int):
        self.__confUrl = [
            'https://listado.mercadolibre.com.co/'
            'https://www.amazon.com/s?k=xbox'
        ]
        self.__cantDif = cant
        self.__urlWeb = urlWeb
        self.__rechParam = rechParam
        self.__data = []
        self.__df: object
        
        self.processScrapping(self.__rechParam)
        return
    @anotExRaiScrap
    def processScrapping(self, rechParam):
        if rechParam != '':
            self.lo_playwright = sync_playwright().start()
            self.lo_browser = self.lo_playwright.chromium.launch(headless=False)
            self.lo_page = self.lo_browser.new_page()
            lv_query = f'{rechParam}?sb=all_mercadolibre#D[A:{rechParam}]'
            url = f'{self.__urlWeb}{ lv_query }'
            self.lo_page.goto(url)
            self.valScrap()
        else:
            raise Exception('No se especifico parametro de busqueda')
        return
    
    @anotExRaiScrap
    def valScrap(self):
        lv_cont = 0
        self.lo_page.wait_for_selector('[aria-label="Paginación"]')
        lti_pagCant = self.lo_page.query_selector_all('li.andes-pagination__button')
        lv_rangPag  = calCont(lti_pagCant)

        print(f'cantidad paginación{len(lti_pagCant)}')

        lv_cantDif = self.__cantDif - 1 if self.__cantDif != 0 and self.__cantDif > 0 else lv_rangPag
        while lv_cont <= lv_rangPag and lv_cont <= lv_cantDif:
            self.lo_page.wait_for_selector('[aria-label="Paginación"]')
            self.lo_page.click('li.andes-pagination__button.andes-pagination__button--next')
            self.lo_page.wait_for_selector('li.ui-search-layout__item')
            lti_data = self.lo_page.query_selector_all('li.ui-search-layout__item')
            lti_tabFilt = self.lectData(lti_data)
            self.__data = self.__data + lti_tabFilt
            if lv_cont % 10 == 0 and lv_cont == 10:
                self.lo_page.wait_for_selector('[aria-label="Paginación"]')
                lti_pagCant = self.lo_page.query_selector_all('li.andes-pagination__button')
                lo_pagFinal = lti_pagCant[-2].evaluate("node => node.textContent")
                lv_rangPag = int(lo_pagFinal) - 2
            lv_cont += 1
        self.closeProces()
        df = pl.DataFrame(self.__data,
                          schema=['titulo','rating','price','link'],
                          orient='row')
        
        self.__df = df
        return
    
    def lectData(self, data:List[object]):
        lti_data = []
        for item in data:
            lo_nodeTitle = item.query_selector(".poly-component__title-wrapper")
            lv_title = self.valNoneNode(lo_nodeTitle)
            lo_nodeRant = item.query_selector(".poly-component__review-compacted")
            lv_rating = self.valNoneNode(lo_nodeRant)
            lo_nodePrice = item.query_selector(".andes-money-amount__fraction")
            lv_price = self.valNoneNode(lo_nodePrice)
            lo_nodeLink = item.query_selector(".poly-component__title")
            lv_link = lo_nodeLink.evaluate("node => node.getAttribute('href')") if lo_nodeLink else 'N/A'
            lti_data.append((lv_title, lv_rating, lv_price, lv_link))

        return lti_data
    def valNoneNode(self, object: object):
        if object:
            lv_valNode = object.evaluate("node => node.textContent")
        else:
            lv_valNode = f'N/A'
        return lv_valNode
    def closeProces(self):
        self.lo_browser.close()
        self.lo_playwright.stop()
        return
    def getDf(self):
        return self.__df

    
