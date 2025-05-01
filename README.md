<p><small>Best View in <a href="https://github.com/settings/appearance">Light Mode</a> and Desktop Site (Recommended)</small></p><br/>

![AI-Resume-Analyzer](https://i.imgur.com/6E9Fjy5.png)

<div align="center">
  <h1>🌴 AI RESUME ANALYZER 🌴</h1>
  <p>A Tool for Resume Analysis, Predictions and Recommendations</p>
  <!-- Badges -->
  
  <!--links-->
  <h4>
    <a href="#preview-">View Demo</a>
    <span> · </span>
    <a href="#setup--installation-">Installation</a>
    <span> · </span>
  </h4>
  <p>
    <small align="justify">
      Built with 🤍 by Shivendra Kumar Patel
</div><br/><br/>

## About the Project 🥱
<div align="center">
    <br/><img src="https://i.imgur.com/6E9Fjy5.png" alt="screenshot" /><br/><br/>
    <p align="justify"> 
      A tool which parses information from a resume using natural language processing and finds the keywords, cluster them onto sectors based on their keywords. 
      And lastly show recommendations, predictions, analytics to the applicant / recruiter based on keyword matching.
    </p>
</div>

## Scope 😲
i. It can be used for getting all the resume data into a structured tabular format and csv as well, so that the organization can use those data for analytics purposes

ii. By providing recommendations, predictions and overall score user can improve their resume and can keep on testing it on our tool

iii. And it can increase more traffic to our tool because of user section

iv. It can be used by colleges to get insight of students and their resume before placements

v. Also, to get analytics for roles which users are mostly looking for

vi. To improve this tool by getting feedbacks

<!-- TechStack -->
## Tech Stack 🍻
<details>
  <summary>Frontend</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Learn/HTML">HTML</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Web/CSS">CSS</a></li>
    <li><a href="https://developer.mozilla.org/en-US/docs/Learn/JavaScript">JavaScript</a></li>
  </ul>
</details>

<details>
  <summary>Backend</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
    <li><a href="https://www.python.org/">Python</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://www.mysql.com/">MySQL</a></li>
  </ul>
</details>

<details>
<summary>Modules</summary>
  <ul>
    <li><a href="https://pandas.pydata.org/">pandas</a></li>
    <li><a href="https://github.com/OmkarPathak/pyresparser">pyresparser</a></li>
    <li><a href="https://pypi.org/project/pdfminer3/">pdfminer3</a></li>
    <li><a href="https://plotly.com/">Plotly</a></li>
    <li><a href="https://www.nltk.org/">NLTK</a></li>
  </ul>
</details>

<!-- Features -->
## Features 🤦‍♂️
### Client: -
- Fetching Location and Miscellaneous Data

  Using Parsing Techniques to fetch
- Basic Info
- Skills
- Keywords

Using logical programs, it will recommend
- Skills that can be added
- Predicted job role
- Course and certificates
- Resume tips and ideas
- Overall Score
- Interview & Resume tip videos

### Admin: -
- Get all applicant’s data into tabular format
- Download user’s data into csv file
- View all saved uploaded pdf in Uploaded Resume folder
- Get user feedback and ratings
  
  Pie Charts for: -
- Ratings
- Predicted field / roles
- Experience level
- Resume score
- User count
- City
- State
- Country

### Feedback: -
- Form filling
- Rating from 1 – 5
- Show overall ratings pie chart
- Past user comments history 

## Requirements 😅
### Have these things installed to make your process smooth 
1) Python (3.9.12) https://www.python.org/downloads/release/python-3912/
2) MySQL https://www.mysql.com/downloads/
3) Visual Studio Code **(Prefered Code Editor)** https://code.visualstudio.com/Download
4) Visual Studio build tools for C++ https://aka.ms/vs/17/release/vs_BuildTools.exe

## Setup & Installation 👀

To run this project, perform the following tasks 😨
Step 1: Clone the Repository

Clone the AI Resume Analyzer repository to your local machine:

```bash

git clone https://github.com/your-username/AI-Resume-Analyzer.git

cd AI-Resume-Analyzer
```
Replace your-username with your GitHub username.

Step 2: Set Up a Virtual Environment

Create and activate a Python virtual environment to manage dependencies:

```bash
python -m venv venvapp

.\venvapp\Scripts\activate  # On Windows
source venvapp/bin/activate  # On macOS/Linux

```

