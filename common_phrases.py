from os import listdir
from os.path import isfile, join
import math


def multiple_replace(char_tuple_, string, replacer):
    for value in char_tuple_:
        string = string.replace(value, replacer)
    return string


def word_to_plural(word_):
    # note: returns a tuple of the original word and the new word
    if word_ == "i":
        return word_, word_
    elif word_[-1] != "s":
        return word_, word_ + "s"
    else:
        return word_, word_


def parse_non_important_words(sentence_list, to_remove):

    for i_ in range(len(sentence_list)):
        sentence_list[i_] = [x for x in sentence_list[i_] if x[0] not in to_remove]


def common_complementary_words(word_, sentence_list):
    plural_word = word_to_plural(word_)
    words_that_appear = {}
    for list_ in sentence_list:
        plural_list = []
        for words in list_:
            plural_list.append(words[1])
        if plural_word[1] in plural_list:
            visited = []
            for words in list_:

                if words[0] not in words_that_appear:
                    words_that_appear[words[0]] = 1
                elif words[0] not in visited:
                    words_that_appear[words[0]] += 1
                visited.append(words[0])
    wta_list = []
    for key, value in words_that_appear.iteritems():
        wta_list.append([key, value])

    wta_list = sorted(wta_list, key=lambda x: x[1], reverse=True)
    wta_list = [x for x in wta_list if x[0] != word_ and x[0] != plural_word[1]]
    top = []
    if len(wta_list) > 10:
        top = wta_list[:10]
    elif len(wta_list) > 0:
        top = wta_list[:len(wta_list)]
    else:
        top = []
    return top


