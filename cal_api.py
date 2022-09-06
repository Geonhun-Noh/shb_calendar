from flask import Flask, jsonify,request, session, render_template, redirect, url_for, send_from_directory, flash,send_file
from utils.common_logs import _logger as logger
import decimal
import pytz
import datetime
import requests
from Database import Database

app = Flask(__name__)

def get_now_with_format(date_format):
    try:
        date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime(date_format)
    except Exception as e:
        date_now = None
    finally:
        return date_now

@app.route('/')
@app.route('/schedule', methods=['Get','POST'])
def insert_schedule():
    #TODO 로그인 SESSION에서 id 가져오기 
    user_id = '22101802'
    tag = 1
    memo = '메롱'

    # if request.method == 'POST':
    #     dept = request.form('dept')
    #     start_date = request.form('start_date')
    #     end_date = request.form('end_date')
    items='None'
    try:
        logger.info(1)
        with Database() as db:
            logger.info(2)
            items = db.select_user() # 리스트 조회
            logger.info('DB TEST SUCCESS : {}'.format(items))
    except Exception as e:
        logger.info(3)
        logger.error("schedule : {}".format(e))   

    return items

# @app.route('/getMonthlyAccountsData', methods=['Get'])
# def getMonthlyAccountsData():
#     print("SESSION : ",session)
#     _dept_no = session['jumCd']
#     _year = get_now_with_format('%Y')
#     if 'id' not in session:
#         return redirect(url_for('login'))
#     try:
#         with Database() as db:
#             month_accounts = db.select_month_accounts(_dept_no,_year) # 리스트 조회
#             converted_accounts = []
#             for account in month_accounts:
#                 new_account = []
#                 for val in account:
#                     new_val = val
#                     if type(val) is decimal.Decimal:
#                         new_val = int(val)
#                         new_account.append(new_val)
#                 converted_accounts.append(new_account)
#     except Exception as e:
#         logger.error("select_monthly_accounts_info : {}".format(e))
#     # logger.info("month accounts : {}".format(converted_accounts))
#     return jsonify(accounts=converted_accounts)


if __name__ == "__main__":
    # Jinja2 environment add extension for break
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = 'cloud~#'  # todo get key in os.environ
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=8000, debug=True)
    except Exception as e:
        logger.debug('app.run error')
        logfile.error(e)