Step 3: Install Dependencies

Ensure pip is up-to-date:

```bash

python -m pip install --upgrade pip

```

Clear the cache to avoid corrupted downloads:

```bash

pip cache purge

```

Install the required Python packages listed in requirements.txt:

```bash

cd App

pip install -r requirements.txt

```

Step 4: Install spaCy Language Model

The project uses spaCy’s en_core_web_sm model for resume parsing. Install it:

```bash

python -m spacy download en_core_web_sm

```

Step 5: Configure MySQL Database

1. Start MySQL Server:

  - Ensure MySQL is installed and running. Download it from mysql.com if needed.
  - Start the MySQL server using your preferred method (e.g., mysql.server start on macOS or via the MySQL Workbench on Windows).

2. Set Up Database:

  - Log in to MySQL as the root user:
   ```bash
  
     mysql -u root -p

   ```
   Enter your MySQL root password (default is Shiv@2004 in the project; update App.py if different).


  - Create the database:
   ```sql

    CREATE DATABASE mydb;

   ```

  - Exit MySQL:
   ```sql

    EXIT;

   ```

3. Update MySQL Credentials (if needed):

 - Open ```App.py``` and verify the MySQL connection settings:
  ```python

   connection = pymysql.connect(host='localhost', user='root', password='Shiv@2004', db='mydb')

  ```

 - If your MySQL password differs, update the ```password``` field or use an environment variable:
   
  ```python
   import os
   connection = pymysql.connect(host='localhost', user='root', password=os.getenv('MYSQL_PASSWORD'), db='mydb')

  ```

  Set the environment variable:
  ```bash

   export MYSQL_PASSWORD='your_password'  # On macOS/Linux
   set MYSQL_PASSWORD=your_password      # On Windows

  ```

Step 6: Set Up Project Folders

Create the required directories for storing uploaded resumes and logo images:
  ```bash

   mkdir Uploaded_Resumes
   mkdir Logo

  ```
  I will already provides this dir. do not create it.

Place the following image files in the ```Logo``` directory:

  - RESUM.png: The main logo image.
  - recommend.png: The favicon image.

You can download these from the repository’s Logo folder or provide your own images with the same names.

Step 7: Download NLTK Data

The project uses NLTK for text processing. Download the required NLTK data:
  ```bash

   python -c "import nltk; nltk.download('stopwords')"

  ```

## After change all settings

Go to ```venvapp\Lib\site-packages\pyresparser``` folder

And replace the ```resume_parser.py``` with ```resume_parser.py``` 

which was provided by me inside ```pyresparser``` folder

``Congratulations 🥳😱 your set-up 👆 and installation is finished 😵🤯``

I hope that your ``venvapp`` is activated and working directory is inside ``App``

Step 8: Run the Application

Start the Streamlit application:
  ```bash

   cd App  # ("If the directory already exists, do not execute this command.")
   streamlit run App.py

  ```
  - Open your browser and navigate to http://localhost:8501 to access the app.
  - Note: Ensure the MySQL server is running before starting the app.

Step 9: Test the Application

  1. Sign Up:
  
  - Create an account with a valid password ( at least 6 characters, including 1 uppercase, 1 lowercase, and 1 special character like ```!@#$%^&*```).

  2. Log In:
  
  - Log in with your credentials or use the admin account:
    - Username: ```admin```
    - Password: ```admin@resume-analyzer```

  3. Upload a Resume:
  
  - In the “User” section, enter your name, email, and mobile number, then upload a PDF resume.
  - The app will analyze the resume and display recommendations.

Troubleshooting

- MySQL Connection Error:

  - Verify MySQL is running and credentials in App.py match your setup.
  - Test connectivity:

  ```bash

    python -c "import pymysql; conn = pymysql.connect(host='localhost', user='root', password='Shiv@2004', db='mydb'); print('Connected')"

  ```

- Missing ```en_core_web_sm```:

  - Reinstall the spaCy model:

  ```bash

    python -m spacy download en_core_web_sm

  ```

- Dependency Issues:
  - Ensure Python 3.8 is used:
  
  ```bash

    python --version

  ```

  - Reinstall dependencies:

  ```bash
  
    pip install -r requirements.txt

  ```


- Missing Logo Images:

  - Confirm RESUM.png and recommend.png are in the Logo folder. If missing, create placeholder images or contact the repository owner.

