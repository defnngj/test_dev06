import threading
from time import ctime, sleep, time


def super_player(name, t):
    print(f"play {name} - {ctime()}")
    sleep(t)


play_list = [
    ["孤勇者.mp3", 3],
    ["四海.mov", 5],
    ["xxx.mov", 6]
]

threads = []
for play in play_list:
    t = threading.Thread(target=super_player, args=(play[0], play[1]))
    threads.append(t)


if __name__ == '__main__':
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("all over %s" %ctime())



