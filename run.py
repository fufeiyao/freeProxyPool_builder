import sys
import io
from ProxyPool.schedule import Scheduler



sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s =Scheduler()
        s.run()
    except:
        print('failed')
        main()


if __name__ == '__main__':
    main()
