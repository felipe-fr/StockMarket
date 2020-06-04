from flask import Flask, render_template, redirect, url_for, flash
import datetime

from app.factory.stock_api import get_price
from app.factory.database import db
from app.models import User, TransactionHistory

        
def buy_shares(form, name):
    price = get_price(form.symbol.data)
    if price != False:
        price = float(price)
        shares = int(form.shares.data)
        cost = price*shares
        user = User.query.filter_by(username=name).first()
        date_time = datetime.datetime.now() #.strftime("%Y-%m-%d %H:%M:%S")
        if user.cash > cost:
            cash = user.cash - cost
            user.cash = cash
            db.session.commit()
            new_buy = TransactionHistory(user_id=user.id, symbol=(form.symbol.data).upper(), shares=shares,price=price,cost=cost,date_time=date_time)
            db.session.add(new_buy)
            db.session.commit()
            flash("You've bought successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("not enough cash")
            return redirect(url_for('buy'))
    else:
        flash("not a valid symbol")
        return redirect(url_for('buy'))
    
def raw_wallet(name):
    user = User.query.filter_by(username=name).first()
    transations = TransactionHistory.query.filter_by(user_id=user.id)
    history = []
    for row in transations:
        item_history = {"Symbol" : "" , "Shares" : ""}    
        item_history["Symbol"] = row.symbol
        item_history["Shares"] = row.shares
        check_history = False
        for item in history:
            if item_history["Symbol"] in item.values():
                item["Shares"] += item_history["Shares"]
                if item["Shares"] == 0:
                    history.remove(item)

                check_history = True
        if check_history == False:
            history.append(item_history)
    return history

def create_wallet(name):
    user = User.query.filter_by(username=name).first()
    wallet = []
    raw = raw_wallet(name)
    for share in raw:
        item = {"Symbol" : "" , "Shares" : "", "Price" : "" , "Total" : "" }
        item["Symbol"] = share["Symbol"]
        item["Shares"] = int(share["Shares"])
        item["Price"]  = float(get_price(share["Symbol"]))
        cost  = item["Shares"]*item["Price"]
        item["Total"]  = round(cost,2)
        wallet.append(item)
    cash = {"Symbol" : "" , "Shares" : "", "Price" : "" , "Total" : "" }
    cash["Symbol"] = "CASH"
    cash["Total"]  = round(user.cash,2)
    wallet.append(cash)
    total = 0
    for element in wallet:
        total += element["Total"]
    last = {"Symbol" : "" , "Shares" : "", "Price" : "" , "Total" : "" }
    last["Total"] = total
    wallet.append(last)
    return wallet

def get_history(name):
    user = User.query.filter_by(username=name).first()
    transations = TransactionHistory.query.filter_by(user_id=user.id)
    history = []
    for row in transations:
        item_history = {"Symbol" : "" , "Shares" : "", "Price": "", "Cost" : "", "Transacted" : "" }    
        item_history["Symbol"] = row.symbol
        item_history["Shares"] = row.shares
        item_history["Price"] = row.price
        item_history["Cost"] = row.cost
        item_history["Transacted"] = (row.date_time).strftime("%Y-%m-%d %H:%M:%S")
        history.append(item_history)
    return history

def get_stocks(name):
    aux_wallet = raw_wallet(name)
    stocks = []
    for item in aux_wallet:
        element = (item["Symbol"], item["Symbol"])
        stocks.append(element)
    return stocks

def sell_validation(form, name):
    aux_wallet = raw_wallet(name)
    for item in aux_wallet:
        if form.symbol.data in item.values():
            if item["Shares"] >= form.shares.data:
               return True
            else:
                return False 
    return False



def sell_shares(form, name):
    if sell_validation(form, name):
        price = float(get_price(form.symbol.data))
        shares = int(form.shares.data)
        gain = price*shares
        shares = shares*(-1)
        user = User.query.filter_by(username=name).first()
        date_time = datetime.datetime.now()
        cash = user.cash + gain
        user.cash = cash
        db.session.commit()
        new_sell = TransactionHistory(user_id=user.id, symbol=(form.symbol.data).upper(), shares=shares,price=price,cost=gain,date_time=date_time)
        db.session.add(new_sell)
        db.session.commit()
        flash("You've sold successfully")
        return redirect(url_for('dashboard'))
    else:
        flash("not enough shares")
        return redirect(url_for('sell'))

