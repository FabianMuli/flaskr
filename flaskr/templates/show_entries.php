{% if session.logged_in %}
<!DOCTYPE html>
<html lang="en-us">

    <nav id="top" style="background-color: white;">
        <ul>

            <li>

                <div id="mySidenav" class="sidenav" style="color:white;">
                    <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
                    <a href="about.html">Profile</a>
                    <a href="contacts/contacts.html">Friends</a>
                </div>

                <div id="main" style="text-align:right;">
                    <span style="font-size:30px;cursor:pointer" onclick="openNav()">&#9776;</span>
                </div>

            </li>

            <li id="company-name">
                <a href="#">FabChat
                </a>
            </li>

            <span style="margin-right:5%!important;">
                <li><a href="{{url_for('recent_feed')}}">Feed</a></li>
                <li><a href="#popularPosts">Popular Posts</a></li>
                <li><a href="about.html">Friends</a></li>
                <li><a href="contacts/contacts.html">Profile</a></li>

            

                <a class="hover" href="{{url_for('logout')}}">
                    Signout
                </a>

            </span>
        </ul>
    </nav>

    <body style="background-color: white;">
        {% extends "layout.html" %} {% block body %}
        <div class=container>

            <fieldset class="fieldset">
                <form action="{{ url_for('add_entry') }}" method=post class=add-entry>
                    Name: <input type='text' name='title' placeholder='name'>
                    <br />
                    <br />
                    Start Chat:<input style="width: 70%; height: 10%;" 
                    type="text" name="text" id="password" placeholder="Type message" required>
                    <br />
                    <br />
                    <input type="submit" value="Post" class="submit_button">
                    <b />
                    <br />
                </form>
            </fieldset>
        
            <br/>

            <fieldset class="fieldset">
                <ul class=entries>
                    {% for entry in entries %}
                
                    <li>
                        <fieldset class=entry_fieldset>
                            <legend>{{entry.title}}</legend>
                            <span>{{ entry.text }}</span>
                        </fieldset>
                    </li>

                    {% else %}
                    <li>

                    <em>
                        Start chatting to see messages here.
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
