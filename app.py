from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_transactions(company_name):
    base_url = "https://marknadssok.fi.se/Publiceringsklient/sv-SE/Search/Search/Insyn"
    params = {
        "SearchFunctionType": "Insyn",
        "Utgivare": company_name,
        "button": "search"
    }

    all_transactions = []

    while True:
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        transactions = soup.find("tbody").find_all("tr")

        for transaction in transactions:
            transaction_data = {}
            columns = transaction.find_all("td")
            transaction_data["Date"] = columns[0].text.strip()
            transaction_data["Company"] = columns[1].text.strip()
            transaction_data["Person"] = columns[2].text.strip()
            transaction_data["Position"] = columns[3].text.strip()
            transaction_data["Transaction Type"] = columns[5].text.strip()
            transaction_data["Amount"] = columns[10].text.strip()
            transaction_data["Currency"] = columns[12].text.strip()
            transaction_data["Character"] = columns[5].text.strip() # Assuming "karaktär" is the 4th column
            transaction_data["typ"] = columns[7].text.strip() # Assuming "karaktär" is the 4th column

            all_transactions.append(transaction_data)

        next_page = soup.find("li", class_="next")
        if next_page:
            next_page_link = next_page.find("a")
            if next_page_link:
                params["Page"] = next_page_link["href"].split("=")[-1]
            else:
                break
        else:
            break

    return all_transactions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    company_name = request.form['company_name']
    transactions = get_transactions(company_name)
    return render_template('results.html', company_name=company_name, transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
