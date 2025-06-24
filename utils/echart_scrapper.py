import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import requests
import json

BASE_URL = "https://echarts.apache.org/examples/en/index.html"
DOMAIN = "https://echarts.apache.org/examples/examples/js/"

def init_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def extract_data_format(driver: WebDriver, link: str):
    driver.get(link)
    print(driver.page_source)


def get_example_links(driver):
    driver.get(BASE_URL)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []
    # nav_links = soup.select('a.left-chart-nav-link span.chart-name')
    results = {}
    example_lists = soup.select('div.example-list-panel > div')
    for div in example_lists:
        catagory = div.select_one('h3.chart-type-head').text.splitlines()[1].replace("'","").strip()
        charts = div.div.select('a.example-link')
        results[catagory] = []
        for chart in charts:
            types = {}
            href = chart.get("href")
            types['name'] = href.replace('./editor.html?c=', '')
            types['link'] = DOMAIN + types['name']  + ".js" if href.startswith('./editor.html?c=') else href
            results[catagory].append(types)

    return results

def js_to_json(js_code):
    # Basic JS to JSON conversion for ECharts `option` object
    js_code = js_code.replace("'", '"')  # replace single with double quotes
    js_code = re.sub(r'(\w+):', r'"\1":', js_code)  # add quotes to keys
    return js_code

def extract_echarts_example(js_url):
    response = requests.get(js_url)
    js_text = response.text

    # Extract metadata
    meta_match = re.search(r'/\*\s*title:\s*(.*?)\s*category:\s*(.*?)\s*titleCN:\s*(.*?)\s*difficulty:\s*(.*?)\s*\*/', js_text, re.DOTALL)
    metadata = {}
    if meta_match:
        metadata = {
            "title": meta_match.group(1).strip(),
            "category": meta_match.group(2).strip(),
            "titleCN": meta_match.group(3).strip(),
            "difficulty": int(meta_match.group(4).strip())
        }

    # Extract `option = {...};`
    option_match = re.search(r'option\s*=\s*({.*?});', js_text, re.DOTALL)
    option_data = {}
    if option_match:
        option_js = option_match.group(1)
        try:
            option_json_str = js_to_json(option_js)
            option_data = json.loads(option_json_str)
        except json.JSONDecodeError as e:
            option_data = {"error": f"Failed to parse option: {e}"}

    return {
        "metadata": metadata,
        "option": option_data
    }


def main():
    driver = init_driver()
    charts = get_example_links(driver)
    print(f"Found {len(charts)} chart examples.")


    for chart in charts.keys():
        for link in charts[chart]:
            try:
                option_raw = extract_echarts_example(link['link'])
                if option_raw:
                    link['option'] = option_raw['option']
                    print(f"Extracted {link['name']} successfully.")
                else:
                    print(f"No data found for {link['name']}.")
            except Exception as e:
                print(f"Error parsing {link}: {e}")

    driver.quit()
    with open("echarts_options.json", "w") as f:
        json.dump(charts, f, indent=2)

    print("Saved extracted chart options to echarts_options.json")

if __name__ == "__main__":
    main()
