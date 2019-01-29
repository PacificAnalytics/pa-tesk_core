import json
from tesk_core import path


class Filer:
    
    def getEnv(self):
        
        return self.spec['spec']['template']['spec']['containers'][0]['env']
    
    def __init__(self, name, data, filer_version='v0.5', debug=False):
        self.name = name
        self.spec = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {"name": name},
            "spec": {
                "template": {
                    "metadata": {"name": "tesk-filer"},
                    "spec": {
                        "containers": [{
                            "name": "filer",
                            "image": "eu.gcr.io/tes-wes/filer:" + filer_version,
                            "args": [],
                            "env": [],
                            "volumeMounts": [],
                            "imagePullPolicy": "IfNotPresent"
                        }
                        ],
                        "volumes": [],
                        "restartPolicy": "Never"
                    }
                }
            }
        }

        if debug:
            self.spec['spec']['template']['spec']['containers'][0]['imagePullPolicy'] = 'Always'

        env = self.getEnv()
        env.append({ "name": "JSON_INPUT"           , "value": json.dumps(data)          })
        env.append({ "name": "HOST_BASE_PATH"       , "value": path.HOST_BASE_PATH       })
        env.append({ "name": "CONTAINER_BASE_PATH"  , "value": path.CONTAINER_BASE_PATH  })


    def set_ftp(self, user, pw):
        env = self.getEnv()
        env.append({"name": "TESK_FTP_USERNAME", "value": user})
        env.append({"name": "TESK_FTP_PASSWORD", "value": pw})


    def set_volume_mounts(self, pvc):
        tempspec = self.spec['spec']['template']['spec']
        tempspec['containers'][0]['volumeMounts'] = pvc.volume_mounts
        tempspec['volumes'] = [{"name": "task-volume",
                                "persistentVolumeClaim": {"claimName": pvc.name}}]

    def get_spec(self, mode, debug=False):
        self.spec['spec']['template']['spec']['containers'][0]['args'] = [
            mode, "$(JSON_INPUT)"]

        if debug:
            self.spec['spec']['template']['spec']['containers'][0]['args'].append(
                '-d')

        self.spec['spec']['template']['metadata']['name'] = self.name
        return self.spec