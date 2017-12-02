#coding:gbk
from random import randint

def guess_num():
    all_data = []
    all_player = []
    with open('guessdata.txt') as f:
        for line in f.readlines():
            all_data.append(list(line.strip().split()))
    for i in all_data:
        all_player.append(i[0])
    print 'all_data:%s' % all_data
    print 'all_player:%s' % all_player
    player=raw_input('输入你的ID:')
    exist_player=False
    if player in all_player:
        exist_player=True
        print '欢迎回来 %s,祝你游戏愉快！' % player
    else:
        print '欢迎 %s,祝你游戏愉快！' % player
    all = []
    times = 0
    guess = True
    random_num = randint(1, 100)
    while guess:
        try:
            you_num = int(input('请输入100以内的数字:'))
        except:
            print '输入错误，请输入100以内的数字！'
            continue
        print '第%s次' % (times+1)
        if you_num > random_num:
            times += 1
            print "%s 大了" % you_num
        elif you_num < random_num:
            times += 1
            print "%s 小了" % you_num
        else:
            times += 1
            print "恭喜猜中了 %d " % you_num
            all.append(times)
            times = 0
            isgoon = raw_input('想要再次猜数吗,Y or N:')
            if isgoon == 'Y' or isgoon == 'Yes' or isgoon == 'yes' or isgoon == 'y':
                guess = True
                random_num = randint(1, 100)
            else:
                guess = False
                print "不再继续，下面是你的成绩。"
                print    "现在你已经猜了 %s 轮，平均每轮需要 %s 猜中" % (all.__len__(), sum(all) / all.__len__())
                if exist_player:
                    #将存在用户的数据的list更新
                    play_index=all_player.index(player)
                    exist_all=int(all_data[play_index][1])+all.__len__()
                    exist_alltimes=int(all_data[play_index][1])*int(all_data[play_index][2])+sum(all)
                    all_data[play_index]=[player,exist_all,exist_alltimes/exist_all]
                else:
                    #用户猜数数据新增此用户的数据
                    all_data.append([player,all.__len__(),sum(all) / all.__len__()])
    #将数据重新写入用户数据记录文件
    with open('guessdata.txt','w') as f:
        for user in all_data:
            for x in user:
                user[user.index(x)]=str(x)
            userdata=' '.join(user)
            f.write(userdata)
            f.write('\n')

if __name__ == '__main__':
    guess_num()
