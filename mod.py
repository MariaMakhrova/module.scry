import requests
from bs4 import BeautifulSoup
import csv

# Функція для отримання даних про телевізори 
def scrape_olx_tv_offers():
    url = "https://www.olx.ua/elektronika/tovary-dlya-kompyutera/monitory-i-aksesuary/monitory/tovary-dlya-kompyutera/monitory-i-aksesuary/monitory/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    tv_offers = []

    while url:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Отримання списку оголошень
        offers = soup.find_all("div", class_="offer-wrapper")

        # Збираємо дані про кожне оголошення
        for offer in offers:
            title = offer.find("a", class_="marginright5 link linkWithHash detailsLink").text.strip()
            price = offer.find("p", class_="price").text.strip()
            location = offer.find("small", class_="breadcrumb x-normal").text.strip()
            date = offer.find("div", class_="space inlblk rel").find("p", class_="color-9 lheight16 marginbott5 x-normal").text.strip()

            tv_offers.append([title, price, location, date])

        # Переходимо на наступну сторінку, якщо вона є
        next_button = soup.find("a", class_="block br3 brc8 large tdnone lheight24")
        url = next_button['href'] if next_button else None

    return tv_offers

# Записуємо дані в CSV файл
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Назва", "Ціна", "Місце", "Дата"])
        writer.writerows(data)

# Отримуємо дані та записуємо їх в CSV файл
tv_data = scrape_olx_tv_offers()
save_to_csv(tv_data, 'olx_tv_offers.csv')
