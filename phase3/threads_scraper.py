"""
Scrape Instagram Threads posts and export specific fields to a text file.
Fetches posts from usernames in threads_usernames_verified.txt

Requirements:
- selenium
- beautifulsoup4
- webdriver-manager
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Required package not found: {e}")
    print("Install with: pip install selenium beautifulsoup4 webdriver-manager")
    sys.exit(1)


def load_threads_usernames(filename: str = "threads_usernames_verified.txt") -> List[str]:
    """Load Threads usernames from a text file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f if line.strip()]
        return usernames
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)


def format_post_data(post: Dict[str, Any]) -> str:
    """Format a single post as mm/dd/yyyy text."""
    text = post.get('text', 'N/A')
    created = post.get('created_at', '')

    if created:
        try:
            date_only = created.split("T")[0]
            year, month, day = date_only.split("-")
            formatted_date = f"{month}/{day}/{year}"
        except:
            formatted_date = "N/A"
    else:
        formatted_date = "N/A"

    return f"{formatted_date} {text}"


def fetch_threads_posts(
    username: str,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Fetch posts from a Threads user using Selenium.

    Args:
        username: Threads username to scrape
        limit: Maximum number of posts to retrieve

    Returns:
        List of post dictionaries with text and created_at
    """

    posts = []
    url = f"https://www.threads.net/@{username}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = None

    try:
        print(f"Setting up driver for ARM64...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        print(f"Loading {url}...")
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )
        except:
            print("Warning: Timeout waiting for articles to load")

        for i in range(3):
            print(f"Scrolling... ({i + 1}/3)")
            driver.execute_script("window.scrollBy(0, window.innerHeight)")
            time.sleep(1.5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article')

        print(f"Found {len(articles)} articles on page")

        if len(articles) == 0:
            print("\nDebug Info:")
            print(f"Page title: {soup.title}")

            divs = soup.find_all('div')
            print(f"Total divs on page: {len(divs)}")

            alt_posts = soup.find_all(['div', 'section'], {'role': 'article'})
            print(f"Found {len(alt_posts)} elements with role='article'")

            body_text = soup.get_text()[:200]
            print(f"Page text preview: {body_text}")

            post_divs = soup.find_all(
                'div',
                class_=lambda x: x and ('post' in x.lower() or 'thread' in x.lower())
            )
            print(f"Found {len(post_divs)} divs with 'post' or 'thread' in class")

        for article in articles:
            if len(posts) >= limit:
                break

            try:
                text_el = article.find(['div'], {'data-testid': 'post'})

                if not text_el:
                    text_el = article.find(['div', 'span'])

                text = text_el.get_text(strip=True)[:500] if text_el else ""

                time_el = article.find('time')
                created_at = time_el.get('datetime', '') if time_el else ""

                if text:
                    posts.append({
                        'text': text,
                        'created_at': created_at
                    })

                    print(f"✓ Post {len(posts)} extracted")

            except Exception as e:
                print(f"Warning: Error parsing article: {e}")
                continue

        print(f"Successfully extracted {len(posts)} posts")

    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

    return posts


def scrape_and_export(
    username: str,
    output_filename: str,
    limit: int = 10,
) -> None:
    """
    Scrape Threads posts from a user and export to a text file.

    Args:
        username: Threads username to scrape
        output_filename: Output text file name
        limit: Number of posts to retrieve
    """

    print(f"Scraping Threads for @{username}...")

    try:
        posts = fetch_threads_posts(username=username, limit=limit)

        if not posts:
            print(f"No posts found for @{username}")
            return

        with open(output_filename, 'w', encoding='utf-8') as f:
            for post in posts:
                f.write(format_post_data(post))
                f.write("\n\n")

        print(f"✓ Successfully exported {len(posts)} posts to {output_filename}")

    except Exception as e:
        print(f"Error scraping @{username}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_username = sys.argv[1]
    else:
        usernames = load_threads_usernames()

        if not usernames:
            print("No usernames found in threads_usernames_verified.txt")
            sys.exit(1)

        target_username = usernames[0]

    output_file = f"threads_posts_{target_username}.txt"

    print(f"\n{'=' * 80}")
    print(f"Instagram Threads Scraper - Post Exporter")
    print(f"{'=' * 80}")
    print(f"Target username: @{target_username}")
    print(f"Posts to fetch: 10")
    print(f"Output file: {output_file}")
    print(f"{'=' * 80}\n")

    scrape_and_export(
        username=target_username,
        output_filename=output_file,
        limit=10,
    )

    print(f"\n✓ Done! Check {output_file} for results.")
