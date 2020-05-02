import stockquotes
american = stockquotes.Stock('AAL')
americanPrice = american.current_price
print(americanPrice)