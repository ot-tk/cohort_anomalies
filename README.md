# Cohort Anomalies

## Project Description

Identify anomalies and metrics in student access to the Codeup Curriculum

## Project Goal

Identify:

* most and least popular lessons
* less active students
* suspicious activity
* frequently referenced topics

## Initial Thoughts

The program with the most cohorts will have the most diverse log activity.

## The Plan

* Acquire data from Codeup MySQL DB
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
    2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
    3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
    4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
    5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
    6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
    7. Which lessons are least accessed?
    8. Are there any other anomalies?
* Conclusions:
  * Identify anomalies and analyze Codeup metrics

## Data Dictionary

| Feature          | Definition (measurement)                                   |
| :--------------- | :--------------------------------------------------------- |
| datetime (index) | date and time of user access to the Codeup Curriculum      |
| path             | The path to the curriculum                                 |
| user_id          | ID for the user accessing the curriculum                   |
| cohort_id        | Quality rating given by users out of max score of 5        |
| ip               | IP address at the time of access                           |
| name             | Name of the Cohort                                         |
| start_date       | Start date of the Cohort                                   |
| end_date         | End date of the Cohort                                     |
| program_id       | ID of the Codeup program (i.e. WebDev, Data Science, etc.) |

## Steps to Reproduce

1) Clone this repo
2) If you have access to the Codeup MySQL DB:
   * Save **env.py** in the repo w/ `user`, `password`, and `host` variables
   * Run notebook
3) If you don't have access:
   * Request access from Codeup
   * Do step 2

## Key Findings and Conclusions

- All time most referenced lesson per Program:
    - **Web Dev**: Javascript-I – Intro – Working with Data Types, Operators, and Variables
    - **Data Science**: Classification – Overview (referenced mostly by Darden Cohort)
- Top 3 referenced topics per Program after graduation:
    - **Web Dev**: Spring, Javascript-I, and HTML-CSS
    - **Data Science**: SQL, Fundamentals, and Classification
- There were some students who accessed the curriculum less often than there were days in the program they were in. Most were from web dev, in cohorts Oberon, Neptune, and Sequoia. It is possible that some of these students were not able to finish the course and dropped out.
- Before the cross-curriculum access was shut off, there were some students accessing the curriculum of both programs. After the shut off, it seemed that of the few students that were trying to access another program's curriculum, most were web dev students.


### Recommendations and Next Steps

* We should send out an alumni survey to ascertain if the frequently searched for topics on the Codeup site were thoroughly covered during their course and take appropriate action. Additionally, any overlap in currently covered topics and searched for topics should be specifically emphasized as soon as possible. 
