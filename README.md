Description:
    This project is a flask site which allows you to create an account, log in, and create a dashboard of tasks that you may add and remove as you please.
    The main two additional requirements I fufilled were user authenticaton and an additional database(specifially being able to insert and delete from a database table). The 
    main databases in this project are the database of users and the database of tasks which keeps track of user id's to check who submitted a task, task ids, task names and task
    descriptions.

    The project includes a form you can fill out from your dashboard to submit a task and a delete button to remove a task you have created. If you oberserve thhe data.sqlite file
    (with the appropriate software allowing you to view the file) while removing tasks you will see you are not just removing it from view but also removing it from the
    database.

File Structure:
    All of the relevant python/flask code is within the app.py file. The html templates can be found within the "templates" folder and the images and css can be found inside the "static" folder.

Running:
    In order to run my code you must first navigate to the folder where my project's files are contained. Type ```pip install -r requirements.txt``` just in case you don't have all of the correct packages installed. Then, from a virtual environment or computer you must type "python app.py" to begin running my code. You will then be prompted with an address such as "http://127.0.0.1:5000/" which you may navigate to in order to see my website. From there you can press the login button to login or the register button to create an account. Once you are logged in you may go to the dashboard from the navigation bar (if not already redirected) and begin adding and removing tasks. If it is not immediately apparent, the logout button appears in the navigation bar when you are logged in.