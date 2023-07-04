# SW50 - Spotify Wrapped Every Month!

## What is it

My project is my own take on the popular "spotify wrapped" feature with the company release each year. The idea is that they present your listening habits across the year and visulise this in different ways. However, the problem with this, is it's only released once a year! That's what my flask-based web app aims to fix.

## The Tech Stack

- HTML/CSS
- Python (Flask)
- Javascript

## The Spotify API

One of my favourite things about this project was that I was seeing an idea I had, myself through to the end. The spotify API is vast and incredibly powerful, to be compeltely honest I have only scratched the surafec of what can be achieved. To use the spotify API you must first register an app and this app will be asigned a "client id" and a "client secret".

### Authentication and 0Auth

One of the first hurdles I faced with this project was spotify's range of authentication systems. I opted to go for the "Authorization code with PKCE" flow as this allowed my application to be used by different users if I decide to publish the project! The flow works be having your app redirect the user to the spotify serves where they will login before being redirected back to your app. When they are redirected back they are sent with an "access token" which can be used to make calls against the API.

### A Drop in the Ocean

The app that I have created does the bare minimum that the API itself is capabale of and should be explored in more detail by anyone that has an interest in spotify and data!

### Spotipy

In order to interface with the API I used a python library called "Spotipy", which makes the process of requesting various pieces of information alot more simple. However, through this I have interfaced with objects and methods and delved into the world of cookies!

## The Design

The design of the web app is my own, but I used various assets on the Figma community site to give me some inspiration as well as a few colour pallettes from the website coolers.com

### Bootstrap

I have incorportated bootstrap heavily in the project and I feel significantly more comfortable working with this framework to create UI's than I did going into this project.

### CSS

I had some experience in both HTML and CSS before this project but again, this has strengthened my abilities in both of these technologies and I feel like I'm in a brilliant position to delve deeper into the world of web development!

Thanks for reading,
Daniel
