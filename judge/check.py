import os
import sys
from time import time


def make_result(jar, pk, testcase, tc, an, rs):
    try:
        testcases = [str(i) for i in range(testcase)]
        time_limit = 5
        for index in testcases:
            print('Test Case #{}'.format(index))
            start = time()
            os.system('java -jar {} < {}/input{}.txt > {}/answer{}.txt'.format(jar, tc, index, an, index))
            end = time()
            print('Running Time: {:.2f}sec'.format(end-start))
            fcor = open('{}/output{}.txt'.format(tc, index), 'r')
            fans = open('{}/answer{}.txt'.format(an, index), 'r')
            count = 0
            while True:
                count += 1
                lcor = fcor.readline()
                if lcor=='':
                    print('Correct')
                    break
                lans = fans.readline()
                if lcor!=lans:
                    print('Line', str(count)+":", 'Dismatch')
                    print(' ', lcor.rstrip(), '/', lans.lstrip().rstrip())
                    result = open('{}/{}.txt'.format(rs, pk), 'w')
                    result.write('Wrong Answer ({}:{})'.format(index, count))
                    result.close()
                    exit()
                    break
            fcor.close()
            fans.close()

            result = open('{}/{}.txt'.format(rs, pk), 'w')
            print(str((int(index)+1)*100//testcase)+'%')
            result.write('Check '+str((int(index)+1)*100//testcase)+'%')
            result.close()
        result = open('{}/{}.txt'.format(rs, pk), 'w')
        result.write('All Correct')
        result.close()
    except Exception as e:
        result = open('{}/{}.txt'.format(rs, pk), 'w')
        result.write('Error')
        result.close()
