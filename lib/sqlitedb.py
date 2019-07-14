import web

db = web.database(dbn='sqlite',
                  db='AuctionBase'  # TODO: add your SQLite database filename
                  )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!


def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database


def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database


def getTime():
    query_string = 'select Time from CurrentTime'

    t = db.transaction()
    try:
        results = query(query_string)
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()
    return results[0]['Time']


def updateCurrTime(oldTime, inputTime):
    sql = "UPDATE CurrentTime SET Time = '" + \
        inputTime + "' WHERE Time = '" + oldTime + "'"

    t = db.transaction()
    try:
        db.query(sql)
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()



# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info


def query(query_string, vars={}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    try:
        query_string = 'select * from Items where item_ID = $itemID'
        result = query(query_string, {'itemID': item_id})
        return result[0]
    except Exception as e:
        print(str(e))
        return None
# TODO: additional methods to interact with your database,

def add_bid(item_id, user_id, price):
    # TODO insert a bid to the database
    t = db.transaction()
    try:
        currtime = getTime()
        # Check if the item_id violates the foreign key constraint
        item = getItemById(item_id)['Name']
        if item == None:
            print("Invalid itemID! No such item exists")
            return False
        else:
            print("Item: ", item)

        # Check if the user_id violates the foreign key constraint
        user = getUser(user_id)
        if user == None:
            print("Invalid userID! No such user exists")
            return False
        else:
            print("User Name: ", user)

        # Check if the user input price is higher than current price
        currentPrice = getCurrentPrice(item_id)
        if price > currentPrice:
            print("Invalid input on Amount! must be higher than current amount! \n")
            print("Current amount: ", currentPrice)
            return False
        else:
            print("Your bid amount: ", price)
        db.insert("Bids", ItemID=item_id, UserID=user_id, Amount=price, Time=currtime)

        #? need to check current time?
    except Exception as e:
        t.rollback()
        print str(e)
        print "??????????????????????????????????"
        return False             
    else:
        t.commit()
        return True

def getCurrentPrice(item_id):
    try:
        query_string = 'select Currently from Items where item_ID = $itemID'
        result = query(query_string, {'itemID': item_id})
        return result[0]["Currently"]
    except Exception as e:
        print(str(e))
        return None

# returns the user with specific user_id. return None if no such user exists
def getUser(user_id):
    try:
        query_string = 'select * from Users where User_ID = $userID'
        result = query(query_string, {'userID': user_id})
        return result[0]["Name"]
    except Exception as e:
        print(str(e))
        return None


##############################################################


# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getBidsByItemId(item_id):
    if (item_id == ''):
        return None
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = "select * from Items where ItemID = " + item_id 
    t = db.transaction()
    try:
        result = query(query_string, {'ItemID': item_id})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()
    return result

# defined by me
# returns a single item specified by the user's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!

def getUserById(user_id):
    if (user_id == ''):
        return None
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = "select * from Items where Seller_UserID = " + user_id 
    t = db.transaction()
    try:
        result = query(query_string, {'UserID': user_id})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()
    return result
# defined by me
# returns a single item specified by the price in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!

def getMinPrice(min_price):
    if (min_price == ''):
        return None

    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = "select * from Items where currently >= " + min_price
    t = db.transaction()
    try:
        result = query(query_string, {'minPrice': min_price})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()

    return result

# defined by me
# returns a single item specified by the price in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!

def getMaxPrice(max_price):
    if (max_price == ''):
        return None
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = "select * from Items where currrently <= " + max_price 
    t = db.transaction()
    try:
        result = query(query_string, {'maxPrice': max_price})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()
    return result

def getStatus(status):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    if status == "open":
        query_string = "select * from currenttime, items where currenttime.time >= items.started and currenttime.time <= items.ends"
    if status == "close":
        query_string = "select * from items, currenttim where (currenttime.time > items.ends or items.currently >= items.buy_price)"
    if status == "notStarted":
        query_string = "select * from items, currenttime where currenttime.time < items.started"
    else: 
        query_string = "select * from items, currenttime"
   
    t = db.transaction()
    try:       
        result = query(query_string, {'Status': status})
    except Exception as e:
        t.rollback()
        print str(e)
    else:
        t.commit()
    return result