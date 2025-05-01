# Developed by Shiv  Made with Streamlit

###### Packages Used ######
import streamlit as st
import pandas as pd
import base64, random
import time, datetime
import pymysql
import os
import socket
import platform
import geocoder
import secrets
import io
import bcrypt
import re
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from pyresparser import ResumeParser
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import nltk
nltk.download('stopwords')

###### Preprocessing Functions ######

def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 👨‍🎓**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

###### Database Functions ######

# SQL connector
connection = pymysql.connect(host='localhost', user='root', password='Shiv@2004', db='mydb')
cursor = connection.cursor()

def create_users_table():
    table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT NOT NULL AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)
    );
    """
    cursor.execute(table_sql)
    connection.commit()

def insert_user(username, email, password, timestamp):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    insert_sql = "INSERT INTO users (username, email, password, created_at) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_sql, (username, email, hashed_password, timestamp))
    connection.commit()

def check_user_credentials(identifier, password):
    query = "SELECT username, password FROM users WHERE username = %s OR email = %s"
    cursor.execute(query, (identifier, identifier))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
        return result[0]  # Return username
    return None

def insert_data(sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country, act_name, act_mail, act_mob, name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses, pdf_name):
    DB_table_name = 'user_data'
    insert_sql = "INSERT INTO " + DB_table_name + """
    VALUES (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (str(sec_token), str(ip_add), host_name, dev_user, os_name_ver, str(latlong), city, state, country, act_name, act_mail, act_mob, name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills, courses, pdf_name)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def insertf_data(feed_name, feed_email, feed_score, comments, Timestamp):
    DBf_table_name = 'user_feedback'
    insertfeed_sql = "INSERT INTO " + DBf_table_name + """
    VALUES (0,%s,%s,%s,%s,%s)"""
    rec_values = (feed_name, feed_email, feed_score, comments, Timestamp)
    cursor.execute(insertfeed_sql, rec_values)
    connection.commit()

###### Page Configuration ######

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon='./Logo/recommend.png',
)

###### Main Application Logic ######

def signup_page():
    st.title("Sign Up")
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign Up")
        if submit:
            if not username or not email or not password:
                st.error("All fields are required.")
            else:
                # Password validation
                password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*])(?=.{6,})'
                if not re.match(password_pattern, password):
                    st.error("Password must be at least 6 characters long and contain at least 1 uppercase letter, 1 lowercase letter, and 1 special character (!@#$%^&*).")
                else:
                    try:
                        ts = time.time()
                        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
                        insert_user(username, email, password, timestamp)
                        st.success("Account created successfully! Please log in.")
                        st.session_state.page = "login"
                    except pymysql.err.IntegrityError:
                        st.error("Username or email already exists.")
    if st.button("Already have an account? Log In"):
        st.session_state.page = "login"

def login_page():
    st.title("Log In")
    with st.form("login_form"):
        identifier = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Log In")
        if submit:
            if not identifier or not password:
                st.error("All fields are required.")
            else:
                username = check_user_credentials(identifier, password)
                if username:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.page = "main"
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Invalid username/email or password.")
    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = "signup"
    if st.button("Forgot Password?"):
        st.warning("Please contact the admin at admin@resume-analyzer.com to reset your password.")

