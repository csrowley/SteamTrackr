import sqlite3

class Wishlist:
    def __init__(self, user, title, price, link):
        self.user = user
        self.title = title
        #self.initial_price = initial_price
        self.price = price
        self.link = link


conn = sqlite3.connect('user_wishlists.db')
c = conn.cursor()

def insert_wish_list(wish):
    with conn:
        c.execute("INSERT INTO wishlist VALUES (:user, :title, :price, :link)",
                {'user': wish.user, 'title': wish.title, 'price': wish.price, 'link': wish.link})


def get_wish_by_user(username):
    c.execute("SELECT * FROM wishlist WHERE user=:user", {'user': username})
    return(c.fetchall())

def update_game_price(wish, price):
    with conn:
        c.execute("UPDATE wishlist SET price = :price WHERE user = :user AND price = :price",
                  {'user': wish.user, 'price': wish.price})

def remove_a_wish(username, gametitle):
    with conn:
        c.execute("DELETE from wishlist WHERE user= :user AND title = :title", 
                  {'user': username, 'title': gametitle})

def remove_all_wish(username):
    with conn:
        c.execute("DELETE from wishlist WHERE user= :user", {'user': username})

def number_entries_from_user(username):
    with conn:
        c.execute("SELECT * FROM wishlist where user=:user", {'user': username})
    rows = c.fetchall()
    return len(rows)

async def close_connection():
    conn.close()

'''c.execute("""CREATE TABLE wishlist (
          user text,
          title text,
          price real,
          link text
          )""") 
'''

print("connected to database")