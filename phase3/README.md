# PLEASE READ!!!

MVP is meant to scrape data from twitter, then convert and analyze into usable information.
HOWEVER, actively running a scraper costs a subscription fee.
Therefore - to test the program, we will have 2 data sets: exampledata, sampledata

### Example data 
will contain manufactured tweets from imaginary people which is written specifically to be good data for our program.

Ex. 
person1 can accuratly predict when stocks will rise/fall

person2 is always perfectly wrong in their predictions

person3 is randomly correct/incorrect


Ex. person1 tweet: "xx/yy/20zz S&P500 is totally gonna go up"

Certain tweets from example people will be unrelated to S&P500, eg "I got a cat today". This will demonstrate our ability to filter by keywords.

### Sample data (optional)
will contain a couple sets of real tweets manually copied from twitter for true testing




## Scraper Overview

Within the Phase 3 folder, there are two scrapers: one for extracting posts from X (formerly twitter), and the other for Meta Threads. While continuing research on methods of extraction from these social media platforms, the team found that completing a fully competent MVP with real-world live data would not be possible because of the restrictions that have been put in place on social media data acquisition. With proper funding, a completed MVP is possible; however, for the purposes of this project, the team determined that a proof-of-concept would suffice.

- ### Scraper Program Procedure
  The current program that was created and placed in the GitHub repository for scraping X posts makes use of an older Twitter scraper that worked before Twitter became X and began requiring a paid  subscription for API access. Due to this API restriction, the program cannot extract data from X and serves solely as a prove-of-concept. Similarly to the X scraper program, the Instagram Threads scraper is limited in its access to the Threads API; however, this program is a more in-depth look at what a successful model would actually accomplish. The Threads program is fully capable of naviagting to the URL where the required information would be extracted; however, it cannot extract the data without the proper API access. Thus, the following information is purely descriptive of the program procedure and the results that would be achieved if the team were given API tools from these social media platforms.

  Step 1: User runs script with python threads_scraper.py ThreadsUsername

  Step 2: Program opens Threads account and examines the last "X" # of posts by this individual. (NOTE: Only extracts text)

  Step 3: The program outputs the post text and post creation date into a .txt with the name "threads_posts_ThreadsUsername.txt". The following is the format of the output .txt:

  ```txt
  04/24/2026 Example Threads post text here

  04/23/2026 Another example Threads post text here
  ```
 
  Step 4: From here, the .txt can be parsed in a separate program and used for analysis and correlation with stock market data.

  Future Modifications: Rather than the individual manually entering the names of each individual, a matrix of influential individuals formated in a .txt document could be read by the program and outputted to a .txt with the exact same structure as before.
