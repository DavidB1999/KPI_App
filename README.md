# KPI_App

Just for fun I started playing around with *Streamlit* (https://streamlit.io/). I realized how fun it is so I started builiding this app, that accessed data from *FBref* (https://fbref.com/en/) and allows the user to visualize a number of KPIs in a radar chart (classic :D). My app works exactly the way I intended it to... but only offline. 
When deploying it via *Streamlit* (https://kpiapp-db.streamlit.app/), I get an *RecursionError* which is apparently caused by my select widgets (selectbox and multiselect).
So far I have been unable to find a solution, but since the deployment relies on a github-repository anyway I might as well document the current status of this mini-project.

This is what it looks like offline: <br>


![The App]('https://github.com/DavidB1999/KPI_App/blob/main/WebApp.jpg)
