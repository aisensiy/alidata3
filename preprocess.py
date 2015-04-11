#!/usr/bin/env python
# encoding: utf-8

from csv import DictReader
from csv import DictWriter
import logging


logging.basicConfig(format='%(asctime)s-[%(levelname)s]: %(message)s',
                    level=logging.DEBUG)


def to_dict_format(fileobj, start_date, label_date):
    reader = DictReader(fileobj)
    all_keys = set()
    result = {}

    for idx, row in enumerate(reader):
        if idx % 10000 == 0:
            logging.info('[%d] processed in to dict format', idx)

        date = row['time'].split(' ')[0]
        uid_iid = (row['user_id'], row['item_id'])
        result.setdefault(uid_iid, {})
        if date < start_date or date > label_date or row['behavior_type'] in ['2', '3']:
            continue
        if date == label_date:
            if int(row['behavior_type']) == 4:
                result[uid_iid]['label'] = 1
        else:
            key = '%s_%s' % (row['behavior_type'], date)
            all_keys.add(key)
            result[uid_iid].setdefault(key, 0)
            result[uid_iid][key] += 1

    return all_keys, result


def remove_empty_uid_iid(result):
    counter = 0
    for key, value in result.iteritems():
        if value == {}
        del result[key]
        counter += 1
    logging.info('remove empty pairs [%d]', counter)
    return result


def to_csv(all_keys, result, fileobj):
    columns = ['user_id', 'item_id'] + sorted(list(all_keys)) + ['label']
    writer = DictWriter(fileobj, fieldnames=columns)
    writer.writeheader()
    counter = 0
    for uid_iid, data in result.iteritems():
        uid, iid = uid_iid
        new_dict = {'user_id': uid, 'item_id': iid}
        for column in columns:
            if column in ['user_id', 'item_id']:
                continue
            if column not in data:
                new_dict[column] = 0
            else:
                new_dict[column] = data[column]
        writer.writerow(new_dict)
        counter += 1
        if counter % 10000 == 0:
            logging.info('[%d] processed in to csv', counter)


if __name__ == '__main__':
    import sys
    import time
    start = time.time()
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    start_date = sys.argv[3]
    label_date = sys.argv[4]
    with open(inputfile) as f:
        keys, result = to_dict_format(f, start_date, label_date)
    logging.info('rows count: [%d]', len(result))
    result = remove_empty_uid_iid(result)
    with open(outputfile, 'w') as f:
        to_csv(keys, result, f)
    logging.info('costs: %s', str(time.time() - start))