- Empty Admin Charts:

  - The admin section requires data in the user_data table. Upload a resume in the “User” section first.

Notes: 

- The project is licensed under the MIT License.
- For production, secure sensitive data (e.g., MySQL password) using environment variables.
- If you encounter issues, check the Issues section or open a new issue.


## Known Error 🤪
If ``GeocoderUnavailable`` error comes up then just check your internet connection and network speed

## Issue While Installation and Set-up 🤧
Check-out installation [Video](https://youtu.be/WFruijLC1Nc)

Feel Free to <a href="mailto:shivendrap455@gmail.com?subject=I%20have%20an%20issue%20while%20setup%2Finstalling%20of%20AI%20RESUME%20ANALYZER&body=Name%3A%20-%0D%0A%0D%0ADesignation%3A%20-%0D%0A%0D%0APlease%20describe%20your%20problem%20in%20brief%20with%20attached%20photos%20of%20error">Send mail</a>  

## Usage
- After the setup it will do stuff's automatically
- You just need to upload a resume and see it's magic
- Try first with my resume uploaded in ``Uploaded_Resumes`` folder
- Admin userid is ``admin`` and password is ``admin@resume-analyzer``

<!-- Roadmap -->
## Roadmap 🛵
* [x] Predict user experience level.
* [x] Add resume scoring criteria for skills and projects.
* [x] Added fields and recommendations for web, android, ios, data science.
* [ ] Add more fields for other roles, and its recommendations respectively. 
* [x] Fetch more details from users resume.
* [ ] View individual user details.

## Contributing 🤘
Pull requests are welcome. 

For major changes, please open an issue first to discuss what you would like to change.

I've attached the <a href="https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/AI%20RESUME%20ANALYSER%20SYNOPSIS.pdf">synopsis</a> of the project

If you want the full report of project
<a href="mailto:shivendrap455@gmail.com?subject=Request%20for%20AI-RESUME-ANALYZER%20Project%20Report%20(2022-23)&body=Hi%2C%0D%0A%0D%0AI%20would%20like%20to%20request%20the%20project%20report%20for%20AI-RESUME-ANALYZER.%0D%0AHere%20are%20my%20details%3A%0D%0A%0D%0AFull%20Name%3A%20%0D%0ACollege/Organization%3A%20%0D%0AGitHub%20Profile%20Link%3A%20%0D%0AHow%20I%20found%20this%20project%3A%20%0D%0APurpose%20for%20requesting%20the%20report%3A%20%0D%0A%0D%0AThank%20you!">📩 Request Project Report</a> – <strong>It's Free!</strong>


## License
This project is licensed under the [MIT License](LICENSE.md).

## Preview 👽

### Client Side

**Main Screen**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/user/1-Main%20Screen.png?raw=true)

**Resume Analysis**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/user/2-Analysis.png?raw=true)

**Skill Recommendation And Tips**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/user/3-%20Recom-Tips.png?raw=true)

**Course Recommendation If needed**

![Screenshot](https://github.com/deepakpadhi986/AI-Resume-Analyzer/blob/main/screenshots/user/4-recom.png?raw=true)

**Resume Score**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/user/4-%20Resume%20Score.png?raw=true)

**Video Recommendation**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/user/5-%20Recom.png?raw=true)

### Feedback

**Feedback Form**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/feedback/1-%20From.png?raw=true)

**Overall Rating Analysis and Comment History**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/feedback/2%20-%20Analytics.png?raw=true)

### Admin

**Login**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/1-%20Main%20Screen.png?raw=true)

**User Count and it's data**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/2%20-%20User%20Data.png?raw=true)

**Exported csv file**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/4-%20Feed%20Data.png?raw=true)

**Feedback Data**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/4-%20Feed%20Data.png?raw=true)

**Pie Chart Analytical Representation of clusters**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/5-%20Pie%20exp..png?raw=true)

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/6-%20Pie%20score.png?raw=true)

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/7-%20Pie%20Location.png?raw=true)

## Signup Page
**Main page**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/Signup%20Page/Main%20Page.png?raw=true)

## Login Page
**Main page**

![Screenshot](https://github.com/shivendra9203/AI-Resume-Analyzer/blob/main/screenshots/admin/5-%20Pie%20exp..png?raw=true)


### Built with 🤍 AI RESUME ANALYZER by Shivendra Kumar Patel
