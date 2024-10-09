# WHAT THIS IS:
Crypto Auto Trader Script is a python script that runs at regular intervals to determine if a certain asset on the Kraken crypto trading platform is a good buy. It decides this by using a concrete set of  commandments and logic gates to determine how confident of an asset it is. 
# I AM NOT LIABLE: 
First of all, I am by no means an expert in crypto or stocks. I've invested in Doge at so many wrong points that now I'm at the point where I'd trust my own algorithm with my own money than me, lol. This entire project is merely an experiment that I am running so see if automatic trading and decision making is even possible or worthwhile. 
# TRADES MUST ABIDE BY ALL THE FOLLOWING: 
### 1. **If Market Trends are Favorable**
   - If the overall market trend is bullish (upward trend)
     - If the specific stock shows a consistent upward trend
       - If the stock is performing better than its sector average
         - If the stock's Price-to-Earnings (P/E) ratio is reasonable compared to historical averages
           - If the company's earnings are growing consistently
             - If the company has a strong balance sheet
               - Then **Buy**
             - Else
               - Then **Hold**
           - Else
             - Then **Hold**
         - Else
           - Then **Hold or Re-evaluate**
       - Else
         - Then **Hold or Re-evaluate**
     - Else
       - Then **Hold or Re-evaluate**
   - Else
     - Then **Hold**

### 2. **If Market Trends are Unfavorable**
   - If the overall market trend is bearish (downward trend)
     - If the specific stock shows a consistent downward trend
       - If the stock's Price-to-Earnings (P/E) ratio is high compared to historical averages
         - If the company's earnings are declining
           - If the company has a weak balance sheet
             - Then **Sell**
           - Else
             - Then **Hold**
         - Else
           - Then **Hold or Re-evaluate**
       - Else
         - Then **Hold or Re-evaluate**
     - Else
       - Then **Hold or Re-evaluate**
   - Else
     - Then **Hold**

### 3. **If Market is Volatile**
   - If the market shows high volatility (frequent large swings)
     - If the stock is highly volatile
       - If you have a low risk tolerance
         - Then **Hold or Re-evaluate**
       - Else
         - If the stock has strong fundamentals
           - Then **Hold**
         - Else
           - Then **Sell**
     - Else
       - Then **Hold**
   - Else
     - Then **Hold**

### 4. **If Market News or Events are Influential**
   - If there are significant news events affecting the market or the specific stock (e.g., earnings reports, mergers, acquisitions)
     - If news is positive
       - If the stock price reacts positively
         - If the positive news is likely to have a long-term impact
           - Then **Buy**
         - Else
           - Then **Hold**
       - Else
         - Then **Hold**
     - Else
       - If news is negative
         - If the stock price reacts negatively
           - If the negative news is likely to have a long-term impact
             - Then **Sell**
           - Else
             - Then **Hold**
         - Else
           - Then **Hold**
   - Else
     - Then **Hold**

### 5. **If Personal Financial Situation Changes**
   - If your personal financial situation changes (e.g., need for liquidity, change in risk tolerance)
     - If you need immediate liquidity
       - Then **Sell**
     - Else
       - If your risk tolerance increases
         - If market trends and stock fundamentals are favorable
           - Then **Buy**
         - Else
           - Then **Hold**
       - Else
         - Then **Hold**

### 6. **If Technical Indicators are Relevant**
   - If technical analysis supports the decision
     - If moving averages show a golden cross (short-term MA crosses above long-term MA)
       - Then **Buy**
     - Else
       - If moving averages show a death cross (short-term MA crosses below long-term MA)
         - Then **Sell**
       - Else
         - Then **Hold**
     - Else
       - Then **Combine with other analyses and decide**