def main_app():
    img = Image.open('./Logo/RESUM.png')
    st.image(img)
    st.sidebar.markdown("# Choose Something...")
    ## link = '<a href="https://dnoobnerd.netlify.app" target="_blank">Developed by dnoobnerd</a>'
    ## st.sidebar.markdown(link, unsafe_allow_html=True)
    activities = ["User", "Feedback", "About", "Admin", "Logout"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

    if choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.success("Logged out successfully.")
        return

    # Create database and tables
    db_sql = """CREATE DATABASE IF NOT EXISTS mydb;"""
    cursor.execute(db_sql)

    DB_table_name = 'user_data'
    table_sql = """
    CREATE TABLE IF NOT EXISTS """ + DB_table_name + """
        (ID INT NOT NULL AUTO_INCREMENT,
        sec_token varchar(20) NOT NULL,
        ip_add varchar(50) NULL,
        host_name varchar(50) NULL,
        dev_user varchar(50) NULL,
        os_name_ver varchar(50) NULL,
        latlong varchar(50) NULL,
        city varchar(50) NULL,
        state varchar(50) NULL,
        country varchar(50) NULL,
        act_name varchar(50) NOT NULL,
        act_mail varchar(50) NOT NULL,
        act_mob varchar(20) NOT NULL,
        Name varchar(500) NOT NULL,
        Email_ID VARCHAR(500) NOT NULL,
        resume_score VARCHAR(8) NOT NULL,
        Timestamp VARCHAR(50) NOT NULL,
        Page_no VARCHAR(5) NOT NULL,
        Predicted_Field BLOB NOT NULL,
        User_level BLOB NOT NULL,
        Actual_skills BLOB NOT NULL,
        Recommended_skills BLOB NOT NULL,
        Recommended_courses BLOB NOT NULL,
        pdf_name varchar(50) NOT NULL,
        PRIMARY KEY (ID)
        );
    """
    cursor.execute(table_sql)

    DBf_table_name = 'user_feedback'
    tablef_sql = """
    CREATE TABLE IF NOT EXISTS """ + DBf_table_name + """
        (ID INT NOT NULL AUTO_INCREMENT,
        feed_name varchar(50) NOT NULL,
        feed_email VARCHAR(50) NOT NULL,
        feed_score VARCHAR(5) NOT NULL,
        comments VARCHAR(100) NULL,
        Timestamp VARCHAR(50) NOT NULL,
        PRIMARY KEY (ID)
        );
    """
    cursor.execute(tablef_sql)

    create_users_table()

    ###### CODE FOR CLIENT SIDE (USER) ######
    if choice == 'User':
        act_name = st.text_input('Name*')
        act_mail = st.text_input('Mail*')
        act_mob = st.text_input('Mobile Number*')
        sec_token = secrets.token_urlsafe(12)
        host_name = socket.gethostname()
        ip_add = socket.gethostbyname(host_name)
        dev_user = os.getlogin()
        os_name_ver = platform.system() + " " + platform.release()
        g = geocoder.ip('me')
        latlong = g.latlng
        geolocator = Nominatim(user_agent="http")
        try:
            location = geolocator.reverse(latlong, language='en')
            address = location.raw['address']
            city = address.get('city', '')
            state = address.get('state', '')
            country = address.get('country', '')
        except:
            city, state, country = '', '', ''

        st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload Your Resume, And Get Smart Recommendations</h5>''', unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Hang On While We Cook Magic For You...'):
                time.sleep(4)
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            pdf_name = pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                resume_text = pdf_reader(save_image_path)
                st.header("**Resume Analysis 🤘**")
                st.success("Hello " + resume_data['name'])
                st.subheader("**Your Basic info 👀**")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Degree: ' + str(resume_data['degree']))
                    st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                except:
                    pass

                cand_level = ''
                if resume_data['no_of_pages'] < 1:
                    cand_level = "NA"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''', unsafe_allow_html=True)
                elif 'INTERNSHIP' in resume_text.upper():
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''', unsafe_allow_html=True)
                elif 'EXPERIENCE' in resume_text.upper():
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!</h4>''', unsafe_allow_html=True)
                else:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Fresher level!</h4>''', unsafe_allow_html=True)

                st.subheader("**Skills Recommendation 💡**")
                keywords = st_tags(label='### Your Current Skills', text='See our skills recommendation below', value=resume_data['skills'], key='1')

                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit']
                web_keyword = ['react', 'django', 'node js', 'react js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'asp.net', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator', 'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro', 'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp', 'user research', 'user experience']
                n_any = ['english', 'communication', 'writing', 'microsoft office', 'leadership', 'customer management', 'social media']

                recommended_skills = []
                reco_field = ''
                rec_course = ''

                for i in resume_data['skills']:
                    i_lower = i.lower()
                    if i_lower in ds_keyword:
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling', 'Data Mining', 'Clustering & Classification', 'Data Analytics', 'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras', 'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', 'Flask', 'Streamlit']
                        st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='2')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(ds_course)
                        break
                    elif i_lower in web_keyword:
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento', 'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                        st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='3')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(web_course)
                        break
                    elif i_lower in android_keyword:
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java', 'Kivy', 'GIT', 'SDK', 'SQLite']
                        st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='4')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(android_course)
                        break
                    elif i_lower in ios_keyword:
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode', 'Objective-C', 'SQLite', 'Plist', 'StoreKit', 'UI-Kit', 'AV Foundation', 'Auto-Layout']
                        st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='5')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(ios_course)
                        break
                    elif i_lower in uiux_keyword:
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq', 'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing', 'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe', 'Solid', 'Grasp', 'User Research']
                        st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills, key='6')
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job💼</h5>''', unsafe_allow_html=True)
                        rec_course = course_recommender(uiux_course)
                        break
                    elif i_lower in n_any:
                        reco_field = 'NA'
                        st.warning("** Currently our tool only predicts and recommends for Data Science, Web, Android, IOS, and UI/UX Development**")
                        recommended_skills = ['No Recommendations']
                        st_tags(label='### Recommended skills for you.', text='Currently No Recommendations', value=recommended_skills, key='7')
                        st.markdown('''<h5 style='text-align: left; color: #092851;'>Maybe Available in Future Updates</h5>''', unsafe_allow_html=True)
                        rec_course = "Sorry! Not Available for this Field"
                        break

                st.subheader("**Resume Tips & Ideas 🥂**")
                resume_score = 0
                if 'OBJECTIVE' in resume_text.upper() or 'SUMMARY' in resume_text.upper():
                    resume_score += 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective/Summary</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your career objective, it will give your career intention to the Recruiters.</h5>''', unsafe_allow_html=True)
                if 'EDUCATION' in resume_text.upper() or 'SCHOOL' in resume_text.upper() or 'COLLEGE' in resume_text.upper():
                    resume_score += 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Education. It will give your qualification level to the recruiter.</h5>''', unsafe_allow_html=True)
                if 'EXPERIENCE' in resume_text.upper():
                    resume_score += 16
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Experience. It will help you to stand out from the crowd.</h5>''', unsafe_allow_html=True)
                if 'INTERNSHIP' in resume_text.upper():
                    resume_score += 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Internships. It will help you to stand out from the crowd.</h5>''', unsafe_allow_html=True)
                if 'SKILL' in resume_text.upper():
                    resume_score += 7
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Skills. It will help you a lot.</h5>''', unsafe_allow_html=True)
                if 'HOBBIES' in resume_text.upper():
                    resume_score += 4
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Hobbies. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h5>''', unsafe_allow_html=True)
                if 'INTERESTS' in resume_text.upper():
                    resume_score += 5
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interests</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Interests. It will show your interests other than the job.</h5>''', unsafe_allow_html=True)
                if 'ACHIEVEMENTS' in resume_text.upper():
                    resume_score += 13
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Achievements. It will show that you are capable for the required position.</h5>''', unsafe_allow_html=True)
                if 'CERTIFICATION' in resume_text.upper():
                    resume_score += 12
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h5>''', unsafe_allow_html=True)
                if 'PROJECT' in resume_text.upper():
                    resume_score += 19
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h5>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Projects. It will show that you have done work related to the required position or not.</h5>''', unsafe_allow_html=True)

                st.subheader("**Resume Score 📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score += 1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score) + '**')
                st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")

                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                insert_data(str(sec_token), str(ip_add), host_name, dev_user, os_name_ver, str(latlong), city, state, country, act_name, act_mail, act_mob, resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course), pdf_name)

                st.header("**Bonus Video for Resume Writing Tips💡**")
                resume_vid = random.choice(resume_videos)
                st.video(resume_vid)

                st.header("**Bonus Video for Interview Tips💡**")
                interview_vid = random.choice(interview_videos)
                st.video(interview_vid)

                st.balloons()
            else:
                st.error('Something went wrong..')

    ###### CODE FOR FEEDBACK SIDE ######
    elif choice == 'Feedback':
        ts = time.time()
        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(cur_date + '_' + cur_time)
        with st.form("my_form"):
            st.write("Feedback form")
            feed_name = st.text_input('Name')
            feed_email = st.text_input('Email')
            feed_score = st.slider('Rate Us From 1 - 5', 1, 5)
            comments = st.text_input('Comments')
            submitted = st.form_submit_button("Submit")
            if submitted:
                insertf_data(feed_name, feed_email, feed_score, comments, timestamp)
                st.success("Thanks! Your Feedback was recorded.")
                st.balloons()
        query = 'SELECT * FROM user_feedback'
        plotfeed_data = pd.read_sql(query, connection)
        labels = plotfeed_data.feed_score.unique()
        values = plotfeed_data.feed_score.value_counts()
        st.subheader("**Past User Ratings**")
        fig = px.pie(values=values, names=labels, title="Chart of User Rating Score From 1 - 5", color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig)
        cursor.execute('SELECT feed_name, comments FROM user_feedback')
        plfeed_cmt_data = cursor.fetchall()
        st.subheader("**User Comments**")
        dff = pd.DataFrame(plfeed_cmt_data, columns=['User', 'Comment'])
        st.dataframe(dff, width=1000)

    ###### CODE FOR ABOUT PAGE ######
    elif choice == 'About':
        st.subheader("**About The Tool - AI RESUME ANALYZER**")
        st.markdown('''
        <p align='justify'>
            A tool which parses information from a resume using natural language processing and finds the keywords, clusters them onto sectors based on their keywords. And lastly shows recommendations, predictions, analytics to the applicant based on keyword matching.
        </p>
        <p align="justify">
            <b>How to use it: -</b> <br/><br/>
            <b>User -</b> <br/>
            In the Side Bar choose yourself as user and fill the required fields and upload your resume in pdf format.<br/>
            Just sit back and relax our tool will do the magic on its own.<br/><br/>
            <b>Feedback -</b> <br/>
            A place where users can suggest feedback about the tool.<br/><br/>
            <b>Admin -</b> <br/>
            For login use <b>admin</b> as username and <b>admin@resume-analyzer</b> as password.<br/>
            It will load all the required stuff and perform analysis.
        </p><br/><br/>
        <p align="justify">
            Built with 🤍 by Shivendra Kumar Patel
        </p>
        ''', unsafe_allow_html=True)

    ###### CODE FOR ADMIN SIDE ######
    else:
        st.success('Welcome to Admin Side')
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'admin' and ad_password == 'admin@resume-analyzer':
                cursor.execute('''SELECT ID, ip_add, resume_score, convert(Predicted_Field using utf8), convert(User_level using utf8), city, state, country FROM user_data''')
                datanalys = cursor.fetchall()
                plot_data = pd.DataFrame(datanalys, columns=['Idt', 'IP_add', 'resume_score', 'Predicted_Field', 'User_Level', 'City', 'State', 'Country'])
                values = plot_data.Idt.count()
                st.success("Welcome Shivendra ! Total %d " % values + " Users Have Used Our Tool : )")
                cursor.execute('''SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob, convert(Predicted_Field using utf8), Timestamp, Name, Email_ID, resume_score, Page_no, pdf_name, convert(User_level using utf8), convert(Actual_skills using utf8), convert(Recommended_skills using utf8), convert(Recommended_courses using utf8), city, state, country, latlong, os_name_ver, host_name, dev_user FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's Data**")
                df = pd.DataFrame(data, columns=['ID', 'Token', 'IP Address', 'Name', 'Mail', 'Mobile Number', 'Predicted Field', 'Timestamp', 'Predicted Name', 'Predicted Mail', 'Resume Score', 'Total Page', 'File Name', 'User Level', 'Actual Skills', 'Recommended Skills', 'Recommended Course', 'City', 'State', 'Country', 'Lat Long', 'Server OS', 'Server Name', 'Server User'])
                st.dataframe(df)
                st.markdown(get_csv_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                cursor.execute('''SELECT * FROM user_feedback''')
                data = cursor.fetchall()
                st.header("**User's Feedback Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Feedback Score', 'Comments', 'Timestamp'])
                st.dataframe(df)
                query = 'SELECT * FROM user_feedback'
                plotfeed_data = pd.read_sql(query, connection)
                labels = plotfeed_data.feed_score.unique()
                values = plotfeed_data.feed_score.value_counts()
                st.subheader("**User Ratings**")
                fig = px.pie(values=values, names=labels, title="Chart of User Rating Score From 1 - 5 🤗", color_discrete_sequence=px.colors.sequential.Aggrnyl)
                st.plotly_chart(fig)
                
                # Pie-Chart for Predicted Field Recommendation
                labels = plot_data.Predicted_Field.unique()
                values = plot_data.Predicted_Field.value_counts()
                pie_df = pd.DataFrame({'labels': labels, 'values': values})
                st.subheader("**Pie-Chart for Predicted Field Recommendation**")
                fig = px.pie(pie_df, values='values', names='labels', title='Predicted Field according to the Skills 👽', color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
                st.plotly_chart(fig)
                
                # Pie-Chart for User's Experienced Level
                labels = plot_data.User_Level.unique()
                values = plot_data.User_Level.value_counts()
                pie_df = pd.DataFrame({'labels': labels, 'values': values})
                st.subheader("**Pie-Chart for User's Experienced Level**")
                fig = px.pie(pie_df, values='values', names='labels', title="Pie-Chart 📈 for User's 👨‍💻 Experienced Level", color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig)
                
                # Pie-Chart for Resume Score
                labels = plot_data.resume_score.unique()
                values = plot_data.resume_score.value_counts()
                pie_df = pd.DataFrame({'labels': labels, 'values': values})
                st.subheader("**Pie-Chart for Resume Score**")
                fig = px.pie(pie_df, values='values', names='labels', title='From 1 to 100 💯', color_discrete_sequence=px.colors.sequential.Agsunset)
                st.plotly_chart(fig)
                
                # Pie-Chart for Users App Used Count
                labels = plot_data.IP_add.unique()
                values = plot_data.IP_add.value_counts()
                pie_df = pd.DataFrame({'labels': labels, 'values': values})
                st.subheader("**Pie-Chart for Users App Used Count**")
                fig = px.pie(pie_df, values='values', names='labels', title='Usage Based On IP Address 👥', color_discrete_sequence=px.colors.sequential.matter_r)
                st.plotly_chart(fig)
                
                # Pie-Chart for City
                labels = plot_data.City.unique()
                values = plot_data.City.value_counts()
                pie_df = pd.DataFrame({'labels': labels, 'values': values})
                st.subheader("**Pie-Chart for City**")
                fig = px.pie(pie_df, values='values', names='labels', title='Usage Based On City 🌆', color_discrete_sequence=px.colors.sequential.Jet)
                st.plotly_chart(fig)
                
                # Pie-Chart for State
                labels = plot_data.State.unique()
                values = plot_data.State.value_counts()
                pie_df = pd.DataFrame({'labels': labels, 'values': values})
                st.subheader("**Pie-Chart for State**")
                fig = px.pie(pie_df, values='values', names='labels', title='Usage Based on State 🚉', color_discrete_sequence=px.colors.sequential.PuBu_r)
                st.plotly_chart(fig)
                
                # Pie-Chart for Country
                labels = plot_data.Country.unique()
                values = plot_data.Country.value_counts()
                pie_df = pd.DataFrame({'labels': labels, 'values': values})
                st.subheader("**Pie-Chart for Country**")
                fig = px.pie(pie_df, values='values', names='labels', title='Usage Based on Country 🌏', color_discrete_sequence=px.colors.sequential.Purpor_r)
                st.plotly_chart(fig)
            else:
                st.error("Wrong ID & Password Provided")

###### Main Run Function ######

def run():
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "main" and st.session_state.logged_in:
        main_app()

if __name__ == "__main__":
    run()
