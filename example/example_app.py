from flask.ext.mab.storage import JSONBanditStorage
from flask.ext.mab.bandits import EpsilonGreedyBandit

color_bandit = EpsilonGreedyBandit(0.9)
color_bandit.add_arm("green","green")
color_bandit.add_arm("red","red")
color_bandit.add_arm("blue","blue")

txt_bandit = EpsilonGreedyBandit(0.5)
txt_bandit.add_arm("casual","Hey dude, wanna buy me?")
txt_bandit.add_arm("neutral","Add to cart")
txt_bandit.add_arm("formal","Good day sir... care to purchase?")

from flask import Flask,render_template
from flask.ext.mab import BanditMiddleware

app = Flask('test_app',template_folder="./example/templates",static_folder="./example/static")
app.config['MAB_STORAGE_ENGINE'] = 'JSONBanditStorage'
app.config['MAB_STORAGE_OPTS'] = ('./example/bandit_storage.json',) 
BanditMiddleware().init_app(app) #bandit storage from previous code block
app.add_bandit('color_btn',color_bandit) #our bandits from previous code block
app.add_bandit('txt_btn',txt_bandit)

@app.route("/")
@app.choose_arm("color_btn")
@app.choose_arm("txt_btn")
def home():
    """Render the btn using values from the bandit"""
    return render_template("ui.html",btn_color=home.color_btn,btn_text=home.txt_btn)

@app.route("/btnclick")
@app.reward_endpt("color_btn",1.0)
@app.reward_endpt("txt_btn",1.0)
def reward():
    """Button was clicked!"""
    return render_template("btnclick.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
