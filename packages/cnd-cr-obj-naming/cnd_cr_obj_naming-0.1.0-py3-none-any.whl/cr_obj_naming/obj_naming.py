from cnd_cr_object import CrObject
import consul
import hashlib
import json


class ObjNaming(CrObject):
    consul_creds = {}

    def __init__(self, data, md5_length, _print):
        super().__init__(_print)
        self._data = data
        self._md5_length = md5_length

    def set_consul(self, host, port, token, path):
        self.consul_creds["host"] = host
        self.consul_creds["token"] = token
        self.consul_creds["path"] = path
        self.consul_creds["port"] = port
        self.consul = consul.Consul(
            host=self.consul_creds["host"],
            port=self.consul_creds["port"],
            token=self.consul_creds["token"]
        )

    def full_path(self, deployment_id):
        return f'{self.consul_creds["path"]}/{deployment_id}'

    def _value(self):
        base_string = f"{self._data['vra_id']}-{self._data['service_name']}-{self._data['env']}"
        hash_val = hashlib.md5(f"{base_string}-{self._data['deployment_id']}".encode())
        return f"{base_string}-{hash_val.hexdigest()[0:self._md5_length]}"
        
    def save(self):
        self._data["name"] = self._value()
        return self.consul.kv.put(self.full_path(self._data["deployment_id"]), json.dumps(self._data, indent=4))

    def find_by_id(self, id):
        index, my_data = self.consul.kv.get(self.full_path(id))
        return json.loads(my_data['Value'])["name"]
        
    def update(self, obj_naming):
        return obj_naming.save()
        
    def destroy(self):
        return self.consul.kv.delete(self.full_path(self._data["deployment_id"]))
        
    def has_children(self):
        return False
        
    def find_relation(self):
        return []

