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
    player=raw_input('�������ID:')
    exist_player=False
    if player in all_player:
        exist_player=True
        print '��ӭ���� %s,ף����Ϸ��죡' % player
    else:
        print '��ӭ %s,ף����Ϸ��죡' % player
    all = []
    times = 0
    guess = True
    random_num = randint(1, 100)
    while guess:
        try:
            you_num = int(input('������100���ڵ�����:'))
        except:
            print '�������������100���ڵ����֣�'
            continue
        print '��%s��' % (times+1)
        if you_num > random_num:
            times += 1
            print "%s ����" % you_num
        elif you_num < random_num:
            times += 1
            print "%s С��" % you_num
        else:
            times += 1
            print "��ϲ������ %d " % you_num
            all.append(times)
            times = 0
            isgoon = raw_input('��Ҫ�ٴβ�����,Y or N:')
            if isgoon == 'Y' or isgoon == 'Yes' or isgoon == 'yes' or isgoon == 'y':
                guess = True
                random_num = randint(1, 100)
            else:
                guess = False
                print "���ټ�������������ĳɼ���"
                print    "�������Ѿ����� %s �֣�ƽ��ÿ����Ҫ %s ����" % (all.__len__(), sum(all) / all.__len__())
                if exist_player:
                    #�������û������ݵ�list����
                    play_index=all_player.index(player)
                    exist_all=int(all_data[play_index][1])+all.__len__()
                    exist_alltimes=int(all_data[play_index][1])*int(all_data[play_index][2])+sum(all)
                    all_data[play_index]=[player,exist_all,exist_alltimes/exist_all]
                else:
                    #�û����������������û�������
                    all_data.append([player,all.__len__(),sum(all) / all.__len__()])
    #����������д���û����ݼ�¼�ļ�
    with open('guessdata.txt','w') as f:
        for user in all_data:
            for x in user:
                user[user.index(x)]=str(x)
            userdata=' '.join(user)
            f.write(userdata)
            f.write('\n')

if __name__ == '__main__':
    guess_num()
