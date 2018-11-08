from flask import Flask, render_template, request, redirect, url_for, flash, Markup
import blockclock
app = Flask(__name__)
app.secret_key = 'super_secret_key_here'

@app.route('/', methods=["GET", "POST"])
def homepage():
	try:
		btc_data = blockclock.btcGet()
		bch_data = blockclock.bchGet()
		btg_data = blockclock.btgGet()
	except:
		return redirect(url_for('error'))

	try:
		if request.method == "POST":
			raw_txid = request.form['btc-txid']
			clean_txid = raw_txid.strip()
			tx_info = blockclock.getBtcTxInfo(clean_txid)
			age = str(tx_info[2])
			stripped_age = age[:-7]
			message = Markup("BTC Transaction " + clean_txid + ":" """
				<ul>
				<li>Confirmations: <strong>""" + str(tx_info[1]) + """</strong></li>
				<li>Age: <strong>""" + stripped_age + """</strong></li>
				<li>Height: <strong>""" + str(tx_info[0]) + """</strong></li>
				</ul> """ )
			flash(message)
	except:
		pass

	try:
		if request.method == "POST":
			raw_txid = request.form['bch-txid']
			clean_txid = raw_txid.strip()
			tx_info = blockclock.getBchTxInfo(clean_txid)
			age = str(tx_info[2])
			stripped_age = age[:-7]
			message = Markup("BCH Transaction " + clean_txid + ":" """
				<ul>
				<li>Confirmations: <strong>""" + str(tx_info[1]) + """</strong></li>
				<li>Age: <strong>""" + stripped_age + """</strong></li>
				<li>Height: <strong>""" + str(tx_info[0]) + """</strong></li>
				</ul> """ )
			flash(message)
	except:
		pass

	try:
		if request.method == "POST":
			raw_txid = request.form['btg-txid']
			clean_txid = raw_txid.strip()
			tx_info = blockclock.getBtgTxInfo(clean_txid)
			age = str(tx_info[2])
			stripped_age = age[:-7]
			if tx_info[1] == 0:
				stripped_age = blockclock.lastBtgBlock(btg_data)
			message = Markup("BTG Transaction " + clean_txid + ":" """
				<ul>
				<li>Confirmations: <strong>""" + str(tx_info[1]) + """</strong></li>
				<li>Age: <strong>""" + stripped_age + """</strong></li>
				<li>Height: <strong>""" + str(tx_info[0]) + """</strong></li>
				</ul> """ )
			flash(message)
	except:
		pass

	w = blockclock.getBtgBlockTimes(btg_data)
	x = blockclock.getBlockTimes(btc_data)
	y = blockclock.getBlockTimes(bch_data)
	z = str(blockclock.getCurrentTimes())

	btc_lastbt = str(x[0])
	bch_lastbt = str(y[0])
	current_timestring = z[11:19]
	current_datestring = z[0:10]

	btc_currentbt = blockclock.lastBlock(btc_data)
	bch_currentbt = blockclock.lastBlock(bch_data)
	btg_currentbt = blockclock.lastBtgBlock(btg_data)

	btc_blocklist = blockclock.blockList(btc_data)
	bch_blocklist = blockclock.blockList(bch_data)
	btg_blocklist = blockclock.btgBlockStrings(w)

	btc_headlist = blockclock.getBtcBlockHead(btc_data)
	bch_headlist = blockclock.getBchBlockHead(bch_data)
	btg_headlist = blockclock.getBtgBlockHead(btg_data)

	btc_timelist = blockclock.blockTimeDiff(btc_blocklist)
	bch_timelist = blockclock.blockTimeDiff(bch_blocklist)
	btg_timelist = blockclock.btgBlockTimeDiff(w)

	return render_template('main.html',  
		current_timestring=current_timestring, btc_currentbt=btc_currentbt, 
		bch_currentbt=bch_currentbt, btc_blocklist=btc_blocklist, 
		bch_blocklist=bch_blocklist, btc_timelist=btc_timelist, 
		bch_timelist=bch_timelist, btg_currentbt=btg_currentbt,
		btg_timelist=btg_timelist, btg_blocklist=btg_blocklist,
		current_datestring=current_datestring, btc_headlist=btc_headlist,
		bch_headlist=bch_headlist, btg_headlist=btg_headlist)

@app.route('/fetch_error')
def error():
	z = str(blockclock.getCurrentTimes())
	current_timestring = z[11:19]
	current_datestring = z[0:10]
	return render_template('error.html', current_timestring=current_timestring,
		current_datestring=current_datestring)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=True)
