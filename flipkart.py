from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def scrape_flipkart(keyword):
    results = []
    driver = webdriver.Chrome()
    for page in range(1, 6):
        url = f"https://www.flipkart.com/search?q={keyword}&page={page}"
        driver.get(url)
        time.sleep(3)  # Give time for the page to load
        prods = driver.find_elements(By.CLASS_NAME, "cPHDOP col-12-12")
        for i in range(1, 26):
            try:
                prod_path = f'//*[@id="container"]/div/div[3]/div[1]/div[2]/div[{i}]'
                name = driver.find_element(By.XPATH, f'{prod_path}/div/div/div/a/div[2]/div[1]/div[1]').text
                rating = driver.find_element(By.XPATH, f'{prod_path}/div/div/div/a/div[2]/div[1]/div[2]/span[1]/div').text
                price = driver.find_element(By.XPATH, f'{prod_path}/div/div/div/a/div[2]/div[2]/div[1]/div[1]/div[1]').text
                
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
    results = scrape_flipkart(keyword)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
