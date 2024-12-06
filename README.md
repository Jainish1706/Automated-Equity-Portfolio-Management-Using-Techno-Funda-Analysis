# Automated Equity Portfolio Management Using Techno-Funda Analysis

This repository contains the Python-based implementation for **Automated Equity Portfolio Management** using an integrated **Techno-Funda Analysis** approach. The project was developed as part of the experimental research presented at **NICOM 2025, Nirma University**.

## 📄 Abstract

The research explores a dynamic framework for equity portfolio management, combining **fundamental** and **technical analysis** to create and manage optimal stock portfolios. Stocks from the **NIFTY 100 index** are screened based on financial metrics, technical indicators, and optimization techniques like **Efficient Frontier** and **Monte Carlo Simulations**. The strategy automates stock selection, portfolio optimization, and trading decisions using Python, ensuring a continuous closed-loop system for real-time adjustments.

---

## 🚀 Features

- **Data Sources**: 
  - Financial metrics (e.g., Revenue, EPS, PE ratio) via Screener.in.
  - Historical stock prices via Yahoo Finance API (`yfinance`).

- **Fundamental Analysis**:
  - Screening based on CAGR, EBITDA margins, and projected PE ratios.
  - Ranking stocks for portfolio inclusion.

- **Portfolio Optimization**:
  - Efficient Frontier analysis for risk-return optimization.
  - Monte Carlo Simulations to maximize Sharpe Ratio.

- **Technical Analysis**:
  - Entry/Exit signals using:
    - EMA Crossovers (e.g., EMA 20-50, EMA 9-15).
    - ADX slopes and RSI thresholds.

- **Performance Evaluation**:
  - Extended Internal Rate of Return (XIRR) for trading performance.
  - Comparison with benchmark returns (NIFTY 100).

---

## 🛠️ Methodology

1. **Data Preparation**:
   - Gather historical financial and stock price data.
2. **Fundamental Screening**:
   - Screen stocks based on CAGR, EBITDA margins, and PE ratio projections.
   - Rank top 30 stocks for portfolio consideration.
3. **Portfolio Optimization**:
   - Use Monte Carlo Simulations and Efficient Frontier to allocate weights.
4. **Technical Entry/Exit**:
   - Apply technical indicators for trading decisions.
5. **Performance Tracking**:
   - Calculate XIRR for portfolio stocks and compare with benchmarks.
6. **Dynamic Updates**:
   - Automatically update the portfolio with new financial data and technical signals.

---

## 📊 Results

- **Fundamental Screening**: Filtered stocks with strong growth trajectories and margins.
- **Efficient Frontier Analysis**: Identified optimal portfolios with maximum Sharpe ratios.
- **Performance Metrics**: Achieved atleast 5 percent higher returns compared to NIFTY 100 benchmarks.<br><br>
![Screenshot 2024-12-06 122558](https://github.com/user-attachments/assets/5d2d664c-b595-4327-9183-90ef0f633ef4)
---

## 🧰 Tools and Technologies

- **Programming Language**: Python
- **Environment**: vs code
- **Libraries**:
  - `yfinance` for stock price data.
  - `numpy` and `pandas` for data manipulation.
  - `matplotlib` for visualizations.

---

## 📝 Future Scope

- Expand the stock universe for broader diversification.
- Integrate advanced risk management and machine learning models.
- Implement real-time algorithmic trading.

---

## 📖 References

1. Hilkevics, S., & Zablockis, A. (2016). *The Combination of Fundamental and Technical Analysis In Portfolio Optimization*.
2. Oosterlee, C.W., & Cong, F. (2016). *Multi-period Mean–Variance Portfolio Optimization Based on Monte-Carlo Simulation*.
3. Seetharaman, A., et al. (2017). *A Study of Factors Influencing Portfolio Choices in Singapore*.
4. Leran Dai. (2023). *Portfolio Optimization Using Markowitz and Index Models*.

---

## 📧 Authors

- **Vishwas Darji** - Pandit Deendayal Energy University  
- **Gautam Makwana** - Pandit Deendayal Energy University  
- **Jainish Shah** - Indian Institute of Science Education and Research, Thiruvananthapuram  

---


