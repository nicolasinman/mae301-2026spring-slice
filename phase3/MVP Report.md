# 
# Executive Summary
Problem: With the rise of social media, many social media platforms have taken on an increasing role in macroeconomics. Influential political and social media figures routinely post on the internet and whether or not those posts correlate with subsequent market movement is a question that retail investors have no practical way to answer. There are too many accounts to follow, too many posts to read, and no systematic way to distinguish a post that is genuinely market-relevant from one that is just noise. Even when a retail investor does encounter a relevant post, evaluating whether that person's past statements have actually predicted market behavior requires historical data and quantitative analysis that most individuals do not have the tools or training to perform 

Solution: This project delivers an automated pipeline which scrapes data from influential accounts across major platforms such as X and Threads. The system then runs multi-layer language processing on every post to extract sentiment features, aligns those features with real market data, and applies a linear regression to determine whether a given person's market-related statements correlate with actual market movement. The final output presents this correlation in plain English, giving a retail investor a clear, data-backed answer to the whether a post is worth paying attention to. 

#
# User & Use Case
User: The target user is someone who manages their own portfolio, follows financial news and political commentary casually across social media, and is aware that the statements of prominent media figures can potentially guess or influence market sentiment. 

Usage case: A user wants to evaluate whether a political commentator's statements about the S&P 500 are worth acting on. They run SLICE against that person's X account, specifying a start date to define a historical window. The scraper collects all posts since that date and saves them as a dated text file. It then analyzes the text file, in a separate program, as chunks and converts those chunks into data points where it measures various attributes using AI language processing. Then it retrieves the S&P 500 direction for each corresponding date from a market data file, and computes the relationship between what the person said and what the market did. 

#
# System Design

#
# Data

