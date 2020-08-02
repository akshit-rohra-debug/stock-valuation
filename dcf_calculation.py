def calculateByDcf(fcf, rate1t5, rate6t10, discount, terminal, totalShares, netdebt, marginOfSafety):
    intrinsicValue = 0
    rate1t5 = rate1t5/100
    rate6t10 = rate6t10/100
    discount = discount/100
    terminal = terminal/100
    marginOfSafety = marginOfSafety/100
    fcfn = []
    fcfn.append(fcf)
    for i in range(1,6):
        fcfn.append(fcfn[i-1] * (1+rate1t5))
        
    for i in range(6,11):
        fcfn.append(fcfn[i-1] * (1+rate6t10))
        
    for i in range(1,11):
        pv = fcfn[i] / pow((1+discount), i)
        intrinsicValue = intrinsicValue + pv
    
    intrinsicValue = intrinsicValue - netdebt
    terminalValue = fcfn[10]
    terminalValue = terminalValue * (1+terminal)
    terminalValue = terminalValue / (discount - terminal)
    terminalValue = terminalValue / pow((1+discount),10)
    intrinsicValue = intrinsicValue + terminalValue
    valuePerShare = intrinsicValue / totalShares
    return valuePerShare, valuePerShare * (1 - marginOfSafety)

if __name__ == "__main__":
    #below values in percentage
    rate1t5 = 10
    rate6t10 = 10
    discount = 20
    terminal = 1
    marginOfSafety = 20
    #below values in crores
    fcf = 300
    totalShares = 7.64
    netdebt = -276.046
    #dcf calculation
    dcf, value = calculateByDcf(fcf, rate1t5, rate6t10, discount, terminal, totalShares, netdebt, marginOfSafety)
    print("Value (before MOS): " + str(dcf))
    print("Value (after MOS): " + str(value))