def get_bigrams(sentence_data):
    bigrams = {}
    window_val = 5

    for sentence in sentence_data:

        for i in range(len(sentence)):
            window = []
            if i - window_val >= 0 and i + window_val < len(sentence):
                window = range(-window_val, window_val + 1)
            elif i - window_val >= 0:
                window = range(-window_val, len(sentence) - i)
            elif i + window_val < len(sentence):
                window = range(-i, window_val + 1)
            else:
                window = range(-i, len(sentence) - i)
            window = list(window)
            window.remove(0)

            if sentence[i][1] in bigrams:
                bigrams[sentence[i][1]][1] += 1
                visited_words = []
                for ind in window:
                    neighboring_word = sentence[i + ind]
                    if neighboring_word[1] in bigrams[sentence[i][1]][0] and neighboring_word[1] not in visited_words:
                        bigrams[sentence[i][1]][0][neighboring_word[1]] += 1
                        visited_words.append(neighboring_word[1])
                    elif neighboring_word[0] in bigrams[sentence[i][1]][0] and neighboring_word[0] not in visited_words:
                        bigrams[sentence[i][1]][0][neighboring_word[0]] += 1
                        visited_words.append(neighboring_word[0])
                    elif (neighboring_word[0][-1] == 's' and neighboring_word[0][:-1] in bigrams[sentence[i][1]][0] and
                          neighboring_word[0][:-1] not in visited_words):
                        data_to_copy = bigrams[sentence[i][1]][0][neighboring_word[0][:-1]]
                        bigrams[sentence[i][1]][0][neighboring_word[0]] = data_to_copy
                        del data_to_copy
                        bigrams[sentence[i][1]][0][neighboring_word[0]] += 1
                        visited_words.append(neighboring_word[0])
                    elif neighboring_word[0] not in bigrams[sentence[i][1]][0]:
                        bigrams[sentence[i][1]][0][neighboring_word[0]] = 1
                        visited_words.append(neighboring_word[0])
            else:
                if sentence[i][0] in bigrams:
                    bigrams[sentence[i][0]][1] += 1
                elif sentence[i][0][-1] == 's' and sentence[i][0][:-1] in bigrams:
                    data_to_copy = bigrams[sentence[i][0][:-1]]
                    bigrams[sentence[i][0]] = data_to_copy
                    del data_to_copy
                    bigrams[sentence[i][0]][1] += 1
                else:
                    bigrams[sentence[i][0]] = [{}, 1]

                visited_words = []

                for ind in window:

                    neighboring_word = sentence[i + ind]

                    if neighboring_word[1] in bigrams[sentence[i][0]][0] and neighboring_word[1] not in visited_words:
                        bigrams[sentence[i][0]][0][neighboring_word[1]] += 1
                        visited_words.append(neighboring_word[1])
                    elif neighboring_word[0] in bigrams[sentence[i][0]] and neighboring_word[0] not in visited_words:
                        bigrams[sentence[i][0]][0][neighboring_word[0]] += 1
                        visited_words.append(neighboring_word[0])
                    elif (neighboring_word[0][-1] == 's' and neighboring_word[0][:-1] in bigrams[sentence[i][0]] and
                          neighboring_word[0][-1] not in visited_words):
                        data_to_copy = bigrams[sentence[i][0]][neighboring_word[0][:-1]]
                        bigrams[sentence[i][0]][neighboring_word[0]] = data_to_copy
                        del data_to_copy
                        bigrams[sentence[i][0]][0][neighboring_word[0]] += 1
                        visited_words.append(neighboring_word[0])

                    elif neighboring_word[0] not in bigrams[sentence[i][0]][0]:
                        bigrams[sentence[i][0]][0][neighboring_word[0]] = 1
                        visited_words.append(neighboring_word[0])
            # if sentence[i][1] in bigrams:
            #     for ind in window:
            #         neighboring_word = sentence[i + ind]
            #
            #         if neighboring_word[1] in bigrams[sentence[i][1]]:
            #             bigrams[sentence[i][1]][neighboring_word[1]].append(ind)
            #         elif neighboring_word[0] in bigrams[sentence[i][1]]:
            #             bigrams[sentence[i][1]][neighboring_word[0]].append(ind)
            #         elif neighboring_word[0][-1] == 's' and neighboring_word[0][:-1] in bigrams[sentence[i][1]]:
            #             data_to_copy = bigrams[sentence[i][1]][neighboring_word[0][:-1]]
            #             bigrams[sentence[i][1]][neighboring_word[0]] = data_to_copy
            #             del data_to_copy
            #             bigrams[sentence[i][1]][neighboring_word[0]].append(ind)
            #         else:
            #             bigrams[sentence[i][1]][neighboring_word[0]] = []
            #             bigrams[sentence[i][1]][neighboring_word[0]].append(ind)
            # else:
            #     if sentence[i][0] in bigrams:
            #         pass
            #     elif sentence[i][0][-1] == 's' and sentence[i][0][:-1] in bigrams:
            #         data_to_copy = bigrams[sentence[i][0][:-1]]
            #         bigrams[sentence[i][0]] = data_to_copy
            #         del data_to_copy
            #
            #     else:
            #         bigrams[sentence[i][0]] = {}
            #     for ind in window:
            #         neighboring_word = sentence[i + ind]
            #
            #         if neighboring_word[1] in bigrams[sentence[i][0]]:
            #             bigrams[sentence[i][0]][neighboring_word[1]].append(ind)
            #
            #         elif neighboring_word[0] in bigrams[sentence[i][0]]:
            #             bigrams[sentence[i][0]][neighboring_word[0]].append(ind)
            #
            #         elif neighboring_word[0][-1] == 's' and neighboring_word[0][:-1] in bigrams[sentence[i][0]]:
            #             data_to_copy = bigrams[sentence[i][0]][neighboring_word[0][:-1]]
            #             bigrams[sentence[i][0]][neighboring_word[0]] = data_to_copy
            #             del data_to_copy
            #             bigrams[sentence[i][0]][neighboring_word[0]].append(ind)
            #
            #         else:
            #             bigrams[sentence[i][0]][neighboring_word[0]] = []
            #             bigrams[sentence[i][0]][neighboring_word[0]].append(ind)

    return bigrams


