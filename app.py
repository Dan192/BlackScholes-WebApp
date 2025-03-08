import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from blackscholes import BlackScholes

st.set_page_config(
    page_title = "Black-Scholes Calculator",
    layout = "wide",
    initial_sidebar_state = "expanded",
)

st.title("Black-Scholes Calculator")

with st.sidebar:

    st.title('Black-Scholes Parameters')
    linkedin_logo_url = "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png"
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="{linkedin_logo_url}" width = "20" style="margin-right: 10px;"/>
            <span>Developed by: <a href="https://www.linkedin.com/in/dan-rassouli/" target="_blank">Daniel Rassouli</a></span>
        </div>
        """,
        unsafe_allow_html = True
    )

    st.write("")

    stock_price = st.number_input("Stock Price", value = 100.0)
    exercise_price = st.number_input("Exercise Price", value = 100.0)
    time = st.number_input("Maturity", min_value = 0.1, max_value = 5.0, value = 1.0, step = 0.1)
    risk_free_rate = st.number_input("Risk-Free Rate", min_value = 0.01, max_value = 10.0, value = 0.05, step = 0.01)
    volatility = st.number_input("Volatility", min_value = 0.01, max_value = 1.0, value = 0.2, step = 0.01)

    st.title('Heatmap Variables')
    spot_min = st.number_input('Minimum Spot Price', min_value = 0.01, value=stock_price * 0.8, step = 0.01)
    spot_max = st.number_input('Maximum Spot Price', min_value = 0.01, value=stock_price * 1.2, step = 0.01)
    vol_min = st.slider('Minimum Volatility for Heatmap', min_value = 0.01, max_value = 1.0, value = 0.1, step = 0.01)
    vol_max = st.slider('Maximum Volatility for Heatmap', min_value = 0.01, max_value = 1.0, value = 0.3, step = 0.01)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

# Initialize Black-Scholes model
scholes_model = BlackScholes(stock_price, exercise_price, risk_free_rate, time, volatility)

data = {
    "Current Price": [stock_price],
    "Exercise Price": [exercise_price],
    "Risk-Free Rate": [risk_free_rate],
    "Maturity": [time],
    "Volatility": [volatility]
}

table1 = pd.DataFrame(data)
st.table(table1)

col1, col2 = st.columns(2)

box_style = """
    <div style="
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 5px;">
        {}
    </div>
