I have created this project to serve the purpose of the first course project for the Cyber Security Base 2024 at the Open University of Helsinki. This project aims to outline five different flaws from the OWASP 2017 top ten list, and their fixes, in a form of To do list -web application. This project is backend focused. 
To install and test this project, the installations required on the course should be enabled. First, you may clone this project.

Then make the necessary migrations:
```
python3 manage.py migrate
python3 runserver
```

After which the website should be found from your localhost. There are a few possible users you may login:
```
alice - redqueen
admin - pass
bob - squarepants
```

# FLAW 1:  Injection 
### Code Location: https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L62

Injection is a flaw, where malicious data is injected through unsanitized data input field in an application. SQL injection vulnerabilities occur when user input is directly embedded into SQL queries without validation or sanitization. When unsanitized input is executed as part of a query, it allows attackers to inject malicious SQL commands, potentially leading to unauthorized data access, data manipulation, or even deletion of database tables. [1] 

In this project, the viewall function uses user input directly within a raw SQL query, making it vulnerable to SQL injection. The function allows users to pass in parameters through the text parameter, which is then directly formatted into the SQL command. For example with URL http://localhost:8000/viewall/?text=' OR '1'='1 , user can reach all todos of all users. 

### How to Fix: 
This vulnerability can be fixed by using Django's Object Related Mapping ORM, which includes further protection. In this case, Django’s method filter could be used, as shown in https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L63 

# FLAW 2: Sensitive Data Exposure 
### Code Locations: 
https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L21C1-L31C29
https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L69

Sensitive Data Exposure is a vulnerability where sensitive user data is improperly protected, increasing the likelihood of unauthorized access or data leaks, mentioned in OWASP list of 2017. [2]  

In this project data exposure occurs in two ways: first, the addtodo function uses a GET request, which exposes user data such as the username and todo fields in the URL. This approach increases the risk of sensitive data leakage, as URLs can be stored in browser history and logged by network servers. Second, allowing access to user data in the viewtodo function, only by guessing the correct IDs and URL, which could allow attackers to guess and access other users' to-do items. For example http://127.0.0.1:8000/viewtodo/47/ . If users trust the application and adds personal details in their to-dos, it risks leaking sensitive information to unauthorized users. 

### How to Fix: 
This flaw could be fixed by switching to POST requests instead of GET requests, as shown in https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L33C1-L46C1 and https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/templates/index.html#L32. In addition, access control should be developed further, which is discussed in the next section. Encrypting or use of HTTPS protocol especially with sensitive data would provide further security, making the data unusable to attackers even if they gain unauthorized access.  

 
# FLAW 3: Broken Access Control 
### Code Locations: 
https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L21C1-L31C29
https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L69
 
Broken access control is a vulnerability that enables users to act outside their intended permissions. Due to broken access control, users might gain access to sensitive data or perform unauthorized functions. This can result in severe security issues such as data exposure, unauthorized data modification, or loss of data integrity. [3] 
In this project, access control vulnerabilities appear in several parts: the addtodo function does not verify if the currently authenticated user matches the user specified in the URL. Therefore, an attacker can manipulate the username parameter to add to-do items on another user's account. For example 127.0.0.1:8000/addtodo?user=admin&todo=youhavebeenhacked&done=true. In addition, viewtodo does not check if the user owns the requested todo item, which means that any user who knows a to-do item’s URL can view it, regardless of whether they own the item. 
  
### How to Fix: 
This could be fixed by using request.user instead of allowing user in GET parameters, https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L38. This ensures that only the authenticated user can modify their data. Besides, @login_required tags should be uncommented: https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L48. Lastly, the ownership of the todo should be validated by checking that request.user matches the owner of the todo, if nessecary: https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L52. 
One solution to enhanced access control is shown in the function deletetodo, where is implemented both fixes, POST requests and authentication of the user with request.user. 

# FLAW 4: Cross-Site Request Forgery (CSRF) 
### Code Location: 
https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/templates/viewtodo.html#L14
https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L19

With Cross-site Request Foregy it is possible to create requests from another site to the web application. If the user accessing the source site is authenticated for the target web application, as the user is accessing the source site, the browser will send an authentication token with the request,. This allows the attacker to perform actions within the target application without the user’s consent, potentially accessing or modifying data that should be protected. [2] So, without CSRF tokens in forms, the application is vulnerable to attacks where an attacker could forge requests on behalf of authenticated users, since the application cannot verify the origin of a request. 
This project lacks both,  some ‘csrf_token’ -tags in the HTML, but also ‘@csrf_protect’ -tags in functions where sensitive actions occur. Furthermore, as CSRF goes along with POST, the vulnerabilities related to requests above should be fixed before this. Without CSRF tokens, the application does not check the origin of POST requests, thus this application is vunerable to POST request from other, possibly malicious sites.  

### How to Fix: 
This could be fixed by adding {% csrf_token %} to all HTML forms that submit data via POST requests. In addition, @csrf_protect should be enabled in all functions where sensitive actions occur. Lastly, ’csrf_exempt’ -tag should be removed. Fixes have been implemented as comments, for example https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/views.py#L19 . 
 
# FLAW 5: Cross-Site Scripting (XSS) 
### Code Location:  https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/templates/viewtodo.html#L7

In Cross-Site Scripting attacks, malicious scripts are injected into trusted websites. When attacker uses a web application to send the malicious code, typically to a different end user in a form of browser side script, the attack occurs. The end user’s browser cannot distinguish between trusted and malicious scripts, so it executes the code, potentially exposing cookies, session tokens, and other sensitive information stored in the browser. [4] 
In this project, an XSS vulnerability is present because todo.text is rendered with the safe filter in viewtodo.html. The safe filter marks content as safe and bypasses HTML escaping [5], allowing execution of arbitrary JavaScript if todo.text contains malicious code. This lack of proper sanitization for user-provided content leaves the application vulnerable to XSS.

### How to Fix: 
This could be fixed by replacing {{ todo.text | safe }} with  Django’s built in escape filter{{ todo.text | escape }}, which will automatically sanitize the input by escaping HTML tags and special characters, preventing potential script injection. https://github.com/vesaloko/csb/blob/ec63fc400a5bd5763c03322b51f016e4a98ee623/pages/templates/viewtodo.html#L7C1-L10C64

____________________________________________________________
[1] https://owasp.org/www-community/attacks/SQL_Injection 
[2] https://cybersecuritybase.mooc.fi/module-2.3/1-security 
[3] https://owasp.org/Top10/A01_2021-Broken_Access_Control/
[4] https://owasp.org/www-community/attacks/xss/ 
[5] https://docs.djangoproject.com/en/5.1/ref/templates/builtins/ 
 
