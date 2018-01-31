<!DOCTYPE html>
<html>
    <head>
        <title>
            Signup
        </title>
        
    </head>

    {% extends "layout.html" %}

    <body>
        {% block body%}
        <div>
                 {% if error %}
                <p class=error>{{ error }}</p>
                {% endif %}

                {% from "_formhelpers.html" import render_field %}
                <form action='' method="post" class="form">
                    {{ form.hidden_tag() }}
                    <fieldset class="signup_fieldset">
                        <h1 class="logo">Fabchat</h1>
                        <br />
                        <h2>Sign up</h2>
                        <br />
                        <dl>
                            {{ render_field(form.first_name, placeholder="first name")}}
                            <br />
                            {{ render_field(form.second_name, placeholder="second name")}}
                            <br />
                            {{ render_field(form.email, placeholder="example@gmail.com") }}
                            <br />
                            {{ render_field(form.mobile_number, placeholder="mobile number") }}
                            <br />
                            {{ render_field(form.password, placeholder="password")}}
                            <br />
                            {{ render_field(form.password2, placeholder="confirm password")}}
                            <br />
                        </dl>
                        <p><input type="submit" value="sign up" class="submit_button"></p>
                    </fieldset>
                </form>
        </div>
        {% endblock %}
    </body>
</html>

