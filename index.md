---
---

<img src="assets/logo.jpg" height="100">

<body>

<ul>
{% for episode in site.data.episodes %}
<li>
    {% if episode.number %}
    #{{ episode.number }}:
    {% endif %}
    <a href="{{ episode.link }}"><em>{{ episode.title }}</em></a>
    ({{ episode.date|date:"%d"|plus:"0" }} {{episode.date|date:"%B %Y" }})

    {% if episode.films %}
    <ul>
    {% for film in episode.films %}
        <li><em>{{ film.title }}</em>{% if film.year %} ({{ film.year }}){% endif %}</li>
    {% endfor %}
    </ul>
    {% endif %}
    <br>
</li>
{% endfor %}
</ul>

<h2>Bonus content</h2>

<ul>
{% for episode in site.data.bonus %}
<li>
    <a href="{{ episode.link }}"><em>{{ episode.title }}</em></a>
    ({{ episode.date|date:"%d"|plus:"0" }} {{episode.date|date:"%B %Y" }})
</li>
{% endfor %}
</ul>
