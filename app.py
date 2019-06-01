from flask import Flask, jsonify, Response, render_template, request, redirect, url_for
import json
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, SubmitField, validators
from engine import *

app = Flask(__name__)
app.static_folder = 'static'

# CREATE A SECRET KEY BECAUSE THE STUPID FORM REQUIRES IT FOR VALIDATION
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# COMPILES A LIST OF MOVIE TITLES TO BE PASSED INTO THE AUTOCOMPLETE FORM
movie_list = movies['title'].tolist()

# INDEX ROUTE - SELECTS 6 MOVIES AT RANDOM FROM MOVIES DF AND DISPLAYS THEM ON THE PAGE AS A STARTING POINT
# ALSO LISTENS FOR THE POST FROM THE AUTOCOMPLETE FORM AND ROUTES THE FORM SUBMISSION TO THE REC ROUTE
@app.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == 'POST':
        title = form.autocomp.data.replace(" ", "%20")
        return redirect('http://127.0.0.1:5000/rec/' + title)
    rando_df = movies.sample(6)
    title2 = []
    url = []
    for x in rando_df.title:
        title2.append(x)
        print(x)
    for y in rando_df.poster_path:
        url.append("http://image.tmdb.org/t/p/w185" + str(y))
    return render_template('index.html', title2=title2, url=url, form=form)


@app.route("/rec/<title>")
def movie_bot_final(title):
    # ALGORITHM TO FIND THE COSINE SIMILARITY OF MOVIES BASED ON THEIR VECTORIZED GENRE FEATURES
    titles = movies['title']
    indices = pd.Series(movies.index, index=movies['title'])
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    # TAKES THE 12 MOST SIMILAR MOVIES TO THE TITLE MOVIE INPUT
    mv = titles.iloc[movie_indices].head(12).to_frame()
    cols = ['title']
    temp_df = mv.join(movies.set_index(cols), on=cols)
    rando_df = movies.sample(6)
    moviename = []
    title2 = []
    url1 = []
    url = []
    titleloc = movies.loc[movies['title'] == title]
    # GRABS THE HREF FROM THE IMAGES AND RUNS THEM THROUGH THE ALGORYTM TO FIND THE 12 NEAREST MATCHES
    # PULLS THE IMAGE URL FROM THE MOVIES DF AND APPENDS THEM TO THE URL PREFIX FOR THE MOVIE POSTERS
    # PASSES THE MOVIE POSTER URL INTO THE RECS.HTML PAGE
    titleurl = ("http://image.tmdb.org/t/p/w185" + titleloc['poster_path'].iloc[0])
    for rando in rando_df.title:
        title2.append(rando)
    for rando_poster in rando_df.poster_path:
        url.append("http://image.tmdb.org/t/p/w185" + str(rando_poster))
    for film in temp_df.title:
        moviename.append(film)
    for poster in temp_df.poster_path:
        url1.append("http://image.tmdb.org/t/p/w185" + str(poster))
    return render_template('recs.html', moviename=moviename, url1=url1, title2=title2, url=url, title=title, titleurl=titleurl)

# SETS UP THE FORM WITH THE AUTOCOMP TEXT FIELD AND SUBMISSION BUTTON
class SearchForm(Form):
    autocomp = TextField('Enter Movie Title', id='movie_autocomplete')
    submit = SubmitField('Search')

# THE BRAINS OF THE AUTOCOMPLETE. PULLS THE MOVIES FROM THE LIST VARIABLE AND RETURNS A JSON THAT CAN BE PARSED BY THE JQUERY ON THE HTML PAGE
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(movie_list), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)