# Cyber Security Base Project I

As a base for this project, I used a web application that I had made previously for another course. So, originally this program did not have any vulnerabilities.

### INSTALLATION INSTRUCTIONS:
- clone the repository from github to your computer and go to the root folder
- run command `pip install -r requirements.txt` to install all the dependencies
- create .env file to the root and insert database information to it: DATABASE_URL=postgresql:///put your username here SECRET_KEY=put your secret key here
- if the DATABASE_URL above does not work, try postgresql+psycopq2:///your username instead
- open postgresql in a different terminal with the command `start-pg.sh`
- start the program with `flask run` (keep postgresql open on a different terminal)

NOTE that you have to have postgresql installed on your computer for this application to work. It can be downloaded from here: https://www.postgresql.org/download/

The flaws (except Cross-Site Request Forgery (CSRF)) are from the OWASP Top Ten 2017 list.


### FLAW 1 – Cross-Site Request Forgery (CSRF):

LINK 1: https://github.com/sohvip/cyber-security-project/blob/main/routes.py#L113  
LINK 2: https://github.com/sohvip/cyber-security-project/blob/main/templates/editpost.html#L1  

Cross-Site Request Forgery (CSRF) vulnerability is present when the application does not verify whether a page request, that seems to come from a specific user, actually comes from that user. In my program, anyone can pretend to be any user and edit their posts by entering the correct address for example http://127.0.0.1:5000/category/1/1/editpost.

To fix this, we need to ask for the CSRF token when the editing form is sent and compare it to the session token. If they differ from each other, the edit is denied. The code that fixes the problem could be something like this:

routes.py
token = request.form['csrf_token'] 
if session['csrf_token'] != token:
abort(403)

editpost.html
<input type="hidden" name="csrf_token" value="{{ session.csrf_token }}">

The fix is also provided as comments in the links above.


### FLAW 2 – A1:2017 - Injection (SQL):

LINK: https://github.com/sohvip/cyber-security-project/blob/main/categories.py#L16  

SQL injection means that user inputs are concatenated straight into SQL commands making it possible to tamper the original queries. This could lead to serious data leakages and unauthorized access to sensitive data. Also, the database could be manipulated and in the worst case, the whole program could be compromised.

These rows of code should fix the issue:

sql = 'delete from categories where id=:id'
db.session.execute(sql, {'id':id})
db.session.commit()

The fix can also be found in the link above as comments.


### FLAW 3 – A2:2017 - Broken Authentication:

LINK: https://github.com/sohvip/cyber-security-project/blob/main/routes.py#L169  

Broken authentication in my program means that because there are no requirements for setting the password, it is easy for malicious users to guess some accounts' passwords (for example passwords that consist of less than five characters) with brute force. Also, session tokens and other user information could be compromised due to broken authentication. This could result in harmful consequences such as data breaches and identity theft.

Making requirements for the password fixes this problem. In my code, there is a fix provided where the set password must be more than five characters long:

if not len(password) > 5:
return render_template('signup_error.html', \ 
        	    message = 'Password must be atleast 6 characters long.')

Another additional fix could be to prevent users from using common passwords such as “password”.

The fix can also be found in the link above as comments.


### FLAW 4 – A3:2017 - Sensitive Data Exposure:

LINK: https://github.com/sohvip/cyber-security-project/blob/main/routes.py#L41  

Sensitive data exposure happens when there are some private data accessible to a malicious user. In this application, every account’s information is available to the public with an address of the type  http://127.0.0.1:5000/accountinfo/[user_id]. Sensitive data exposure could for example lead to hackers stealing sensitive information such as passwords, credit card information, or other personal data which exposes users to identity theft and financial fraud.

Ideally, this type of information should be avoided to show in a web application. But, to fix the leakage, there must be a confirmation that the user is actually signed in. The confirmation could look like this:

if id != get_user_id():
abort(403)
The code is also provided in the link above as comments.


### FLAW 5 – A7:2017 - Cross-Site Scripting (XSS):

LINK: https://github.com/sohvip/cyber-security-project/blob/main/routes.py#L32  

Cross-Site Scripting (XSS) vulnerability means that the user can modify the appearance of a page that uses HTML with the inputs they give. They could also inject scripts to for example bypass access controls. This is because the program does not check for the validity of the inputs. When a new user registers to my program and gives a username that is in itself HTML code (for example `<h1> HELLO WORLD </h1>`), it will be treated as a part of the HTML template on the pages /account & /accountinfo/[user_id].

Flask’s page templates check the inputs automatically and prevent this flaw, so to fix this problem we need to move the HTML code to a new file in the templates folder, and then render that file with the following code: return render_template(‘name_of_the_file.html’, user_input_parameters).
