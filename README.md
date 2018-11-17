# Kickstarter Idea Evaluator
Machine Learning project which aims to predict the success of Kickstarter project ideas.

This project was created for the _EECS 349: Machine Learning_ class at Northwestern University during Fall 2018.

## Task
Our machine learning task will mainly involve predicting the success of a Kickstarter project based on the content of the project and metadata. Secondary objectives could be predicting whether a project will go viral (become extremely popular as opposed to just meeting the objective), or predicting a ballpark estimate of the amount of funding received.

This task is interesting because a platform like Kickstarter is user-dominated and allows for a symbiotic relationship among its users. The projects are typically original ideas and the funding is driven directly by the end-users of the products. Therefore, it is interesting to see how the content of a Kickstarter project interacts with the users on the platform and on the web, because the project itself is responsible for driving results - there’s no corporate branding, marketing initiatives, etc. In addition, Kickstarter as an organization relies on its users, both on the buy and sell side, for its own company’s health, therefore investigating the interaction between users also has value for Kickstarter, not just the users.

Finally, in accordance with studies on the virality of memes, fake news, and other fast-spreading content, it will be interesting to explore how Kickstarter projects become viral. Unlike other internet content, which is generally free, Kickstarter projects that are significantly over-funded carry with them an economic vote - the people who choose to back them with their money. Viral Kickstarter projects therefore offer willingness to pay as another quantifiable measurement.

## Data Acquisition
The data we will be working with is readily available in .csv and .json files on Kaggle and [Web Robots](https://webrobots.io/kickstarter-datasets/). The Kaggle dataset includes metadata for over 300,000 campaigns launched between 2010 and 2016. Web Robots includes data up to October of the current year, backlogged through April of 2014. The Web Robots data set includes URLs pointing to images featured on a Kickstarter project, so we can scrape these URLs if we wish to acquire images to go along with the rest of the project features.

## Features and Attributes
Our data sets are pre-labeled with many attributes, some more interesting than others. We believe the more useful of these include the name of the project and the short description listed on Kickstarter’s website, launch date and funding deadline of a project, as well as the funding goal in USD and the amount of the goal pledged upon reaching the funding deadline. Other potentially useful attributes may be how many people backed a given project, and what category the project is listed under. If a project creator posted an image to the project page, we may also decide to process the image to extract information about the content of the image.

## Plan of Attack
We plan on first preprocessing the data and creating new attributes based on the metadata. For example, we plan on implementing NLP techniques to parse the titles/blurbs for each campaign (potentially sentiment analysis). We also plan on creating attributes to encode the supply/demand and competition characteristics within each project category. 

The initial ML algorithms we plan on using are Decision Trees (C4.5, RandomForest) and Nearest-neighbor. The highly categorical nature of the data makes Decision Trees an intuitive first choice. 

We will primarily use traditional cross-validation techniques to compare performance across our chosen ML algorithms.  Alternatively, we may train on data for older campaigns (2010 - 2017) and test on more recent data (2018) to evaluate any time-dependent changes to Kickstarter’s platform that may affect generalizability, especially regarding how useful historical trends are for predicting newer examples.

## Contributors
Michael Huyler, Mathias Newman, Ramish Zaidi, Zach Paitsel
