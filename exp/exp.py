from multiprocessing import Pool
import time, os, requests,argparse
import numpy as np

def f(args, debug=False):
    (url, filepath) = args
    start_time = time.time()
    result = requests.post(url, files = {'file':open(filepath,'rb')})
    end_time = time.time()
    if debug:
        print(result.text)
    return end_time - start_time

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Experimental Scripts')
    parser.add_argument('-i', help='interface url', default='http://127.0.0.1:20000/api/v1/classifier')
    parser.add_argument('-f', help='file path', default='cat.png')
    parser.add_argument('-t', help='number of processes', type=int, default=10)
    args = parser.parse_args()

    p = Pool(args.t)
    result = np.array(p.map(f, [(args.i, args.f) for x in range(args.t)]))

    print("Avg response time(s): \t\t" + str(np.mean(result)))
    print("Standard deviation(s): \t\t" + str(np.std(result)))
