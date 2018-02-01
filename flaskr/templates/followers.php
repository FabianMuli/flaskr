<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>followers</title>
</head>

{% extends 'show_posts.php' %}
{% block body %}
<body>
    <fieldset class="fieldset">
        <legend> <h2>Followers</h2> </legend>
    <ul class=entries>
    {% for follower in followers %}
    <li>
        <a href="{{url_for('Profile')}}">{{ follower.name }}</a>
        <a href="{{url_for('removeFollowers')}}"> <button class="submit_button"> unfollow</button></a>

    </li>
    {% else %}
        <p>You have no followers</p>
        <a href="{{url_for('addFollowers')}}"><button>Follow Fabian</button></a>
</body>
{% endfor %}
{% endblock %}
</html>