# Cohort Anomalies 

# Project Description
Identify anomalies and metrics in student access to the Codeup Curriculum

 
# Project Goal
 
* Identify: 
    * which lesson appears to attract the most traffic consistently across cohorts (per program).
    * which lessons are covered significantly more than other cohorts and which are glossed over.
    * if there are students who, when active, hardly access the curriculum and gather the relevant data on them. 
    * any suspicious activity such as web-scraping and suspicious IP access and users and/or machines accessing the curriculum who shouldn’t be. 
    * topics that Codeup grads continue to reference after graduation and into their jobs (for each program).
    * any other anomalies. 

 
# Initial Thoughts
 
The largest cohort will have the most diverse log activity. 
 
# The Plan
 
* Acquire data:
    * Download the anonymized-curriclum-access.txt file from the company email
    * Get the curriculum_logs data from the Codeup SQL server 
    * Convert to a single dataframe
 
* Prepare data:
   * Look at the data:
		* nulls
		* value counts
        * distribution of values
		* data types
		* numerical/categorical columns
		* names of columns
 
* Explore/Analyze data:
   * Answer the following questions:
        1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
        2. Which lessons are covered significantly more than other cohorts and which are glossed over?
        3. If there are students who, when active, hardly access the curriculum and gather the relevant data on them? 
        4. If there is any suspicious activity such as web-scraping and suspicious IP access and users and/or machines accessing the curriculum who shouldn’t be? 
        5. What topics that Codeup grads continue to reference after graduation and into their jobs (for each program)?
        6. If there are any other anomalies. 
       
* Conclusions:
	* Identify anomalies and analyze Codeup metrics
     

# Data Dictionary

| Feature | Definition (measurement)|
|:--------|:-----------|
|App Name| Name of the app|
|App Id| app id|
|Category| Category the app is in (selected by creator)| 
|Rating| Quality rating given by users out of max score of 5| 
|Rating Count| Total count of the user rating| 
|Installs| Total number of installs the app has| 
|Minimum Installs| the minimum installs the app has|
|Maximum Installs| the maximum installs the app has| 
|Free| If the app is free or not|
|Price| The price of the app|
|Currency| The currency of the cost of the app|
|Size| Size of the app in kb|
|Minimum Android| The minimum Android OS needed to run the app|
|Developer Website| The website address for the developer|
|Developer Email| The Email address of the developer|
|Released| The date the app was released| 
|Privacy Policy| The link to the Privacy Policy|
|Last Updated| The date of the app’s last update|
|Content Rating| The content rating of the app|
|Ad Supported| If the app has built in ads|
|In app purchases| If the app has in app purchases| 
|Editor Choice| If the app has an editor choice award|
|Viral| If the app has 1 million or more downloads (Target Variable)|


# Steps to Reproduce
1) 
2)  
3) 
4) Run notebook
 
# Takeaways and Conclusions<br>



# Recommendation
 


