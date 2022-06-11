import time
from quant.mail import send
from utils.BinanceAPI import BinanceAPI
from utils.authorization import api_key, api_secret
from data.runBetData import RunBetData

binan = BinanceAPI(api_key, api_secret)
runbet = RunBetData()


class RunMain:
    def loop_run(self):
        while True:
            cur_market_price = binan.get_ticker_price(
                runbet.get_cointype())  # 当前交易对市价
            grid_buy_price = runbet.get_buy_price()  # 当前网格买入价格
            grid_sell_price = runbet.get_sell_price()  # 当前网格卖出价格
            quantity = runbet.get_quantity()   # 买入量
            step = runbet.get_step()  # 当前步数

            if grid_buy_price >= cur_market_price:   # 是否满足买入价
                res = binan.buy_limit(
                    self.coinType, quantity, grid_buy_price)
                if res['orderId']:  # 挂单成功
                    # 修改data.json中价格、当前步数
                    runbet.modify_price(grid_buy_price, step+1)
                    time.sleep(60*2)  # 挂单后，停止运行1分钟
                else:
                    break
            elif grid_sell_price < cur_market_price:  # 是否满足卖出价
                if step == 0:  # setp=0 防止踏空，跟随价格上涨
                    runbet.modify_price(grid_sell_price, step)
                else:
                    res = binan.sell_limit(
                        self.coinType, runbet.get_quantity(False), grid_sell_price)
                    if res['orderId']:
                        runbet.modify_price(grid_sell_price, step - 1)
                        time.sleep(60*2)  # 挂单后，停止运行1分钟
                    else:
                        break
            else:
                print("当前市价：{market_price}。未能满足交易,继续运行".format(
                    market_price=cur_market_price))


if __name__ == '__main__':
    instance = RunMain()
    try:
        instance.loop_run()
    except Exception as e:
        send('报警：量化服务停止', '错误原因'+str(e))
