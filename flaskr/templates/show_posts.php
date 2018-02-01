{% if session.logged_in %}
<!DOCTYPE html>
<html lang="en-us">
{% extends "layout.html" %} 
    <body>
        {% block body %}

        <div class="container">

            <fieldset class="fieldset">
                {% from "_formhelpers.html" import render_field %}
                <form action="{{ url_for('add_entry') }}" method=post class=add-entry>
                    {{form.hidden_tag() }}
                    <br />
                    <br />
                    {{ render_field(form.post, placeholder="Post something to get claps.", class=
                        "postField")}}
                    <br />
                    <br />
                    {{ render_field(form.submit, class="submit_button")}}
                    <b />
                    <br />
                </form>
            </fieldset>
        
            <br/>

            <fieldset class="fieldset">
                <ul class=entries>
                    {% for post in posts %}
                
                    <li>
                        <fieldset class=entry_fieldset>
                        <legend><a href="#">{{post.name | capitalize}}</a></legend>
                            <span>{{ post.post }}</span>
                            <!--delete the comment 
                            <span class="delete_button">
                            <a href="#">delete</a>
                        </span>
                        -->

                        </fieldset>
                    </li>

                    {% else %}
                    <li>

                    <em>
                        All posts appear here.
                    </em> 

                    {% endfor %}

                </ul>

                <a href="#top" style="margin-left: 19%;">
                    <button class=top>
                        Top
                    </button>
                </a>
            </fieldset>
        </div>
        {% endblock %}

    </body>

    {% else %}
    <p>
        <a href="{{url_for('login')}}">
            Log in
        </a> to see this page
    </p>

    {% endif %}
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous">
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.19.2/locale/af.js">
    </script>

</html>
