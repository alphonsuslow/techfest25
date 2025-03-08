import requests
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright

def fetch_articles_moh():
    url = "https://www.moh.gov.sg/newsroom/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("a", class_="outline outline-offset-2 outline-link outline-0 group flex border-collapse flex-col gap-3 border-b border-divider-medium py-5 first:border-t lg:flex-row lg:gap-6")

    article_data = []
    for article in articles:
        link = article.get("href") 
        
        h3_tag = article.find("div").find("h3")
        if h3_tag:
            title = h3_tag.text.strip()
        else:
            title = "No title found"
        
        p_tag = article.find("p")
        date = p_tag.text.strip() if p_tag else "No date found"
        
        article_data.append({"title": title, "link": f"https://www.moh.gov.sg{link}", "date": date})

    return article_data

def fetch_articles_mccy():
    url = "https://www.mccy.gov.sg/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    grid_items = soup.find_all("div", class_="grid-item col25 animation-element")

    article_data = []
    for item in grid_items:
        link_tag = item.find("a")
        link = link_tag.get("href") if link_tag else None
        
        title_tag = item.find("div", class_="h3")
        title = title_tag.text.strip() if title_tag else "No title found"
        
        date_tag = item.find("small")
        date = date_tag.text.strip() if date_tag else "No date found"

        if link:
            article_data.append({"title": title, "link": f"https://www.mccy.gov.sg{link}", "date": date})

    return article_data

def fetch_articles_mddi():
    url = "https://www.mddi.gov.sg/media-centre/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    grid_items = soup.find_all("div", class_="col is-one-quarter-widescreen is-one-third-desktop is-half-tablet resource-card-element hide")

    grid_items = grid_items[:8]

    article_data = []
    for item in grid_items:
        link_tag = item.find("a")
        link = link_tag.get("href") if link_tag else None
        
        title_tag = item.find("h5", class_="has-text-white padding--bottom--lg")
        title = title_tag.text.strip() if title_tag else "No title found"
        
        date_tag = item.find("div", class_="is-fluid padding--top--md description").find("small", class_="has-text-white")
        date = date_tag.text.strip() if date_tag else "No date found"
        
        if link:
            article_data.append({
                "title": title, 
                "link": f"https://www.mddi.gov.sg{link}", 
                "date": date
            })

    return article_data

def fetch_articles_moe():
    url = "https://www.moe.gov.sg/newsroom/edtalks"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    article_links = soup.find_all("a", class_="hoverable moe-card m-t:xl m-b:m")

    article_data = []
    
    for link in article_links:
        title_tag = link.find("h2")
        title = title_tag.text.strip() if title_tag else "No title found"
        
        href = link["href"]
        article_url = f"https://www.moe.gov.sg{href}"

        date = ""

        article_data.append({
            "title": title,
            "link": article_url,
            "date": date
        })

    return article_data

def fetch_articles_mof():
    url = "https://www.mof.gov.sg/news-publications/press-releases/getNewsroomArticles/"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "month": "all",
        "year": "all",
        "title": "",
        "medium": "all",
        "topic": "all",
        "pageNumber": 1
    }

    response = requests.post(url, headers=headers, data=data)

    articles_data = response.json()
    
    articles = []
    for item in articles_data.get("Items", []):
        title = item.get("Title", "No title")
        link = item.get("RelativeUrl", "")
        date = item.get("ArticleDate", "No date")
        
        articles.append({
            "title": title,
            "link": f"https://www.mof.gov.sg{link}",
            "date": date
        })
    
    return articles

def fetch_articles_mfa():
    url = "https://www.mfa.gov.sg/Newsroom/Press-Statements-Transcripts-and-Photos"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    article_links = soup.find_all('div', class_='strip2')

    article_data = []
    
    for release in article_links:
        title = release.find('h3').text.strip()
        
        date = release.find('span', class_='date').text.strip()
        
        link = release.find('a')['href']

        article_data.append({
            "title": title,
            "link": link,
            "date": date
        })

    return article_data

def fetch_articles_mha():
    url = "https://www.mha.gov.sg/mediaroom"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("div", class_="media-list-items")

    article_data = []
    for article in articles:
        title_tag = article.find("h3", class_="media-subTitle")
        title = title_tag.text.strip() if title_tag else "No Title"

        link_tag = article.find("a", class_="underline-on-hover")
        href = "https://www.mha.gov.sg" + link_tag["href"] if link_tag and "href" in link_tag.attrs else "No Link"

        date_tag = article.find("p", class_="media-date")
        date = date_tag.text.strip() if date_tag else "No Date"

        article_data.append({
            "title": title,
            "link": href,
            "date": date
        })

    return article_data

def fetch_articles_law():
    url = "https://www.mlaw.gov.sg/news/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    grid_items = soup.find_all("div", class_="col is-one-quarter-widescreen is-one-third-desktop is-half-tablet resource-card-element hide")

    grid_items = grid_items[:8]

    article_data = []
    for item in grid_items:
        link_tag = item.find("a")
        link = link_tag.get("href") if link_tag else None
        
        title_tag = item.find("h5", class_="has-text-white padding--bottom--lg")
        title = title_tag.text.strip() if title_tag else "No title found"
        
        date_tag = item.find("div", class_="is-fluid padding--top--md description").find("small", class_="has-text-white")
        date = date_tag.text.strip() if date_tag else "No date found"
        
        if link:
            article_data.append({
                "title": title, 
                "link": f"https://www.mlaw.gov.sg{link}", 
                "date": date
            })

    return article_data

