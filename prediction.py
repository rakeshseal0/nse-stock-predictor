import requests
from bs4 import BeautifulSoup
from colored import fg, attr


def predict():
    url = "https://munafasutra.com/nse/todayIntraday/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    datas = soup.findAll("tr")[1:]
    for idx, dat in enumerate(datas):
        d = dat.text.split("  ")[0]
        print(str(idx + 1) + ". " + fg(idx%2 + 2) + d + attr(0))


if __name__ == "__main__":
    predict()
