from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def scrape(keyword):
    results = []
    driver = webdriver.Chrome()
    for page in range(1, 6):
        url = f"https://www.amazon.in/s?k={keyword}&page={page}"
        driver.get(url)
        time.sleep(3) 
        for i in range(1, 26):
            try:
                prod_path = f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]'
                name = driver.find_element(By.XPATH, f'{prod_path}/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a/span').text
                rating = driver.find_element(By.XPATH, f'{prod_path}/div/div/span/div/div/div/div[2]/div/div/div[2]/div[1]/span[1]').get_attribute("aria-label")
                price = ""
                try:
                    elem = driver.find_element(By.XPATH, prod_path)
                    price = "₹" + elem.find_element(By.CLASS_NAME, 'a-price-whole').text
                except Exception:
                    pass

                try:
                    price = driver.find_element(By.XPATH, f'{prod_path}/div/div/span/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[3]/div/span[2]').text
                except Exception:
                    pass
                
                results.append({"name": name, "rating": rating, "price": price})
            except Exception as e:
                continue

    driver.quit()
    return results

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Please provide a keyword parameter"}), 400
    results = scrape_amazon(keyword)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
