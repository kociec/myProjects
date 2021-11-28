import pyautogui as pag

ex = (612,1065)    # współrzędne excela na pasku
pr = (514,1061)    # współrzędne przeglądarki na pasku

kw1 = (59,218)     # współrzędne komórki z kw_1 w excel
kw2 = (116,218)    # współrzędne komórki z kw_2 w excel
kw3 = (178,218)    # współrzędne komórki z kw_3 w excel

kw_1 = (831,470)   # współrzędne komórki z kw_1 w EUKW
kw_2 = (936,470)   # współrzędne komórki z kw_2 w EUKW
kw_3 = (1030,470)  # współrzędne komórki z kw_3 w EUKW


# przeklejenie początkowego numeru księgi npag. "KR1M"
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(kw1[0],kw1[1])
pag.click()
pag.hotkey('ctrl','c')
pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(kw_1[0],kw_1[1])
pag.click()
pag.hotkey('ctrl','v')

# przeklejenie numeru księgi npag. "00012345"
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(kw2[0],kw2[1])
pag.click()
pag.hotkey('ctrl','c')
pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(kw_2[0],kw_2[1])
pag.click()
pag.hotkey('ctrl','v')

# przeklejenie cyfry kontrolnej npag. "6"
pag.moveTo(ex[0],ex[1])
pag.click()
pag.moveTo(kw3[0],kw3[1])
pag.click()
pag.hotkey('ctrl','c')
pag.moveTo(pr[0],pr[1])
pag.click()
pag.moveTo(kw_3[0],kw_3[1])
pag.click()
pag.hotkey('ctrl','v')

pag.moveTo(833,550)
pag.click()
pag.moveTo(1339,687)

