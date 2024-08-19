import tkinter as tk
from tkinter import messagebox
import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


# Function to fetch a single random quote from the API
def fetch_single_quote():
    api_url = "https://quotes-api-self.vercel.app/quote"


    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an error for bad status codes
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return None


# Function to fetch multiple quotes at the same time...
def fetch_multiple_quotes_concurrently(num_quotes=20):
    quotes = []

    # Using ThreadPoolExecutor to fetch quotes concurrently
    with ThreadPoolExecutor(max_workers=num_quotes) as executor:
        futures = [executor.submit(fetch_single_quote) for _ in range(num_quotes)]

        for future in as_completed(futures):
            quote_data = future.result()
            if quote_data:
                quotes.append(quote_data)

    return quotes


# Function to match the quote word or keywords with the user input, and fallback
def find_matching_quote(quotes, mood):
    mood_lower = mood.lower()
    for quote_data in quotes:
        quote = quote_data['quote'].lower()
        if mood_lower in quote:
            return f"{quote_data['quote']} - {quote_data['author']}"

    # Fallback if no matching quote is found
    fallback_quote = random.choice(quotes)
    return (f"Perhaps, I have something here that might inspire you:"
            f"\n\n{fallback_quote['quote']} - {fallback_quote['author']}")


# Function for the button in graphical user interface(GUI)
def get_quote():
    mood = mood_entry.get()
    quotes = fetch_multiple_quotes_concurrently(num_quotes=20)
    quote = find_matching_quote(quotes, mood)
    result_label.config(text=quote)


# How the GUI works
root = tk.Tk()
root.title("Inspire me - Made by Jahan")

# Name for the mood and input
mood_label = tk.Label(root, text="How do you feel today?")
mood_label.pack(pady=10)
mood_entry = tk.Entry(root, width=50)
mood_entry.pack(pady=10)

# Button for getting the quote
get_quote_button = tk.Button(root, text="Get Quote", command=get_quote)
get_quote_button.pack(pady=20)

# Label for delivering the quote for the user
result_label = tk.Label(root, text="", wraplength=400, justify="center")
result_label.pack(pady=20)

# To run the program
root.mainloop()
