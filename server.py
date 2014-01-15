import time
import zmq
import json

def main():
    with open('data.jsons', 'a') as f:
        zmqc = zmq.Context()
        zmqs = zmqc.socket(zmq.PULL)
        zmqs.bind('tcp://*:4324')
        while True:
            d = zmqs.recv_json()
            print 'Message ...'
            if tuple(sorted(d)) != tuple(map(unicode, (
                    u'N', u'duration', u'initial', u'r', u's', u'xs'))):
                print '  Invalid keys.   Skipping ...'
                continue
            for k, t in {'N': int,
                         'duration': float,
                         'initial': list,
                         'what', basestring,
                         'r': list,
                         's': list,
                         'xs': list}.iteritems():
                if not isinstance(d[k], t):
                    print '  %s is not of type %s. Skipping ...' % (
                            k, str(t))
                    continue
            n = d['N'] * 8 * 2
            for k, l in {'initial': n,
                         'xs': n,
                         'r': 4,
                         's': 4}.iteritems():
                if not len(d[k]) == l:
                    print '  %s is of wrong length.  Skipping ...' % k
                    continue
                for x in d[k]:
                    if not isinstance(x, float):
                        print '  %s contains a non float.  Skipping' % k
                        continue
            d['timestamp'] = time.time()
            f.write(json.dumps(d))
            f.write('\n')
            f.flush()
            print '  ok'

if __name__ == '__main__':
    main()

# vim: sw=4 ts=4 sts=4
