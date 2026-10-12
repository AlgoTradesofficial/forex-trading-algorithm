# Algorithmic Forex Trading Strategy

**A personal software development project exploring algorithmic trading, automation, historical backtesting, and AI-assisted programming using Python and Pine Script.**

## Project Overview

AlgoTrades is a personal project I developed to explore how financial trading strategies can be translated into automated, rule-based algorithms.

I began by independently designing a forex trading strategy based on market structure, liquidity movements, and price action. I then used AI-assisted programming to implement the strategy in Pine Script for TradingView and Python for QuantConnect.

Throughout development, I focused on testing the algorithm, identifying weaknesses, refining parameters, and evaluating performance using historical market data.

My primary goal was to develop practical experience in software development, algorithm design, problem-solving, and data-driven optimisation while working on a project that combines my interests in technology and financial markets.

## Technologies Used

- **Python** — Algorithm implementation and historical backtesting.
- **Pine Script (v6)** — Automated strategy development within TradingView.
- **TradingView** — Strategy visualisation, initial backtesting, and debugging.
- **QuantConnect** — Extended historical data testing and performance analysis.
- **GitHub** — Source code management, documentation, and project sharing.
- **ChatGPT (OpenAI GPT-6)** — AI-assisted code generation, debugging, and implementation based on my independently developed trading strategy and specifications.

## Trading Strategy

The algorithm follows a structured, rule-based approach to identifying potential trading opportunities in the forex market.

Its main components include:

### 1. Trading Session Analysis
The algorithm tracks price movements across predefined trading sessions and records relevant session highs and lows.

### 2. Liquidity Sweep Detection
It identifies when price moves beyond previously established session highs or lows, potentially indicating a liquidity sweep.

### 3. Change of Structure
Following a liquidity sweep, the algorithm looks for a change in market structure to confirm a potential shift in price direction.

### 4. Fair Value Gap Identification
The algorithm detects three-candle price imbalances known as fair value gaps and uses predefined conditions to identify potential entries.

### 5. Risk Management
The strategy includes automated calculations for:

- Position sizing
- Stop-loss placement
- Take-profit targets
- Risk-to-reward ratios
- Percentage-based risk allocation

These components allow the trading rules to be consistently applied and evaluated through historical simulation.

## Historical Backtesting Results

I implemented a Python-based historical simulator using QuantConnect to evaluate the strategy over an extended period of GBP/USD market data.

**Backtesting period:** 1 July 2025 – 1 June 2026

| Performance Metric | Result |
|---|---|
| Starting Simulated Capital | $10,000 |
| Final Simulated Equity | $16,275 |
| Simulated Return | +62.75% |
| Profit Factor | 1.134 |
| Currency Pair | GBP/USD |
| Risk Setting | 10% per trade |
| Take-Profit Ratio | 0.5R |

### Backtest Performance

![QuantConnect Historical Backtesting Results](backtest-results.png)

*Historical backtesting results from the custom Python trading simulator.*

**Disclaimer:** These results are from historical simulation, not live trading. The simulator uses simplified execution assumptions and does not explicitly account for spreads, commissions, or slippage. Results may also be affected by parameter optimisation and do not guarantee future profitability.

## Development and Optimisation

A significant part of this project involved experimenting with algorithm parameters and improving the strategy through repeated testing.

During development, I:

- Designed the initial trading rules and entry conditions.
- Translated my strategy specifications into programming requirements.
- Tested different risk management parameters and stop-loss buffers.
- Evaluated performance using historical financial data.
- Compared strategy performance across different currency pairs and testing periods.
- Identified weaknesses and adjusted the algorithm's parameters.
- Used testing results to guide further development and revisions.

One of my key achievements was extending the testing process beyond TradingView's initially available historical data by developing a Python-based simulator within QuantConnect.

This allowed me to analyse performance over a substantially longer period and make more informed decisions about algorithm behaviour.

## Development Approach and AI Usage

### Independent Strategy Development

I independently developed the financial trading strategy, including its underlying concepts, entry and exit conditions, market analysis rules, risk management approach, and optimisation decisions.

Throughout the project, I determined which improvements to pursue, evaluated the results of historical tests, and directed revisions to the algorithm.

### AI-Assisted Implementation

I used **OpenAI's ChatGPT (GPT-6)** to assist with generating and debugging the Pine Script and Python code.

My development process involved:

1. Defining the trading strategy and converting my ideas into detailed programming specifications.
2. Using AI to generate the initial code implementations.
3. Testing the generated code within TradingView and QuantConnect.
4. Identifying errors, unexpected behaviour, and opportunities for improvement.
5. Directing code revisions and adjusting parameters based on my analysis.
6. Repeating the testing and refinement process to improve the implementation.

While AI assisted with writing the code, the strategy design, development requirements, financial decisions, testing direction, and evaluation of results were independently managed by me.

This project demonstrates my ability to use AI development tools effectively while applying critical thinking, problem-solving, and analytical decision-making to a practical software development challenge.

## Skills Developed

Through this project, I developed experience in:

**Software Development**
- Understanding and working with Python and Pine Script
- Algorithm design and logical problem-solving
- Conditional statements, functions, and state management
- Debugging and iterative development
- Reading, testing, and refining AI-generated code

**Data Analysis and Testing**
- Historical simulation and backtesting
- Performance metric analysis
- Parameter experimentation and optimisation
- Identifying limitations in testing methodologies
- Comparing algorithm behaviour across different conditions

**Project Management**
- Translating real-world ideas into technical requirements
- Independently managing an ongoing software project
- Documenting implementation decisions
- Evaluating results and identifying future improvements

## Repository Structure

```text
forex-trading-algorithm/
│
├── forex_strategy.pine
│   └── TradingView strategy implementation
│
├── quantconnect_forex_simulator.py
│   └── Python historical trading simulator
│
├── backtest-results.png
│   └── Historical simulation results screenshot
│
└── README.md
    └── Project documentation
```

## Future Development

I plan to continue improving this project by:

- Introducing more realistic execution assumptions, including spreads and slippage.
- Testing across additional currency pairs and market conditions.
- Implementing out-of-sample testing to evaluate robustness.
- Improving code organisation and maintainability.
- Expanding automated validation and testing.
- Exploring opportunities to incorporate machine learning and artificial intelligence into financial market analysis.

## About Me

I am currently studying Computer Science and Commerce at the University of Auckland, with a strong interest in artificial intelligence, software development, and financial technology.

I enjoy building practical projects that allow me to apply technical concepts, develop new skills, and solve real-world problems.

AlgoTrades represents my interest in combining technology, independent learning, financial analysis, and AI-assisted software development to create functional applications.

---

*This project is intended for educational, experimental, and software development purposes. It does not constitute financial advice.*