"""

call_price = scholes_model.call_price()
put_price = scholes_model.put_price()

with col1:
    st.markdown(box_style.format(f"Call Price: ${call_price:,.2f}"), unsafe_allow_html = True)
with col2:
    st.markdown(box_style.format(f"Put Price: ${put_price:,.2f}"), unsafe_allow_html = True)

st.markdown(
    """
    <style>
    .stTabs [role="tablist"] {
        justify-content: center; /* Center-align the tabs */
    }
    </style>
    """,
    unsafe_allow_html = True
)

main, tab1, tab2, tab3, tab4, tab5 = st.tabs(["Option Price Heatmap", "Delta Heatmap", "Gamma Surface Plot", "Vega Heatmap", "Theta Line Plot", "Rho Line Plot"])

def plot_option_price_heatmaps(scholes_model: BlackScholes, spot_range: np.ndarray, vol_range: np.ndarray, exercise_price: float) -> None:
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time = scholes_model.time,
                exercise_price = exercise_price,
                stock_price = spot,
                volatility = vol,
                risk_free_rate = scholes_model.risk_free_rate
            )
            call_price = bs_temp.call_price()
            put_price = bs_temp.put_price()
            call_prices[i, j] = call_price
            put_prices[i, j] = put_price

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Call Option Price Heatmap")
        fig_call, ax_call = plt.subplots(figsize=(8, 6))
        sns.heatmap(call_prices, xticklabels = np.round(spot_range, 2), yticklabels = np.round(vol_range, 2), annot = True, fmt = ".2f", cmap = "plasma", ax = ax_call,)
        ax_call.set_title("Call Option Prices")
        ax_call.set_xlabel("Spot Price")
        ax_call.set_ylabel("Volatility")
        st.pyplot(fig_call)

    with col2:
        st.subheader("Put Option Price Heatmap")
        fig_put, ax_put = plt.subplots(figsize = (8, 6))
        sns.heatmap(put_prices, xticklabels = np.round(spot_range, 2), yticklabels = np.round(vol_range, 2), annot = True, fmt = ".2f", cmap = "plasma", ax = ax_put)
        ax_put.set_title("Put Option Prices")
        ax_put.set_xlabel("Spot Price")
        ax_put.set_ylabel("Volatility")
        st.pyplot(fig_put)


def generate_heatmap(greek: str, scholes_model: BlackScholes) -> None:
    call_matrix = np.zeros((len(vol_range), len(spot_range)))
    put_matrix = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            scholes_model.stock_price = spot
            scholes_model.volatility = vol

            if greek == "Delta":
                call_matrix[i, j] = scholes_model.delta(option_type = "call")
                put_matrix[i, j] = scholes_model.delta(option_type = "put")
            elif greek == "Vega":
                call_matrix[i, j] = scholes_model.vega()
                put_matrix[i, j] = scholes_model.vega()
            

    col1, col2 = st.columns(2)

    with col1:
        plt.figure(figsize = (8, 6))
        sns.heatmap(call_matrix.T, xticklabels = [f'{p:.0f}' for p in spot_range], yticklabels = [f'{v:.2f}' for v in vol_range], cmap = "plasma", square = True, annot = True)
        plt.title(f"Call Option {greek} Heatmap")
        plt.ylabel("Volatility")
        plt.xlabel("Spot Price")
        st.pyplot(plt)

    with col2:
        plt.figure(figsize = (8, 6))
        sns.heatmap(put_matrix.T, xticklabels = [f'{p:.0f}' for p in spot_range], yticklabels = [f'{v:.2f}' for v in vol_range], cmap = "plasma", square = True, annot = True)
        plt.title(f"Put Option {greek} Heatmap")
        plt.ylabel("Volatility")
        plt.xlabel("Spot Price")
        st.pyplot(plt)


def generate_surface_plot(scholes_model: BlackScholes, spot_range: np.ndarray, vol_range: np.ndarray) -> None:
    gamma_values = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            scholes_model.stock_price = spot
            scholes_model.volatility = vol
            gamma_values[i, j] = scholes_model.gamma()
    
    X, Y = np.meshgrid(spot_range, vol_range)

    if gamma_values.shape != X.shape or gamma_values.shape != Y.shape:
        st.error("Mismatch in data dimensions for surface plot.")
        return
    
    fig = plt.figure(figsize = (10, 8))
    ax = fig.add_subplot(111, projection = "3d")
    color = ax.plot_surface(X, Y, gamma_values, cmap = "viridis", edgecolor = "k")
    ax.set_title("Gamma Surface Plot")
    ax.set_xlabel("Spot Price")
    ax.set_ylabel("Volatility")
    ax.set_zlabel("Gamma")
    fig.colorbar(color, shrink = 0.5, aspect = 10)
    st.pyplot(fig)

time_range = np.linspace(0.1, scholes_model.time, 20)

def generate_line_plot(greek: str, scholes_model: BlackScholes, time_range: np.ndarray) -> None:
    call_values = []
    put_values = []

    for time in time_range:
        scholes_model.time = time
        if greek == "Theta":
            call_values.append(scholes_model.theta(option_type = "call"))
            put_values.append(scholes_model.theta(option_type = "put"))
        elif greek == "Rho":
            call_values.append(scholes_model.rho(option_type = "call"))
            put_values.append(scholes_model.rho(option_type = "put"))
        else:
            raise ValueError("Invalid Greek specified. Use Theta or Rho")
    
    plt.figure(figsize = (8, 6))
    plt.plot(time_range, call_values, label = f"Call Option {greek}")
    plt.plot(time_range, put_values, label = f"Put Option {greek}")
    plt.title(f"{greek} vs Time to Maturity")
    plt.xlabel("Time to Maturity (Years)")
    plt.ylabel(greek)
    plt.legend()
    st.pyplot(plt)

with main:
    st.info("The following Heatmap depicts how Call and Put option prices change with Spot Price and Volatility")
    st.info("This plot helps visualize the overall value of an option under different market conditions which is critical for pricing and decision making")
    plot_option_price_heatmaps(scholes_model, spot_range, vol_range, exercise_price)

with tab1:
    st.info("Delta measures how much an option price changes with a change in the underlying asset price")
    st.info("Delta indicates the hedge ratio. This tells traders how many shares to buy or sell in order to hedge their original option position")
    generate_heatmap("Delta", scholes_model)

with tab2:
    st.write("*Note: Gamma formula is identical for Calls and Puts.*")
    st.info("Gamma measures the sensitivity of Delta, specifically how Delta changes as the underlying asset price changes")
    st.info("This Surface Plot highlights the risk of sudden changes in Delta, especially for options near the strike price")
    st.info("Plotted in a 3D Surface Plot because volatility isn't fixed. Users can play around with volatility")
    generate_surface_plot(scholes_model, spot_range, vol_range)

with tab3:
    st.write("*Note: Vega formula is identical for Calls and Puts.*")
    st.info(f"Vega measures the sensitivity of an option price to a % change in volatility")
    st.info("Vega shows the sensitivity to market uncertainty, which can help traders manage exposure to volatility")
    generate_heatmap("Vega", scholes_model)

with tab4:
    st.info("Theta measures how much the option price decreases as we get closer to maturity")
    st.info("Theta highlights the cost of holding an option, which increases as the expiration date approaches")
    generate_line_plot("Theta", scholes_model, time_range)

with tab5:
    st.write("*Note: Rho is generally considered to be the least important greek*")
    st.info(f"Rho measures an option price's sensitivity to a % change in interest rates")
    st.info("Rho is important for managing exposure to interest rate changes for long-term options")
    generate_line_plot("Rho", scholes_model, time_range)