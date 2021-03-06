from time import sleep
from multiprocessing.dummy import Pool as ThreadPool, Lock


class Account(object):
    def __init__(self, name, money=5000):
        self.name = name
        self.lock = Lock()
        self.money = money  # 设置一个初始金额


class Bank(object):
    tie_lock = Lock()

    @staticmethod
    def __get_hash(obj):
        return id(obj)  # hash_func(obj)

    @classmethod
    def transfer(p_from, p_to, money):
        """p_from：谁转账,p_to：转给谁,money:转多少"""
        from_hash = Bank.__get_hash(p_from)
        to_hash = Bank.__get_hash(p_to)

        # 规定：谁大先锁谁
        if from_hash > to_hash:
            with p_from.lock:
                p_from.money -= money
                sleep(1)  # 模拟网络延迟
                with p_to.lock:
                    p_to += money
        elif from_hash < to_hash:
            with p_to:
                p_to.money += money
                sleep(1)  # 模拟网络延迟
                with p_from:
                    p_from.money -= money
        # hash出现碰撞时处理：（可能性很低）
        else:
            # 平局的时候，大家一起抢一个中间锁，谁抢到谁先转账
            with Bank.tie_lock:
                with p_from.lock:
                    p_from.money -= money
                    sleep(1)  # 模拟网络延迟
                    with p_to.lock:
                        p_to.money += money


def main():
    xiaoming = Account("小明")
    xiaozhang = Account("小张")
    print(f"[互刷前]小明：{xiaoming.money},小张：{xiaozhang.money}")

    p = ThreadPool()
    p.apply_async(Bank.transfer, args=(xiaoming, xiaozhang, 1000))
    p.apply_async(Bank.transfer, args=(xiaozhang, xiaoming, 1000))
    p.close()
    p.join()

    print(f"[互刷后]小明：{xiaoming.money},小张：{xiaozhang.money}")


if __name__ == '__main__':
    main()
