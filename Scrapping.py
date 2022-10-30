import requests
from bs4 import BeautifulSoup
from csv import writer


def part2(prurl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    PResult = requests.get(prurl, headers=headers)
    soupe = BeautifulSoup(PResult.content, 'html.parser')
    description = soupe.find(id='featurebullets_feature_div')
    details = soupe.find(id='detailBulletsReverseInterleaveContainer')
    detail = details.find('div', id='detailBullets_feature_div')
    ASIN = ""
    Manufacturer = ""
    title = detail.findAll('span', class_='a-list-item')
    for t in title:
        li = list(t.get_text().replace('\n','').split(':'))
        if len(li)!=0 and 'ASIN' in li[0]:
            ASIN = li[1].strip()
        if len(li)!=0 and 'Manufacturer' in li[0]:
            Manufacturer = li[1].strip()

    pdesc = soupe.find(id='productDescription_feature_div')
    ProductDesc = pdesc.find(id='productDescription')
    ProductDescription = ProductDesc.find('p').get_text()
    Dict = {
        "Description" : description.get_text(),
        "ASIN" : ASIN,
        "Manufacturer" : Manufacturer,
        "Product_Description" : ProductDescription 
    }
    print(Dict)
    return Dict

# part2("https://www.amazon.in/Acrux-Polyester-Waterproof-Raincover-Navyorange/dp/B0BJZWFJRQ/ref=sr_1_239?crid=2M096C61O4MLT&keywords=bags&qid=1667123995&qu=eyJxc2MiOiI4LjAzIiwicXNhIjoiOC4wNSIsInFzcCI6IjYuNzUifQ%3D%3D&sprefix=ba%2Caps%2C283&sr=8-239")


# driver code
url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
with open('Products.csv', 'w', encoding='utf-8', newline='') as f:
    thewriter = writer(f)
    head = ['Product_url', 'Product_name', 'Reviews', 'Ratings', 'Price', 'Description', 'ASIN', 'Manufacturer', 'Product Description']
    thewriter.writerow(head)
    for i in range(2,21):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        lists = soup.findAll('div', class_='s-list-col-right')
        for list in lists:
            Productdetails = list.find('h2', class_='s-line-clamp-2')
            Product_name = list.find('span', class_='a-size-medium').get_text()
            purl = Productdetails.find("a").get('href')
            Product_url = "https://www.amazon.in"+purl
            revratcontainer = list.find('div', class_='a-spacing-top-micro')
            toggler = True
            for l in revratcontainer.find_all('a'):
                if toggler:
                    Reviews = l.get_text()
                    toggler = False
                else:
                    Ratings = l.get_text()
            prices = list.find('div', class_='sg-row')
            pricecontainer = prices.find('div', class_='s-price-instructions-style')
            Price = pricecontainer.find('span', class_='a-offscreen').get_text()
            obj = part2(Product_url)

            info = [Product_url, Product_name, Ratings, Reviews, Price[1:], obj['Description'], obj['ASIN'], obj['Manufacturer'], obj['Product_Description']]
            thewriter.writerow(info)
        
        url = "https://www.amazon.in/s?k=bags&page="+str(i)