from multiprocessing import Pool


def hello(name_and_num):
    name = name_and_num[0]
    num = name_and_num[1]
    print("hello, {}! {}".format(name, num))

def hello(name, num):
    print("hello, {}! {}".format(name, num))

name = ["bob", "mary", "sam", "john", "tom", "adam", "penny", "yoshinori", "yuta", "tatsuya", "saul", "taskia", "kouhei", "misa"]

#並列
sample_args = []
for name_ in name:
    for i in range(5):
        sample_args.append((name_, i))

with Pool(processes=3) as pool:
    pool.map(hello, sample_args)

#単純なfor文
for name_in name:
    for i in range(5):
        print(hello_(name, num))
