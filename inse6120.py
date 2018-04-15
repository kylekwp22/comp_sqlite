import sqlite3
import sys

def sql_js_dump(sqlite_file):
	
	#sqlite_file = 'crawl-data-mcdo2.sqlite'    # name of the sqlite database file
	table_name = 'javascript'  # name of the table to be created
	table_name2= 'javascript_cookies'
	column_1 = 'func_name' # name of the column
	column_2 = 'visit_id' # name of the column
	idf = 'script_url'  # column data type
	idf2 = 'value'


	conn = sqlite3.connect(sqlite_file)
	conn.text_factory = str
	c = conn.cursor()
	c.execute('SELECT visit_id , script_url FROM {tn} WHERE length({cn}) > 0 and visit_id>=0 and visit_id < 59 '.\
			format(tn=table_name, cn=column_1))
	
	injected_js=[r for r in c.fetchall()]

	c.execute('SELECT visit_id , value FROM {tn} WHERE visit_id >= 0 and visit_id < 59'.\
			format(tn=table_name2))
	
	injected_cookies=[r for r in c.fetchall()]
	
	conn.commit()
	conn.close()
	ret =[]
	ret.append(injected_js)
	ret.append(injected_cookies)
	return ret


def main():
	#dump_home = sql_js_dump('crawl-data-home2.sqlite')
	#dump_public = sql_js_dump('crawl-data-mcdo2.sqlite')
	if len(sys.argv) >= 3:
		home = sys.argv[1]
		public = sys.argv[2]
		print (home +' vs '+public)
	else:
		print('usage : python inse6120.py name_of_sqlite_home.sqlite name_of_sqlite_public.sqlite')
		return
	dump_home = sql_js_dump(home)
	dump_public = sql_js_dump(public)
	
	js_from_home = dump_home[0]
	js_from_public = dump_public[0]

	cookies_from_home = dump_home[1]
	cookies_from_public = dump_public[1]


	injected_js_from_public = list(set(js_from_public) - set(js_from_home))
 
	#print(injected_js_from_public)
	f = open('injected_js.txt','w')
	for row in injected_js_from_public:
		f.write(str(row[0])+':  ' + row[1] + '\n\n')
	f.close()

	injected_cookies_from_public = list(set(cookies_from_public) - set(cookies_from_home))
	f2 = open('injected_cookies.txt','w')
	for row in injected_cookies_from_public:
		f2.write(str(row[0])+':  ' + row[1] + '\n\n')
	f2.close()

if __name__ == "__main__":
	main()