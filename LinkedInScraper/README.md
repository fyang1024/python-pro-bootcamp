### Quick Start

Because LinkedIn requires user login to do any search, you need to set up two environment variables before running this program
1. LINKEDIN_USER
2. LINKEDIN_PASS

On Windows, they can set in System Environment.
See https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/

On MacOS or Linux, you can run the following command in a terminal:
```shell
export LINKEDIN_USER=your_linkedin_user_account
export LINKEDIN_PASS=your_linkedin_password
```

Once the environment variables are set up, you can run the program as below
```shell
python main.py 'head of people, head of hr' 11
```
The program will use "head of people" and "head of hr" as keywords and for each keyword it will scrape 11 search results and export the data into a CSV file people.csv
The columns of the CSV are:
* location
* company
* name
* title
* about

