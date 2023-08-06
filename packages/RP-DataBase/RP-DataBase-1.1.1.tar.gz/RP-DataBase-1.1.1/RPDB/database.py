import base64
import hashlib
import json
import os.path
import pickle
import random
import threading
from time import sleep


class OldRPDB:

    def __init__(self, path, auto_save=True):
        self.path = path
        if os.path.exists(path):
            self.db_json = json.load(open(self.path, 'r', encoding='utf8'))
        else:
            self.db_json = {}
        self.auto_save = auto_save

    def set(self, key, value):
        if type(value) != str and \
                type(value) != int and \
                type(value) != list and \
                type(value) != dict and \
                type(value) != bool:
            self.db_json[key] = {'DBMark&': 'pickle', 'data': base64.b64encode(pickle.dumps(value)).decode('utf8')}

        else:
            if type(value) == dict:
                if 'DBMark&' in value:
                    raise "Do not write 'DBMark&' to the dict"
            self.db_json[key] = value

    def get(self, key):
        if type(self.db_json[key]) == dict:
            if 'DBMark&' in self.db_json[key]:
                if self.db_json[key]['DBMark&'] == 'pickle':
                    return pickle.loads(base64.b64decode(self.db_json[key]['data']))

        return self.db_json[key]

    def exists(self, key):
        return key in self.db_json

    def dump(self):
        json.dump(self.db_json, open(self.path, 'w', encoding='utf8'))

    def getall(self):
        return self.db_json.keys()

    def rem(self, key):
        del self.db_json[key]
        self.dump()


class RPDB:
    def __init__(self, path, slice_multiplier=1):
        self.path = path
        self.dbs = {}
        self.slice_multiplier = slice_multiplier
        self.set_list = []
        self.lock = threading.Lock()

        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(os.path.join(self.path, 'all.keys')):
            self.keys = set(json.load(open(os.path.join(self.path, 'all.keys'), 'r', encoding='utf8'))['keys'])
        else:
            self.keys = set([])

        threading.Thread(target=self._recycle_thread, daemon=True).start()

    def _recycle_thread(self):
        while True:
            sleep(3)
            del_list = []
            for key in self.dbs:
                self._save_slice(key)
                self.dbs[key]['vitality_value'] -= len(self.dbs) / 2 + 1
                if self.dbs[key]['vitality_value'] <= 0:
                    del_list.append(key)

            for key in del_list:
                del self.dbs[key]
            try:
                json.dump({'keys': list(self.keys)}, open(os.path.join(self.path, 'all.keys'), 'w', encoding='utf8'))
            except Exception as err:
                print(err)

    def get_key_hash(self, key):
        return hashlib.sha1(key.encode('utf8')).hexdigest()[:self.slice_multiplier]

    def dump(self):
        for key in self.dbs:
            self._save_slice(key)
        try:
            json.dump({'keys': list(self.keys)}, open(os.path.join(self.path, 'all.keys'), 'w', encoding='utf8'))
        except Exception as err:
            print(err)

    def _load_slice(self, key):
        sha1_name = self.get_key_hash(key)
        slice_path = os.path.join(self.path, 'slices', sha1_name + '.json')
        if sha1_name not in self.dbs:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            if os.path.exists(slice_path):
                self.dbs[sha1_name] = {'vitality_value': 16, 'data': json.load(open(slice_path, 'r', encoding='utf8'))}
            else:
                self.dbs[sha1_name] = {'vitality_value': 16, 'data': {}}
        else:
            if self.dbs[sha1_name]['vitality_value'] <= 160:
                self.dbs[sha1_name]['vitality_value'] += 16

    def _save_slice(self, slice_name):
        if not os.path.exists(os.path.join(self.path, 'slices')):
            os.makedirs(os.path.join(self.path, 'slices'))
        slice_path = os.path.join(self.path, 'slices', slice_name + '.json')
        json.dump(self.dbs[slice_name]['data'], open(slice_path, 'w', encoding='utf8'))

    def set(self, key, value):
        self._load_slice(key)
        self.keys.add(key)

        value_pickle = base64.b64encode(pickle.dumps(value)).decode('utf8')
        self.dbs[self.get_key_hash(key)]['data'][key] = value_pickle
        # self.set_list.append({'type': 'set', 'key': key, 'value': value_pickle})

    def get(self, key):
        self._load_slice(key)
        return pickle.loads(base64.b64decode(self.dbs[self.get_key_hash(key)]['data'][key]))

    def exists(self, key):
        return key in self.keys

    def getall(self):
        return self.keys

    def rem(self, key):
        self._load_slice(key)
        del self.dbs[self.get_key_hash(key)]['data'][key]
        self.keys.remove(key)
        # self.set_list.append({'type': 'rem', 'key': key})

    def close(self):
        self.dump()

    def __del__(self):
        self.close()

    def enter(self, key):
        return self._with_get(self, key)

    class _with_get:
        def __init__(self, db, key):
            self.lock = db.lock
            self.db = db
            self.key = key

        class V:
            def __init__(self, v=None):
                self.value = v

        def __enter__(self):
            self.lock.acquire()
            self.v = self.V()
            if not self.db.exists(self.key):
                return self.v
            else:
                self.v.value = self.db.get(self.key)
                return self.v

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.v.value is not None:
                self.db.set(self.key, self.v.value)
            elif self.db.exists(self.key):
                self.db.rem(self.key)

            self.lock.release()
            self.db.dump()


