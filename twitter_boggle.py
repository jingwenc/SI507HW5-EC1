import hw5_twitter
import sys

username1=sys.argv[1]
username2=sys.argv[2]
num_tweets=sys.argv[3]

freq_user1=hw5_twitter.frequency_of_words(username1,num_tweets)
freq_user2=hw5_twitter.frequency_of_words(username2,num_tweets)


common_list=[]
for i in freq_user1:
    for j in freq_user2:
        if i[0] == j[0]:
            num=0
            num=i[1]+j[1]
            common_list.append((j[0],num))

def diffe_list(sample_list,common_list):
    word_sample_list=[]
    for i in sample_list:
        word_sample_list.append(i[0])
    word_common_list=[]
    for j in common_list:
        word_common_list.append(j[0])
    word_diff_list=list(set(word_sample_list)-set(word_common_list))
    diff_list=[]
    for i in sample_list:
        for j in word_diff_list:
            if i[0] == j:
                diff_list.append(i)
    return diff_list

diff_list1=diffe_list(freq_user1,common_list)
diff_list2=diffe_list(freq_user2,common_list)
diff_list=diff_list1+diff_list2

top_common_list=hw5_twitter.top_five(common_list)
top_diff_list=hw5_twitter.top_five(diff_list)

print(top_common_list)
print(top_diff_list)
