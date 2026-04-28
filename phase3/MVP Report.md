# 
# Executive Summary
Problem: With the rise of social media, many social media platforms have taken on an increasing role in macroeconomics. Influential political and social media figures routinely post on the internet and whether or not those posts correlate with subsequent market movement is a question that retail investors have no practical way to answer. There are too many accounts to follow, too many posts to read, and no systematic way to distinguish a post that is genuinely market-relevant from one that is just noise. Even when a retail investor does encounter a relevant post, evaluating whether that person's past statements have actually predicted market behavior requires historical data and quantitative analysis that most individuals do not have the tools or training to perform 

Solution: This project delivers an automated pipeline which scrapes data from influential accounts across major platforms such as X and Threads. The system then runs multi-layer language processing on every post to extract sentiment features, aligns those features with market data, and applies a linear regression to determine whether a given person's market-related statements correlate with  market movement. The final output presents this correlation in plain English, giving a retail investor a clear, data-backed answer to the whether or not a post is worth paying attention to. 

#
# User & Use Case
User: The target user is someone who manages their own portfolio, follows financial news and political commentary casually across social media, and is aware that the statements of prominent media figures can potentially guess or influence market sentiment. 

Usage case: A user wants to evaluate whether a political commentator's statements about the S&P 500 are worth acting on. They run SLICE against that person's X account, specifying a start date to define a historical window. The scraper collects all posts since that date and saves them as a dated text file. It then analyzes the text file, in a separate program, as chunks and converts those chunks into data points where it measures various attributes using AI language processing. Then it retrieves the S&P 500 direction for each corresponding date from a market data file, and computes the relationship between what the person said and what the market did. 

#
# System Design

#
# Data
Sources: Currently there are two sources of data that can be utilized. Post data from either X or Threads can be collected. Market data comes from a structured file containing daily S&P 500 direction labels keyed by date.m

Size: The system is designed to operate on post histories spanning weeks to months per individual, paired with a corresponding window of daily market data. In practice, a meaningful collection of data would consist of hundreds of dated posts per tracked account. The size of the post data varies significantly based on the posting frequency of a particular account and the duration of the collection window. However, even an account that posts frequently over a six-month period would generate a flat text file that remains manageable and well within the processing capabilities of the existing system. The primary limitation regarding the size of the collected data is not related to storage or computational power; rather, it is determined by the availability of dated post history that can be accessed through the platform. This availability is influenced by API rate limits, platform-specific restrictions, and the extent of public post archives on each platform. 

Cleaning: Text that is conventionally structured should prove no issue for the current pipeline. However, posts from X or Threads can possibly contain URLs that inflate word counts, mentions that attach to adjacent words and break tokenization, hashtags that merge multiple words into a single unrecognizable token, and abbreviations or political shorthand that do not appear in the tool used for deciding the emotions charge of a word and are therefore missed in the emotional word count. A preprocessing step would need to be added to the pipeline before it is applied to raw scraped data at any meaningful scale. 

Splits: The system performs correlation analysis rather than training a predictive model, so no train/test split is applied. The regression is computed over all available matched data points. 

#
# Models
The system used several pre-trained, specialized models and workflow strategies to provide
comprehensive analysis of social media post. Some of the pre-trained models used include Vader,
TextBlob, and distilBert. These are to analyze social media, extract noun phrases and binary
sentiment classification. The supervised statistical models used include least squares regression
line and mathematical modeling; these include finding the relationship between the sentiment
score and the S&amp;P 500 market directions and to determine if a person is reliable “predictor” for
said market movement. The workflow and its strategies were designed through a multi-
dimensional approach; first using Lexical Density to count specific “emotional” words via Vader,
Contextual Sentiment to understand the polarity/confidence of the statement by DistilBert, and
Keyword Filtering to filter for “S&amp;P500” relevance before the data is inputted into the matrix
(via TextBlob). There was very few fine-tuning performed as the model uses an already fined-
tuned of SST-2. For prompting, the system did not use Generative AI prompting, but rather
programmatic parsing.

#
# Evaluation
In evaluating this system, for its quantitative metrics it evaluates the influencer’s signal
effectiveness using standard statistical measures derived from text sentiment and market
direction correlation. This is accomplished through find the coefficient of determination
measuring the how much variance in the S&amp;P500 direction can be explained by the influencer. If
a strong relationship, given a score &gt;0.7, if weak, &lt;0.3. Then it finds the correlation coefficient to
find the strength and direction of the linear relationship; positive slope equals the person being a
“leading indicator” and vise versa for a negative slope. Thirdly, the system uses lexical density to
filter out posts that lack actionable importance. Possible errors analyzed includes any sarcasm
and slang which DistilBert and Vader can misinterpret and contextual blindness in which a post
can have a neutral score while containing high-impact views.

#
# Limitations &amp; Risks

Some of the biggest failure modes include an inability to recognize slang/sarcasm; models like
SST-2 trained on movie reviews may interpret negative phrases as positive based on their
structure. Financial markets also tend to react the most to neutral-toned data; if the system is to
look at the creditability of the data through its positive and negative tone, it may leave out critical
data. Beyond the nature of the market, influencers may post passed 5:00pm in which the market
has closed. Some biases of this model include the general-purpose nature of DistilBERT and
Vader overlooking critical financial twitter post from nuances. Having small samples sizes can
encourage confirmation bias by “finding” great predictors through statistical coincidence. Some
data issues include unrelated influencer posts like “Memes and lunch posts” will inevitably leak
the data matrix which can dilute the correlation. X and Threads also have constrictions when
extracting APIs which can prevent the model from learning the “noise” of social media posts.
Some privacy and ethical concerns include automated scraping can violate platform TOS, the
idea of a tool encouraging reactive trading can influence the market.

#
# Next Steps
If the team were to have two to three more months to further develop this model, the first action
would be to replace the basic DistilBERT with the much more sophisticated FinBERT that is
more in line with financial corpora. Next, implementing a Time-Lagged Cross-Correlation
function in the analysis to better turn the model into a predictive tool. It would also be prudent to
add a “weight” variable to differentiate the creditability/importance of posts. For the “physical”
or viewable aspect of the model, visible graphs like scatter plots and heatmaps can show the user
the sentiment vs. price change and what influencers have the highest r^2 values. Having
transparent data will allow the user to fact check the model’s predictions and therefore increase
user trust.