class FRPDB:
    def __init__(self, path: str = 'data'):
        self.already_dump = False
        self.path = path
        self.set_list = []
        self.lock = threading.Lock()
        self.lock_with = threading.Lock()
        if not os.path.exists(os.path.join(self.path, 'meta.json')) and os.path.exists(
                os.path.join(self.path, 'slices')):
            import shutil
            rd_dir_name = f'temp-{random.randint(0, 1000)}'
            shutil.move(self.path, rd_dir_name)
            ntf(rd_dir_name, self.path)
            shutil.rmtree(rd_dir_name)

        if not os.path.exists(path):
            os.makedirs(path)

        if os.path.exists(os.path.join(self.path, 'all.keys')):
            self.keys = set(json.load(open(os.path.join(self.path, 'all.keys'), 'r', encoding='utf8'))['keys'])
        else:
            self.keys = set([])

        if os.path.exists(os.path.join(self.path, 'meta.json')):
            self.meta = json.load(open(os.path.join(self.path, 'meta.json'), 'r', encoding='utf8'))
        else:
            self.meta = {'version': 'F_RPDB-1'}

        if not os.path.exists(os.path.join(self.path, 'slices')):
            os.makedirs(os.path.join(self.path, 'slices'))

    @staticmethod
    def get_key_hash(key):
        return hashlib.sha1(key.encode('utf8')).hexdigest()

    def set(self, key, value):
        self.lock.acquire()
        self.keys.add(key)

        with open(os.path.join(self.path, 'slices', self.get_key_hash(key)), 'wb') as f:
            f.write(pickle.dumps(value))
        self.lock.release()

    def get(self, key):

        if key in self.keys:
            with open(os.path.join(self.path, 'slices', self.get_key_hash(key)), 'rb') as f:
                return pickle.loads(f.read())
        else:
            return None

    def exists(self, key):
        return key in self.keys

    def rem(self, key):
        self.lock.acquire()
        if os.path.exists(os.path.join(self.path, 'slices', self.get_key_hash(key))):
            os.remove(os.path.join(self.path, 'slices', self.get_key_hash(key)))

            self.keys.remove(key)
        self.lock.release()

    def close(self):
        self.already_dump = True
        self.dump()

    def dump(self):
        self.lock.acquire()
        with open(os.path.join(self.path, 'all.keys'), 'w', encoding='utf8') as f:
            json.dump({'keys': list(self.keys)}, f)
        with open(os.path.join(self.path, 'meta.json'), 'w', encoding='utf8') as f:
            json.dump(self.meta, f)
        self.lock.release()

    def __del__(self):
        if not self.already_dump:
            self.close()

    def enter(self, key):
        return self._with_get(self, key)

    class _with_get:
        def __init__(self, db, key):
            self.lock_with = db.lock_with
            self.db = db
            self.key = key

        class V:
            def __init__(self, v=None):
                self.value = v

        def __enter__(self):
            self.lock_with.acquire()
            self.v = self.V()
            if not self.db.exists(self.key):
                return self.v
            else:
                self.v.value = self.db.get(self.key)
                return self.v

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.v.value is not None:
                self.db.set(self.key, self.v.value)
            elif self.db.exists(self.key):
                self.db.rem(self.key)

            self.lock_with.release()
            self.db.dump()


def otn(path, new_path, slice_multiplier=1):
    old_db = OldRPDB(path)
    new_db = RPDB(new_path, slice_multiplier=slice_multiplier)
    for key in old_db.getall():
        new_db.set(key, old_db.get(key))
    new_db.close()


def ntf(path, new_path, slice_multiplier=1):
    old_db = RPDB(path, slice_multiplier=slice_multiplier)
    new_db = FRPDB(new_path)

    for key in old_db.keys:
        new_db.set(key, old_db.get(key))
    new_db.close()
