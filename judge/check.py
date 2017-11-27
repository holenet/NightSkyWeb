# python3

import os
import sys
from time import time

import daemon


def check(jar, pk, testcase, tc, an, rs):
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
            result.write('Checking '+str((int(index)+1)*100//testcase)+'%')
            result.close()
        result = open('{}/{}.txt'.format(rs, pk), 'w')
        result.write('All Correct')
        result.close()
    except Exception as e:
        print(e)
        result = open('{}/{}.txt'.format(rs, pk), 'w')
        result.write('Unknown Error')
        result.close()


if __name__=='__main__':
    with daemon.DaemonContext():
        arr = sys.argv
        check(arr[1], int(arr[2]), int(arr[3]), arr[4], arr[5], arr[6])
    arr = sys.argv
    check()
