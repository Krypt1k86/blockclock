import json
import datetime
from urllib.request import Request, urlopen

url_dict = {
	'btc_blocks': 'https://api.blockchair.com/bitcoin/blocks',
	'bch_blocks': 'https://api.blockchair.com/bitcoin-cash/blocks',
	'btg_blocks': 'https://explorer.bitcoingold.org/insight-api/blocks',
	'btc_txid': 'https://api.blockchair.com/bitcoin/dashboards/transaction/',
	'bch_txid': 'https://api.blockchair.com/bitcoin-cash/dashboards/transaction/',
	'btg_txid': 'https://explorer.bitcoingold.org/insight-api/tx/'
}


def btcGet():
	with urlopen(url_dict['btc_blocks']) as data:
		source = data.read()
 
	btc_data = json.loads(source.decode('utf-8'))

	return btc_data

def bchGet():
	with urlopen(url_dict['bch_blocks']) as data:
		source = data.read()

	bch_data = json.loads(source.decode('utf-8'))

	return bch_data

def btgGet():
	req = Request(url_dict['btg_blocks'], headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()

	btg_data = json.loads(source.decode('utf-8'))

	return btg_data

def btgYesterday():
	btg_data = btgGet()
	prev = btg_data['pagination']['prev']

	return prev

def getBlockTimes(data):
	utc = data['data'][0]['time'][11:19]
	hour = utc[0:2]
	minute = utc[3:5]
	second = utc[6:8]
	timedelta = datetime.timedelta(hours=int(hour), minutes=int(minute)
		, seconds=int(second))
	blocktime_list = [utc, timedelta]

	return blocktime_list

def getBtgBlockTimes(data):
	timestamp_list = []
	utc_list = []
	count = 0

	try:
		while count < 10:
			for i in data['blocks'][count]:
				if i == 'time':
					timestamp_list.append(data['blocks'][count]['time'])
					count += 1
				else:
					pass
	except:
		pass

	count = 0

	if len(timestamp_list) < 10:
		prev = btgYesterday()
		btg_url = 'https://explorer.bitcoingold.org/insight-api/blocks?blockDate=' + prev
		req = Request(btg_url, headers={'User-Agent': 'Mozilla/5.0'})
		source = urlopen(req).read()

		btg_data = json.loads(source.decode('utf-8')) 

		while count < 10:
			for i in btg_data['blocks'][count]:
				if i == 'time':
					timestamp_list.append(btg_data['blocks'][count]['time'])
					count += 1
				else:
					pass

	for i in timestamp_list:
		btg_dt = datetime.datetime.utcfromtimestamp(i)
		utc_list.append(btg_dt)

	return utc_list

def getCurrentTimes():
	current_time = datetime.datetime.utcnow()

	return current_time

def lastBlock(data):
	x = getBlockTimes(data)
	z = getCurrentTimes()
	timevar = z - x[1]
	timestring = timevar.strftime("%H:%M:%S")

	return timestring

def lastBtgBlock(data):
	x = getBtgBlockTimes(data)
	z = getCurrentTimes()
	timevar = z - x[0]
	timestring = str(timevar)
	truncatetime = timestring[0:7]

	return truncatetime

def blockList(data):
	count = 0 
	block_list = []

	while count < 10:
		for i in data['data'][count]:
			if i == 'time':
				block_list.append(data['data'][count]['time'])
				count += 1
			else:
				pass

	return block_list

def blockTimeDiff(block_list):
	time_list = []
	datetime_list = []
	timediff_list = []

	head_block = 0
	trail_block = 1

	for i in block_list:
		time_list.append(i[11:19])

	for i in time_list:
		hour = i[0:2]
		minute = i[3:5]
		second = i[6:8]
		timedelta = datetime.timedelta(hours=int(hour), minutes=int(minute)
		, seconds=int(second))
		datetime_list.append(timedelta)

	try:
		for i in datetime_list:
			time_diff = datetime_list[head_block] - datetime_list[trail_block]
			timediff_list.append(time_diff)
			head_block += 1
			trail_block += 1
	except:
		pass

	return timediff_list

def btgBlockTimeDiff(block_list):
	timediff_list = []
	timestring_list = []

	head_block = 0
	trail_block = 1

	try:
		for i in block_list:
			time_diff = block_list[head_block] - block_list[trail_block]
			timediff_list.append(time_diff)
			head_block += 1
			trail_block += 1
	except:
		pass

	for i in timediff_list:
		block_string = str(i)
		format_string = block_string[0:7]
		timestring_list.append(format_string)

	return timestring_list

def btgBlockStrings(data):
	string_list = []

	for i in data:
		block_string = str(i)
		string_list.append(block_string)

	return string_list

def getBtcBlockHead(data):
	head_list = []
	hash_list = []
	hash_url = []
	count = 0

	while count < 10:
		for i in data['data'][count]:
			if i == 'id':
				head_list.append(data['data'][count]['id'])
				count += 1
			else:
				pass

	count = 0

	while count < 10:
		for i in data['data'][count]:
			if i == 'hash':
				hash_list.append(data['data'][count]['hash'])
				count += 1
			else:
				pass

	for i in hash_list:
		block_url = 'https://blockchair.com/bitcoin/block/'
		final_url = block_url + str(i)
		hash_url.append(final_url)

	headurl_list = [head_list, hash_url]

	return headurl_list

def getBchBlockHead(data):
	head_list = []
	hash_list = []
	hash_url = []
	count = 0

	while count < 10:
		for i in data['data'][count]:
			if i == 'id':
				head_list.append(data['data'][count]['id'])
				count += 1
			else:
				pass

	count = 0

	while count < 10:
		for i in data['data'][count]:
			if i == 'hash':
				hash_list.append(data['data'][count]['hash'])
				count += 1
			else:
				pass

	for i in hash_list:
		block_url = 'https://blockchair.com/bitcoin-cash/block/'
		final_url = block_url + str(i)
		hash_url.append(final_url)

	headurl_list = [head_list, hash_url]

	return headurl_list

def getBtgBlockHead(btg_data):
	head_list = []
	hash_list = []
	hash_url = []
	count = 0

	try:
		while count < 10:
			for i in btg_data['blocks'][count]:
				if i == 'height':
					head_list.append(btg_data['blocks'][count]['height'])
					count += 1
				else:
					pass
	except:
		pass

	count = 0

	if len(head_list) < 10:
		prev = btgYesterday()
		btg_url = 'https://explorer.bitcoingold.org/insight-api/blocks?blockDate=' + prev
		req = Request(btg_url, headers={'User-Agent': 'Mozilla/5.0'})
		source = urlopen(req).read()

		new_data = json.loads(source.decode('utf-8')) 

		while count < 10:
			for i in new_data['blocks'][count]:
				if i == 'height':
					head_list.append(new_data['blocks'][count]['height'])
					count += 1
				else:
					pass


	# while count < 10:
	# 	for i in btg_data['blocks'][count]:
	# 		if i == 'height':
	# 			head_list.append(btg_data['blocks'][count]['height'])
	# 			count += 1
	# 		else:
	# 			pass

	count = 0

	try:
		while count < 10:
			for i in btg_data['blocks'][count]:
				if i == 'hash':
					hash_list.append(btg_data['blocks'][count]['hash'])
					count += 1
				else:
					pass
	except:
		pass

	count = 0

	if len(hash_list) < 10:
		prev = btgYesterday()
		btg_url = 'https://explorer.bitcoingold.org/insight-api/blocks?blockDate=' + prev
		req = Request(btg_url, headers={'User-Agent': 'Mozilla/5.0'})
		source = urlopen(req).read()

		new_data = json.loads(source.decode('utf-8')) 

		while count < 10:
			for i in new_data['blocks'][count]:
				if i == 'hash':
					hash_list.append(new_data['blocks'][count]['hash'])
					count += 1
				else:
					pass

	# while count < 10:
	# 	for i in btg_data['blocks'][count]:
	# 		if i == 'hash':
	# 			hash_list.append(btg_data['blocks'][count]['hash'])
	# 			count += 1
	# 		else:
	# 			pass

	for i in hash_list:
		block_url = 'https://explorer.bitcoingold.org/insight/block/'
		final_url = block_url + str(i)
		hash_url.append(final_url)

	headurl_list = [head_list, hash_url]

	return headurl_list

def getBtcTxInfo(txid):
	btc_data = btcGet()

	with urlopen(url_dict['btc_txid'] + str(txid)) as data:
		source = data.read()

	btc_tx = json.loads(source.decode('utf-8'))

	block_id = btc_tx['data'][txid]['transaction']['block_id']
	tx_time = btc_tx['data'][txid]['transaction']['time']
	now = getCurrentTimes()
	tx_datetime = datetime.datetime.strptime(tx_time, '%Y-%m-%d %H:%M:%S')
	tx_age = now - tx_datetime

	if block_id == -1:
		confirmations = 0
	else:
		blockhead_list = getBtcBlockHead(btc_data)
		current_head = blockhead_list[0][0]
		confirmations = (current_head - block_id) + 1

	if block_id == -1:
		block_id = "Unconfirmed"

	txinfo_list = [block_id, confirmations, tx_age]

	return txinfo_list

def getBchTxInfo(txid):
	bch_data = bchGet()

	with urlopen(url_dict['bch_txid'] + str(txid)) as data:
		source = data.read()

	bch_tx = json.loads(source.decode('utf-8'))

	block_id = bch_tx['data'][txid]['transaction']['block_id']
	tx_time = bch_tx['data'][txid]['transaction']['time']
	now = getCurrentTimes()
	tx_datetime = datetime.datetime.strptime(tx_time, '%Y-%m-%d %H:%M:%S')
	tx_age = now - tx_datetime

	if block_id == -1:
		confirmations = 0
	else:
		blockhead_list = getBchBlockHead(bch_data)
		current_head = blockhead_list[0][0]
		confirmations = (current_head - block_id) + 1

	if block_id == -1:
		block_id = "Unconfirmed"

	txinfo_list = [block_id, confirmations, tx_age]

	return txinfo_list

def getBtgTxInfo(txid):
	btg_data = btgGet()

	req = Request(url_dict['btg_txid'] + str(txid), headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()

	btg_txid = json.loads(source.decode('utf-8'))

	block_id = btg_txid['blockheight']
	tx_time = btg_txid['time']
	confirmations = btg_txid['confirmations']
	now = getCurrentTimes()
	tx_datetime = datetime.datetime.utcfromtimestamp(tx_time)
	tx_age = now - tx_datetime

	if block_id == -1:
		height = "Unconfirmed"
	else:
		height = block_id

	txinfo_list = [height, confirmations, tx_age]

	return txinfo_list
