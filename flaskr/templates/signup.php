!DOCTYPE html>
<html>
    <head>
        <title>
            Signup
        </title>
        
        <link href="\static\signup.css" rel="stylesheet">

    </head>

    <nav id="top" style="background-color: white;">
        <ul>


            <li id="company-name">
                <a href="#">FabChat
                </a>
            </li>

        </ul>
    </nav>

    {% extends "layout.html" %}

    <body ng-app="form">
        {% block body%}
        <div>

            <fieldset class="fieldset">

                <legend>
                    Sign up
                </legend>

                 {% if error %}
                <p class=error>{{ error }}</p>
                {% endif %}

                <form class="login_Form" autocomplete="on" method="post" name="signup_form" action="{{url_for('signup')}}">
                    First name: <input style="margin-left: 5%;" type="text" name="first_name" id="first_name">
                    <br />
                    <br /> Second name: <input style="margin-left: 1%;" type="text" name="second_name" id="second_name">
                    <br />
                    <br /> Mobile No.: <input style="margin-left: 6%;" type="tel" name="mobile_no" id="mobile_no">
                    <br />
                    <br /> Email: <input style="margin-left: 20%;" type="email" name="email" id="email">
                    <br />
                    <br /> Password: <input style="margin-left: 10%;" type="password" name="passwd" id="passwd">
                    <br />
                    <br /> Confirm <input style="margin-left: 15%;" type="password" name="passwd2" id="passwd2">
                    <br />
                    <br />
                    <input type="submit" value="Sign Up" class="submit_button">

                </form> 
               
            </fieldset>
        </div>
        {% endblock %}
                
        <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>  

    </body>
</html>

