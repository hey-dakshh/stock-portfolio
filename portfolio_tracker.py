import yfinance as yf
import json

# Portfolio management functions
def add_stock(portfolio, symbol, quantity, purchase_price):
    """Add a stock to the portfolio."""
    portfolio[symbol] = {'quantity': quantity, 'purchase_price': purchase_price, 'current_price': 0.0}

def remove_stock(portfolio, symbol):
    """Remove a stock from the portfolio."""
    if symbol in portfolio:
        del portfolio[symbol]
    else:
        print(f"Stock {symbol} not found in portfolio.")

# Fetch real-time stock data
def get_stock_price(symbol):
    """Fetch the latest stock price using yfinance."""
    stock = yf.Ticker(symbol)
    # Get the last closing price
    return stock.history(period="1d")['Close'][0]

# Calculate stock performance
def calculate_stock_performance(stock_data):
    """Calculate percentage gain/loss for a stock."""
    current_price = stock_data['current_price']
    purchase_price = stock_data['purchase_price']
    return ((current_price - purchase_price) / purchase_price) * 100

# Display portfolio summary
def print_portfolio_summary(portfolio):
    """Print a summary of the portfolio."""
    total_value = 0
    print("\nPortfolio Summary:")
    print("=" * 40)
    for stock, data in portfolio.items():
        data['current_price'] = get_stock_price(stock)
        performance = calculate_stock_performance(data)
        stock_value = data['quantity'] * data['current_price']
        total_value += stock_value
        print(f"{stock}: {data['quantity']} shares | "
              f"Purchase Price: ${data['purchase_price']} | "
              f"Current Price: ${data['current_price']:.2f} | "
              f"Value: ${stock_value:.2f} | "
              f"Performance: {performance:.2f}%")
    print("=" * 40)
    print(f"Total Portfolio Value: ${total_value:.2f}")

# Save portfolio to a file
def save_portfolio(portfolio, filename='portfolio.json'):
    """Save the portfolio to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(portfolio, file)

# Load portfolio from a file
def load_portfolio(filename='portfolio.json'):
    """Load the portfolio from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Main program
if __name__ == "__main__":
    portfolio = load_portfolio()

    # Example stock actions
    add_stock(portfolio, 'AAPL', 10, 150)
    add_stock(portfolio, 'GOOG', 5, 1000)
    add_stock(portfolio, 'MSFT', 15, 250)

    print_portfolio_summary(portfolio)

    save_portfolio(portfolio)