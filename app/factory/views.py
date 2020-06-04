from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from app.forms import LoginForm, RegisterForm, SearchForm, BuyForm, SellForm
from app.factory.auth import create_user, verify_login
from app.models import User
from app.factory.stock_api import get_price, api_response
from app.factory.buy_sell import buy_shares, create_wallet, get_history, get_stocks, sell_shares


def init_app(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/login', methods=['GET','POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            return verify_login(form)
        return render_template('login.html',form=form)


    @app.route('/signup',methods=['GET','POST'])
    def signup():
        form = RegisterForm()
        if form.validate_on_submit():
            return create_user(form)
        return render_template('signup.html',form=form)


    @app.route('/dashboard', methods=['GET','POST'])
    @login_required
    def dashboard():
        form = SearchForm()
        wallet = create_wallet(current_user.username)
        return render_template('dashboard.html',name=(current_user.username).title(), form=form, wallet=wallet)
    

    @app.route('/quote', methods=['GET','POST'])
    @login_required
    def quote():
        form = SearchForm()
        result = form.symbol.data 
        response = get_price(result)
        if response == False:
            text = f'not a valid Symbol'
            return render_template('quote.html', response=text, form=form)
        text = f' A  share of {result} costs {response}.'
        return render_template('quote.html', response=text, form=form)
    
    @app.route('/buy', methods=['GET','POST'])
    @login_required
    def buy():
        form  = SearchForm()
        form2 = BuyForm()
        if form2.validate_on_submit():
            return buy_shares(form2,current_user.username)
        return render_template('buy.html', form=form, form2= form2)
    
    
    @app.route('/sell', methods=['GET','POST'])
    @login_required
    def sell():
        form = SearchForm()
        form2 = SellForm()
        form2.symbol.choices = get_stocks(current_user.username)
        if form2.validate_on_submit():
            return sell_shares(form2,current_user.username)
        return render_template('sell.html', form=form, form2= form2)
    
    @app.route('/history', methods=['GET','POST'])
    @login_required
    def history():
        form = SearchForm()
        history = get_history(current_user.username)
        return render_template('history.html',  form=form, history=history)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
