import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd



st.markdown(
    """
    <style>
    .title-wrapper {
        background-color: black;
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .title {
        color: white;
        margin: 0;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """<div class="title-wrapper"><h1 class="title">REVERSED DCF</h1></div>""",
    unsafe_allow_html=True
)
st.write("""
    Hi there! \n
    This page will help you calculate intrinsic PE of consistent compounders through growth-RoCE DCF model.\n
    We then compare this with current PE of the stock to calculate degree of overvaluation.
            """)

def stock(ticker):
    try:
        request1 = requests.get(f'https://www.screener.in/company/{ticker}/consolidated/')
        if request1.status_code==200:
            webpage1 = request1.text
            soup = BeautifulSoup(webpage1, 'lxml')
            ele = soup.find_all('div', class_ = 'company-ratios')
            ele2 = soup.find_all('table', class_='ranges-table')
            ele3 = soup.find_all('div', class_='responsive-holder fill-card-width')
            ele4 = soup.find_all('section', id ='ratios', class_='card card-large')
            for i in ele:
                stock_pe = i.find_all('span', class_='number')[4].text.strip()
                mak_cap = i.find_all('span', class_='number')[0].text.strip()

            result = []

            for j in ele2:
                data = j.find_all('td')
                for item in data:
                    item_dict = {}
                    for i in range(0, len(data), 2): 
                        key = data[i].text.replace('<td>', '').replace('</td>', '')  
                        value = data[i + 1].text.replace('<td>', '').replace('</td>', '') 
                        item_dict[key] = value
                    result.append(item_dict)

            value_to_extract = ele4[0].find_all('td', class_='')[67:]
            roce = []
            for i in value_to_extract:
                value = i.text.strip().rstrip('%')
                try:
                    if value:
                        roce.append(int(value))
                except ValueError:
                    pass

            df = pd.DataFrame(result)
            df = df.iloc[0:2, 0:4]
            df.index = ['Sales Growth', 'Profit Growth']
            net_profit = ele3[1].find_all('td', class_='')[129].text
            eps = ele3[1].find_all('td', class_='')[-14].text
            ope_pro = ele3[1].find_all('td', class_='')[38].text
            roce = sorted(roce)[2]
            return stock_pe, mak_cap, eps, net_profit, ope_pro, roce, df
    except Exception as e:
        print(f"Error fetching stock P/E from request1: {e}")
    
    try:
        request2 = requests.get(f'https://www.screener.in/company/{ticker}/')
        if request2.status_code==200:
            webpage2 =request2.text
            soup = BeautifulSoup(webpage2, 'lxml')
            ele = soup.find_all('div', class_ = 'company-ratios')
            ele2 = soup.find_all('table', class_='ranges-table')
            ele3 = soup.find_all('div', class_='responsive-holder fill-card-width')
            ele4 = soup.find_all('section', id ='ratios', class_='card card-large')
            for i in ele:
                stock_pe = i.find_all('span', class_='number')[4].text.strip()
                mak_cap = i.find_all('span', class_='number')[0].text.strip()
            result = []

            for j in ele2:
                data = j.find_all('td')  
                for item in data:
                    item_dict = {}
                    for i in range(0, len(data), 2):  
                        key = data[i].text.replace('<td>', '').replace('</td>', '')  
                        value = data[i + 1].text.replace('<td>', '').replace('</td>', '')  
                        item_dict[key] = value
                    result.append(item_dict)

            
            value_to_extract = ele4[0].find_all('td', class_='')[66:]
            roce = []
            for i in value_to_extract:
                value = i.text.strip().rstrip('%')
                try:
                    if value:
                        roce.append(int(value))
                except ValueError:
                    pass
            

            df = pd.DataFrame(result)
            df = df.iloc[0:2, 0:4]
            df.index = ['Sales Growth', 'Profit Growth']
            net_profit = ele3[1].find_all('td', class_='')[119].text
            eps = ele3[1].find_all('td', class_='')[-13].text
            ope_pro = ele3[1].find_all('td', class_='')[35].text
            roce = sorted(roce)[2]
            return stock_pe, mak_cap, net_profit, eps, ope_pro ,roce, df
    except Exception as e:
        print(f"Error fetching stock P/E from request2: {e}")
    
    
    default_value = 0
    return default_value, default_value, default_value, default_value, default_value, default_value, default_value




ticker_input = st.text_input('NSE/BSE symbol', value="NESTLEIND")
ticker_input = str(ticker_input)



cost_of_capital = st.slider('Cost of Capital (CoC): %', 8,16,step=1,value=12)
roce = st.slider('Return on Capital Employed (RoCE): %', 10,100,step=10, value = 20)
growth_rate =st.slider('Growth during high growth period: $', 8,20,step=2, value=12)
high_growth_years = st.slider('High growth period(years)', 10,26,step=2, value=15)
fade_years = st.slider('Fade period(years):', 5,20,step=5, value=15)
terminal_growth_rate = st.slider('Terminal growth rate: %', 0,8, step=1, value=5)



st.write(f'Stock Symbol: {ticker_input}')
stock_pe, mak_cap, net_profit, eps, ope_pro, roce, df = stock(ticker_input)
if mak_cap is not None:
    mak_cap = float(mak_cap.replace(',', ''))
else:
    mak_cap = 0.0
net_profit = float(net_profit.replace(',', ''))
eps = float(eps.replace(',',''))
ope_pro = int(ope_pro.replace(',',''))

st.write(f'Current PE: {stock_pe}')
st.write(f'FY23 PE: {round(mak_cap/net_profit, 1)}')
st.write(f'5-yr median pre-tax RoCE: {roce}%')
st.table(df)

st.bar_chart(df.iloc[0,:].transpose())
st.write('Sales Growth %') 

st.bar_chart(df.iloc[1,:].transpose())
st.write('Profit Growth %')

st.write('Play with inputs to see changes in intrinsic PE and overvaluation:')

def intrinsic_eps(cost_of_capital, ope_pro, growth_rate, high_growth_years, fade_years, terminal_growth_rate, eps):
    tax_rate = 0.25  # Constant tax rate assumed
    
    nopat = ope_pro*(1-tax_rate)
    year = high_growth_years + fade_years
    fcf = []
    linear_decay = ((growth_rate-terminal_growth_rate)/fade_years)
    linear_decay = round(linear_decay/100,2)
    growth_rate = round(growth_rate/100,2)
    cost_of_capital = round(cost_of_capital/100,2)
    for yr in range(1,year+1):
        if yr<=high_growth_years:
            fcf.append(nopat*(cost_of_capital - growth_rate)/(1+(cost_of_capital))**yr)
        else:
            growth_rate-=linear_decay
            if growth_rate<=terminal_growth_rate:
                fcf.append(nopat*(cost_of_capital - (growth_rate/100))/(1+cost_of_capital)**yr)
    fcf_sum = sum(fcf)
    intrinsic_pe = fcf_sum/eps
    return round(intrinsic_pe,2)



intrinsic_pe = intrinsic_eps(cost_of_capital, ope_pro, growth_rate, high_growth_years, fade_years, terminal_growth_rate, eps)

FY23PE = float(round(mak_cap/net_profit, 1))
over_valuation = 0
stock_pe = float(stock_pe)
if stock_pe < FY23PE:
    over_valuation = round(((stock_pe/intrinsic_pe) - 1)*100, 2)
else:
    over_valuation = round(((FY23PE/intrinsic_pe) -1)*100,2)

st.write(f'The calculated intrinsic PE is: {intrinsic_pe}')

st.write(f'Degree of overvaluation: {over_valuation}')
