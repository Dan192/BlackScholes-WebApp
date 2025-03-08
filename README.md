# Black-Scholes Option Pricing and Greek Visualizations

## Overview

This project implements the Black-Scholes option pricing model to calculate option prices and their respective Greeks (Delta, Gamma, Vega, and Theta) allowing Quants and Traders to visualize their respective current positions. Additionally, it generates various graphs and charts in order to visualize the impact of varying spot prices and volatilities on the Greeks for both Call and Put options.

## Features

- **Black-Scholes Model Implementation**: Computes option prices and Greeks based on user-defined inputs.
- **Interactive UI with Streamlit**: Users can adjust parameters like spot price, volatility, and option type.
- **Tabs for Different Greeks**: Separate tabs allow easy navigation between Delta, Gamma, Vega, and Theta.

## Installation
Ensure you have Python 3.7+ installed. Then, install the necessary dependencies:

```sh
pip install -r requirements.txt
```
Or manually install required libraries:

```sh
pip install numpy pandas scipy streamlit seaborn matplotlib
```

## Usage
Run the Streamlit application using:

```sh
streamlit run app.py
```

### User inputs
- Stock Price: The current market price of the asset
- Exercise Price: The strike price of the option
- Risk-Free Rate: The prevailing risk-free interest rate
- Time to Maturity: The time remaining until the option expires
- Volatility: The expected volatility of the underlying asset

### Heatmap Parameters:
- Spot Price Range: Adjustable from a minimum to maximum value
- Volatility Range: Adjustable to visualize sensitivity

## Expected Behavior
- Delta Heatmap: Displays sensitivity of option price to changes in the underlying asset price
- Gamma Surface Plot: Measures the rate of change of Delta
- Vega Heatmap: Displays how volatility impacts the option price
- Theta Line Plot: Measures time decay effects
- Rho Line Plot: Measures exposure to interest rate changes for long-term options

## Troubleshooting
If the visualizations do not display properly, ensure all required packages are installed and rerun the script
Verify numerical stability by adjusting step sizes in np.linspace() for spot prices and volatilities

## License
This project is licensed under the MIT License

## Author
Developed by Daniel Rassouli
