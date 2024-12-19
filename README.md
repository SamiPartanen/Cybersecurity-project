# Cybersecurity-project

Link: https://github.com/SamiPartanen/Cybersecurity-project/ 

My application for this project is Django polls app, where admin can add questions and choices to those questions, and logged in users can vote on those questions. My five security flaws are picked from the 2017 OWASP top ten list. 

To test project clone it with git clone https://github.com/SamiPartanen/Cybersecurity-project.git 
and change to Djangotutorial directory, that includes the manage.py file.

if you do not have Django you may need to install it with 

-pip install Django

then you can run it with 

-python manage.py runserver   

http://127.0.0.1:8000/

User:  	Password:

user1 	password

admin 	12345

testuser 	letmein

Flaw 1 CSRF

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/views.py#L118 

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/templates/polls/detail.html#L13 


1.	 CSRF (Cross-Site Request Forgery) is an attack where the user is tricked into doing unwanted actions on a website, where the user is authenticated. The site is not able to differ the user and the forged request the attack is giving. The attacks usually are targeted actions that change server-side data, so like updating password or making a purchase. Also it can trick user to adding personal data to an account, that the attacker controls. In my Django polls app the link with the different polls, what says “Claim Your Prize” takes the user to polls/malicious/ site where they are tricked into pressing another Claim Your Prize link, which votes on one of the questions automatically without you choosing anything. This is possible because the app lacks CSRF protection and the action is triggered with a GET request, which should only be used to retrieve data, and that makes the app also vulnerable to CSRF attacks. 

To fix this security flaw, we need to enable Django’s CsrfViewMiddleware, which is commented out, and change GET request to POST. In detail.html, csrf-token is also commented out, so to fix this CSRF issue we need to also enable that. [1]

FIXES: 

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/templates/polls/detail.html#L14 

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/settings.py#L50

FLAW 2. XSS

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/models.py#L9

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/templates/polls/detail.html#L16


2.	Cross-Site-Scripting (XSS) allows the attacker to inject malicious scripts into the website, and those scripts are then executed in the victim’s browser. This can happen if input is included in the website without proper validation and the script is executed. The result of the attack depends on the script, but usually the goal of the attack can be for example to steal sensitive data like cookies, hijack sessions or redirect users. The scrips can be stored in the web application, for example in the database, in which case it is a stored XSS attack, like in my Django app. In my app, the admin can add question, but the char field with maximum length, is modified to text field without maximum length. Also in index.html safe filter is used, so that the XSS attack is possible, because the content is considered safe, and the scripts can be executed. Also the content of the text field is passed to html without validating or sanitizing, so the question can contain a script and the safe filter allows the browser to run it. [2]


To fix xss flaw, the text field in models.py needs to be changed to char field with maximum length to reduce the risk to malicious scripts being injected to the text field.  Also removing the safe filter from the html file makes sure that Django it self does not run these scripts, but shows them as plain text. 

FIXES: 

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/models.py#L8

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/templates/polls/detail.html#L16


FLAW 3: Broken access control

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/views.py#L51


3.	Broken access control is a flaw where the application fails to properly check on what actions users can perform or where they can access. The malicious user can then do whatever he/she is capable of, typically seek information, modify or delete data or perform tasks meant for business owners. In my polls app, this means that when user opens the website, they should login, but with the broken access control fault, they can just go to poll and vote without logging in, so for example they can go to /polls/2/ and vote even without logged in. This is possible because the app does not check if the user is logged in before voting. To fix this, before voting the app checks if the user is logged in, in which case they can vote, or if they are not, they are redirected to login page. [3]

To fix the issue, the vote method in views.py to check if the user is logged in. To make that work, the comments need to be removed, and then if the user is not logged in, they are redirected to login page. 


FIXES: 

Remove comments  https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/views.py#L52   and L53

FLAW 4: Security misconfiguration

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/settings.py#L27

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/urls.py#L29


4.	Security misconfiguration is a flaw where the app lacks proper security settings. Examples could be from default passwords to exposing detailed error message or outdated software. Attackers could use this flaw to gain access to sensitive information or generally get access to the app where they should not be able to do.[4] In my polls app, this flaw can be used to see the settings file. When debug is set as true, and going to site /polls/trigger-error/, is executes method in views.py where is division by zero, which causes the error. But when the debug is true, it exposes a lot of information about the application. Another security misconfiguration flaw can be used if user goes to    /expose-settings/ it opens settings file in the browser where sensitive information can be seen. 


To fix this flaw, the debug needs to be false, which will prevent the user seeing the debug view and seeing information there. With the debug being false, allowed hosts need to be put to the settings. Also the re-path to expose settings needs to be removed from urls. 


FIXES:

debug = false https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/settings.py#L27 

Remove: https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/urls.py#L29

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/settings.py#L31


FLAW 5: Sensitive data exposure

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/settings.py#L24

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/views.py#L155

5.	The fifth flaw is sensitive data exposure is flaw, where important information like passwords, credit card numbers or secret keys are not protected and attacker can gain access to them. This can happen if that data is weakly encrypted, stored in plain text or

transported unsafely.[5] In this app the flaw is visible when user goes to /polls/sensitive_data/ where the secret key is displayed. This is because the secret key is stored in text in the views.py file and it returns the key.  

To fix this flaw, we do a env. file where the secret key is stored and the secret key from settings is removed. Then the secret key is stored safely and not in the settings. Also in the views file, the method need to be removed and the secret key is no longer visible 
from /polls/sensitive_data/. 

FIXES: https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/polls/views.py#L161

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/.env

https://github.com/SamiPartanen/Cybersecurity-project/blob/main/djangotutorial/djangotutorial/settings.py#L27




references

[1] https://owasp.org/www-community/attacks/csrf 

[2] https://owasp.org/www-community/attacks/xss/

[3] https://owasp.org/Top10/A01_2021-Broken_Access_Control/

[4] https://owasp.org/Top10/A05_2021-Security_Misconfiguration/ 

[5] https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure 

