<!DOCTYPE html>
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

    <body>
        {% block body%}
        <div>
                 {% if error %}
                <p class=error>{{ error }}</p>
                {% endif %}

                <form method="post">
                    {{ form.first_name() }}
                    <br />
                    <br />
                    {{ form.second_name() }}
                    <br />
                    <br />
                    {{ form.email()}}
                    <br />
                    <br />
                    {{ form.mobile_number() }}
                    <br />
                    <br />
                    {{ form.password() }}
                    <br />
                    <br />
                    {{ form.password2() }}
                    <br />
                    <br />
                    {{ form.submit() }}
                </form>
        </div>
        {% endblock %}
    </body>
</html>

