import sqlite3
import json
from datetime import datetime

timeframe = '2018-05'
sql_transaction = [] # Because we don't want to go line by line, this would be much faster, all at once.

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

def create_table():
	c.execute("""CREATE TABLE IF NOT EXISTS parent_reply(
		parent_id TEXT PRIMARY KEY, 
		comment_id TEXT UNIQUE, 
		parent TEXT,
		comment TEXT,
		subreddit TEXT,
		unix INT,
		score INT)""")


def format_data(data):
	data = data.replace('\n', ' newlinechar ').replace('\r', ' newlinechar ').replace('"', "'")
	return data

def find_parent(parent_id):
	try:
		sql_query = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(parent_id)
		c.execute(sql_query)
		result = c.fetchone()
		if result != None:
			return result[0]
		else:
			return False
	except Exception as e:
		return False

# https://drive.google.com/open?id=1JzlXiX8UNhxAl9P9TqmT9Jv646l7BaLS

def transaction_bldr(sql_query):
    global sql_transaction
    sql_transaction.append(sql_query)
    if len(sql_transaction) > 5000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

def find_existing_score(parent_id):
	try:
		sql_query = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(parent_id)
		c.execute(sql_query)
		result = c.fetchone()
		if result != None:
			return result[0]
		else: 
			return False
	except Exception as e:
		return False

def acceptable(data):
	if len(data.split(' ')) > 50 or len(data) < 1:
		return False
	elif len(data) > 1200:
		return False
	elif data = '[deleted]' or data = '[removed]':
		return False
	else:
		return True

def sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
    try:
        sql_query = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent_data = ?, body = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id = ?;""".format(parent_id, comment_id, parent_data, body, subreddit, int(created_utc), score, parent_id)
        transaction_bldr(sql_query)
    except Exception as e:
        print('s-PARENT insertion', str(e))

def sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
    try:
        sql_query = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}", "{}", "{}", "{}", "{}", {}, {});""".format(parent_id, comment_id, parent_data, body, subreddit, int(created_utc), score, parent_id)
        transaction_bldr(sql_query)
    except Exception as e:
        print('s-NO_PARENT insertion', str(e))

def sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score):
    try:
        sql_query = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}", "{}", "{}", "{}", {}, {});""".format(parent_id, comment_id, body, subreddit, int(created_utc), score, parent_id)
        transaction_bldr(sql_query)
    except Exception as e:
        print('s0 insertion', str(e))


if __name__ == '__main__':
	create_table()
	row_counter = 0
	paired_rows = 0

	with open('/Users/bobbyrathore/Documents/Jupyter Notebook/ChatBot/reddit_data/{}/RC_{}'.format(timeframe.split('-')[0], timeframe), buffering=1000) as f:
		for row in f:
			row_counter += 1
			row = json.loads(row)
			parent_id = row['parent_id']
			comment_id = row['name']
			body = format_data(row['body'])
			created_utc = row['created_utc']
			score = row['score']
			subreddit = row['subreddit']
			parent_data = find_parent(parent_id)


			if score is None:
				continue

			if score >= 2 && acceptable(body):
				existing_comment_score = find_existing_score(parent_id)
				if existing_comment_score:
					if score > existing_comment_score:
						sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
				else:
					if parent_data:
						sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
						paired_rows += 1
					else:
						sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)

			if row_counter % 100000 == 0:
				print('Total rows read: {}, Paired rows read: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now())))