def fetch_articles_mom():
    url = "https://www.mom.gov.sg/newsroom/fact-checks"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("section.item-listing article")

    article_data = []
    for article in articles:
        title_tag = article.find("h3", class_="item-title").find("a")
        title = title_tag.text.strip() if title_tag else "No Title"

        href = "https://www.mom.gov.sg" + title_tag["href"] if title_tag and "href" in title_tag.attrs else "No Link"

        date_tag = article.find("time")
        date = date_tag.text.strip() if date_tag else "No Date"

        article_data.append({
            "title": title,
            "link": href,
            "date": date
        })

    return article_data

def fetch_articles_mnd():
    url = "https://www.mnd.gov.sg/newsroom/parliament-matters/q-as/GetList/"
    headers = {"User-Agent": "Mozilla/5.0"}

    data = {
        "year": "2025",
        "pageNumber": 1 
    }

    response = requests.post(url, headers=headers, data=data)
    articles_data = response.json()

    articles_data = articles_data[:8]

    extracted_articles = []

    for article in articles_data:
        title = article.get("Title", "No title found")
        url_name = article.get("UrlName", "")
        date = article.get("DateStr", "")
        
        article_url = f"https://www.mnd.gov.sg/newsroom/parliament-matters/q-as/view/{url_name}"
        
        extracted_articles.append({
            "title": title,
            "link": article_url,
            "date": date
        })

    return extracted_articles

def fetch_articles_mse():
    url = "https://www.mse.gov.sg/latest-news/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("a", class_="outline outline-offset-2 outline-link outline-0 group flex border-collapse flex-col gap-3 border-b border-divider-medium py-5 first:border-t lg:flex-row lg:gap-6")

    article_data = []
    for article in articles:
        link = article.get("href")
        
        h3_tag = article.find("div").find("h3")
        if h3_tag:
            title = h3_tag.text.strip()
        else:
            title = "No title found"
        
        p_tag = article.find("p")
        date = p_tag.text.strip() if p_tag else "No date found"
        
        article_data.append({"title": title, "link": f"https://www.mse.gov.sg{link}", "date": date})

    return article_data

def fetch_articles_mti():
    url = "https://www.mti.gov.sg/Newsroom/Press-Releases."
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    content_rows = soup.find_all('div', class_='list-content-row')

    article_data = []

    for row in content_rows:
        date_tag = row.find('div', class_='list-content-title')
        date = date_tag.text.strip() if date_tag else "No Date"

        link_tag = row.find('a')
        title = link_tag.text.strip() if link_tag else "No Title"
        link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No Link"

        article_data.append({
            "title": title,
            "link": f"https://www.mti.gov.sg{link}",
            "date": date
        })

    return article_data

async def fetch_articles_mot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  
        page = await browser.new_page()

        await page.goto("https://www.mot.gov.sg/news")

        await page.wait_for_selector("div.news-card")

        content = await page.content()

        soup = BeautifulSoup(content, "html.parser")

        news_cards = soup.find_all("div", class_="news-card")

        articles = []

        for card in news_cards:
            title = card.find("p", class_="news-title").get_text(strip=True)
            link = card.find("a", class_="news-card-body")["href"]
            date = card.find("span", class_="news-date").get_text(strip=True).split(" |")[0]
            
            if link.startswith("/"):
                link = "https://www.mot.gov.sg/news/Details" + link

            article = {
                "title": title,
                "link": link,
                "date": date
            }
            articles.append(article)

        await browser.close()

        return articles
    
async def fetch_articles_msf():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.msf.gov.sg/media-room")

        await page.wait_for_selector("div.col-12.col-lg-6")

        content = await page.content()

        soup = BeautifulSoup(content, "html.parser")

        news_cards = soup.find_all("div", class_="col-12 col-lg-6")

        articles = []

        for card in news_cards:
            title_tag = card.find("a", class_="article-link")
            title = title_tag.get_text(strip=True) if title_tag else None

            link = title_tag["href"] if title_tag and "href" in title_tag.attrs else None

            date_tag = card.find("p", class_="card-update-text")
            date = date_tag.get_text(strip=True).split("Published on:")[-1].strip() if date_tag else None

            article = {
                "title": title,
                "link": "https://www.msf.gov.sg" + link,
                "date": date
            }
            articles.append(article)

        await browser.close()

        return articles
    
async def fetch_articles_def():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) 
        page = await browser.new_page()

        await page.goto("https://www.mindef.gov.sg/news-and-events/latest-releases")

        await page.wait_for_selector("div.col-xs-12.col-sm-4.content-container")

        content = await page.content()

        soup = BeautifulSoup(content, "html.parser")

        news_cards = soup.find_all("a", class_="news-event-item-link")

        articles = []

        for card in news_cards:
            title = card.find("div", class_="content-title").text.strip()
            
            href = card['href'] if 'href' in card.attrs else None
            
            date = card.find("span", class_="type-body-2").text.strip()[1:]
            
            articles.append({
                "title": title,
                "href": href,
                "date": date
            })


        await browser.close()
        
        return articles