def organize_bigrams(sentence_data):

    bigram_list = []
    bg = get_bigrams(sentence_data)
    for word in bg.keys():

        for neighbor in bg[word][0].keys():
            if word != neighbor:
                bigram_count = bg[word][0][neighbor]
                word_count = bg[word][1]
                ratio = float(bigram_count) / float(word_count)
                if ratio >= 0.05 and word_count >= 5:
                    bigram_list.append([word, neighbor, ratio])

    bigram_list = sorted(bigram_list, key=lambda x: x[2], reverse=True)
    bl_without_weights = [[x[0], x[1]] for x in bigram_list]
    index = 1
    while index < len(bl_without_weights):
        if [bl_without_weights[index][1], bl_without_weights[index][0]] in bl_without_weights[:index]:
            del bl_without_weights[index]
        else:
            index += 1
    return bl_without_weights
    # bigram_dict = {}
    # bg = get_bigrams(sentence_data)
    # for key in bg.keys():
    #     word1 = key
    #     for key2 in bg[key].keys():
    #         if len(bg[key][key2]) - 1 > 0:
    #             word2 = key2
    #             words = word1 + "," + word2
    #
    #             mean = sum(bg[key][key2]) / len(bg[key][key2])
    #             sum_ = 0
    #             for i in range(len(bg[key][key2])):
    #                 sum_ += (bg[key][key2][i] - mean) ** 2
    #             variance = float(sum_ / (len(bg[key][key2]) - 1))
    #             sd = math.sqrt(variance)
    #             if sd > 1:
    #
    #                 bigram_dict[words] = sd
    #
    # bigram_list = []
    # for key, value in bigram_dict.iteritems():
    #     bigram_list.append([key, value])
    #
    # bigram_list = sorted(bigram_list, key=lambda x: x[1])
    # return bigram_list







def manipulate_data():
    # lines = []
    dir_path = "spoken"
    path_list= [f for f in listdir(dir_path) if isfile(join(dir_path, f)) and f[-4:] == ".txt"]
    sentence_word_lists = []

    for path in path_list:
        lines = []
        file_ = open("spoken/" + path, "r")
        for line in file_:
            if line.strip() != '':
                lines.append(line.strip())

        for i in range(len(lines)):
            char_tuple = ("%", "&", "'", "(", ")", "*", ";", "+", ",", "-", "/", "{", "}", "^", "<", ">", "=", "@",
                          "[", "]", ":", " ")
            lines[i] = multiple_replace(char_tuple, lines[i], "|")
            punctuation_tuple = ("!", "?", ".")
            lines[i] = multiple_replace(punctuation_tuple, lines[i], ".")

        lines = lines + lines
        for line in lines:
            punctuation_split = line.split(".")
            punctuation_split2 = []
            for i in range(len(punctuation_split)):
                if punctuation_split[i] != '':
                    punctuation_split2.append(punctuation_split[i])

            # for item in punctuation_split2:
            #     if "skirt" in item:
            #         print "yes1"

            for i in range(len(punctuation_split2)):
                punctuation_split2[i] = punctuation_split2[i].split('|')
                j = 0
                while j < len(punctuation_split2[i]):
                    if punctuation_split2[i][j] == '':
                        del punctuation_split2[i][j]
                    else:
                        j += 1
            # for item in punctuation_split2:
            #     for it in item:
            #         if it == "skirts":
            #             print "yes2"
            for sentence_words in punctuation_split2:
                sentence_word_lists.append(sentence_words)
        file_.close()

    for i in range(len(sentence_word_lists)):
        for j in range(len(sentence_word_lists[i])):
            sentence_word_lists[i][j] = list(word_to_plural(sentence_word_lists[i][j]))
            for k in range(2):
                sentence_word_lists[i][j][k] = sentence_word_lists[i][j][k].lower()



    remove = ['the', 'an', 'this', 'that', 'these', 'those', 'my', 'your', 'her', 'it', 'its', 'our', 'their',
              'and', 'as', 'to', 'of', 'we', 'you', 'me', 'in', 'on', 'so', 'is', 'with', 'were',
              'there', 've', '', '\"', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g',
              'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'they', 'was',  'don', "\"as", 'if']
    num_list = []
    for i in range(3000):
        num_list.append(str(i))
    parse_non_important_words(sentence_word_lists, remove)

    parse_non_important_words(sentence_word_lists, num_list)



    return sentence_word_lists


#
# common = common_complementary_words("nothing", manipulate_data())
# print(common)

# bigrs = get_bigrams(manipulate_data())
# print(bigrs)

# print manipulate_data()
print(organize_bigrams(manipulate_data()))

# bigrlist = organize_bigrams(manipulate_data())
# print bigrlist[:20]



