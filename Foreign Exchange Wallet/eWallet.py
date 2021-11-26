import requests                                               # import modules     

startValues, currentValues, line_length = [], [], 125         # declaring  variables for the summary and future prints

def Wallet(currency, quantity, entryPrice):                                                 # creating a function
   
    global date, time                                                                       # define global values
    
    data = requests.get('https://stooq.pl/q/l/?s=' + currency + 'pln&f=sd2t2ohlc&h&e=csv')  # web scraping from stooq.pl
    data = data.text.split(',')
    
    date, time, rateOfExchange = data[7], data[8], float(data[12])                          # data unpacking

    startValue, currentValue = quantity * entryPrice, quantity * rateOfExchange             # calculating...
    nominalChange, percentChange = currentValue - startValue, (currentValue / startValue) - 1 
    
    currency = currency.upper()                                                             # formating text 
    
    startValues.append(startValue)                                                          # collecting data to lists
    currentValues.append(currentValue)
    
    # print results for single currency using format pattern
    pattern = "{0:^12s}|{1:^15.2f}|{2:^15.2f}|{3:^19.3f}|{4:^19.2f}|{5:^+19.2f}|{6:^+19.2%}|"
    print(pattern.format(currency, quantity, startValue, rateOfExchange, currentValue, nominalChange, percentChange))
    print(line_length * '-')
    
                                                                            # print the header of table
print(line_length * '=')
print('CURRENCY\t|\tQUANTITY\t|\tBUY VALUE\t|\tEXCHANGE NOW\t|\tCURRENT VALUE\t|\tNOMINAL CHANGE\t|\tPERCENT CHANGE\t|')    
print(line_length * '=') 

Wallet('usd', 500 ,3.9)                                                     # Calling the function for each owned currency
Wallet('gbp', 300, 4.75)
Wallet('eur', 255.55, 4.8)
Wallet('cad', 115, 3.8)

sumBuy, sumNow = sum(startValues), sum(currentValues)                       # calculating summary results
totalChange = sumNow - sumBuy
percentTotalChange = (sumNow / sumBuy) - 1
                                                                            # print summary results for all currencies
pattern = "{0:^12s}|{1:^15.2s}|{2:^15.2f}|{3:^19.3s}|{4:^19.2f}|{5:^+19.2f}|{6:^+19.2%}|"
print(pattern.format('SUMMARY','', sumBuy, '', sumNow, totalChange , percentTotalChange))
print(line_length * '=')

print('\t' * 20,'ACCOUNT BALLANCE AT: ', date, time,' |')                   # print of last update date
print(line_length * '=')