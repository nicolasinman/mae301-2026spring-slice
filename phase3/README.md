# PLEASE READ

## Scraper Overview

Within the Phase 3 folder, there are two scrapers: one for extracting posts from X (formerly twitter), and the other for Meta Threads. While continuing research on methods of extraction from these social media platforms, the team found that completing a fully competent MVP with real-world live data would not be possible because of the restrictions that have been put in place on social media data acquisition. With proper funding, a completed MVP is possible; however, for the purposes of this project, the team determined that a proof-of-concept would suffice.

- ### Scraper Program Procedure
  The current program that was created and placed in the GitHub repository for scraping X posts makes use of an older Twitter scraper that worked before Twitter became X and began requiring a paid  subscription for API access. Due to this API restriction, the program cannot extract data from X and serves solely as a proof-of-concept. Similarly to the X scraper program, the Instagram Threads scraper is limited in its access to the Threads API; however, this program is a more in-depth look at what a successful model would actually accomplish. The Threads program is fully capable of navigating to the URL where the required information would be extracted; however, it cannot extract the data without the proper API access. Thus, the following information is purely descriptive of the program procedure and the results that would be achieved if the team were given API tools from these social media platforms.

  <ins>**Step 1:**</ins> User runs script with python threads_scraper.py ThreadsUsername

  <ins>**Step 2:**</ins> Program opens Threads account and examines the last "X" # of posts by this individual. (NOTE: Only extracts text)

  <ins>**Step 3:**</ins> The program outputs the post text and post creation date into a .txt with the name "threads_posts_ThreadsUsername.txt". The following is the format of the output .txt:

  ```txt
  04/24/2026 Example Threads post text here

  04/23/2026 Another example Threads post text here
  ```
 
  <ins>**Step 4:**</ins> From here, the .txt can be parsed in a separate program and used for analysis and correlation with stock market data.

  <ins>**Future Modifications:**</ins> Rather than the individual manually entering the names of each individual, a matrix of influential individuals formatted in a .txt document (like the one shown in the Phase 3 folder) could be read by the program and outputted to multiple .txt files with the exact same structure as before.

- ### Scraper Requirements
  - **X Scraper**
    - Programming Language: Python
    - Libraries: twint
  - **Instagram Threads Scraper**
    - Programming Language: Python
    - Libraries: selenium, beautifulsoup4, webdriver-manager

## Example data 
Contains manufactured tweets from imaginary people which is written specifically to be good data for our program.

<ins>Ex.</ins>
- Person1 can accurately predict when stocks will rise/fall

- Person2 is always perfectly wrong in their predictions

- Person3 is randomly correct/incorrect

<ins>Ex.</ins> 

- Person1 tweet: "xx/yy/20zz S&P500 is totally gonna go up"

Certain tweets from example people will be unrelated to S&P500, e.g. "I got a cat today". This will demonstrate our ability to filter by keywords.


## Text Analysis Overview

Text analysis is called in the terminal using : python textanalysisfinal.py yourtextfilename.txt

It analyzes the text file as chunks and converts them into data points measuring various attributes using AI to accuratly read and interperet.

Currently, only keywords and sentiment score are used to calculate final result.

Depending on how the data compares to a reference market_data.csv file, it outputs a judgment on whether or not the selected user is a reliable indicator of the S&P500.

- ### Analysis Requirements
    - Programming Language: Python
    - Libraries: numpy, nltk, transformers, textblob, torch
