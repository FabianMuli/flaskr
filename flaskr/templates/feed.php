<!DOCTYPE html>
<html>
    <head>
        <title>
            Feed
        </title>
    </head>
<nav id="top" style="background-color: white; margin-top: 2px;">
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
            <li><a href="{{url_for('feed')}}">Feed</a></li>
            <li><a href="#popularPosts">Popular Posts</a></li>
            <li><a href="about.html">Friends</a></li>
            <li><a href="contacts/contacts.html">Profile</a></li>

            {% if session.logged_in %}

                <a href="{{url_for('logout')}}">Signout</a>
        
            {% endif %}

        </span>
    </ul>
</nav>
{% extends 'layout.html' %}{% block body %}

<body>
    <fieldset class='fieldset' style="margin-left: 1%;">
    <i> {{ time }}</i> <br/></legend>

    <p>{{ summary }}</p> <br/>

    </fieldset>
    {% endblock %}
    
    <script src="https://unpkg.com/feather-icons/dist/feather.min.js"></script>

    <script>
        feather.replace();
    </script>
</body>
