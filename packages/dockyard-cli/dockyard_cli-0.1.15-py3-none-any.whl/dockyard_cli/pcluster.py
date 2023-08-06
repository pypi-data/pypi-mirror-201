import click
from pathlib import Path
import requests
import json
import os
import time
from tabulate import tabulate
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class ContextObj(object):
    def __init__(self, config, url = None, cookies = None, username = None, cluster = None):
        self.config = config 
        self.url = url
        self.cookies = cookies
        self.username = username
        self.cluster = cluster

@click.group()
@click.pass_context
def hpc(ctx):
    """Group for HPC commands."""
    config = ctx.obj
    username = config.get("default","username",fallback=os.environ.get("USER",""))
    cluster = f"{username}-pcluster"
    url = config.get("default","url")
    cookie = config.get("default","cookie")
    cookies= {"_oauth2_proxy": cookie}
    ctx.obj = ContextObj(config=config,url=url, username=username, cookies=cookies, cluster=cluster)

@click.pass_obj
def pcl_get_cluster(obj, name):
    r = requests.get(f"{obj.url}/hpc/api/cluster/{name}", cookies=obj.cookies, verify=False)
    if r.status_code != 200:
        return None, r.text
    return r.json(), None

@click.pass_obj
def pcl_get_cluster_edit(obj, name):
    r = requests.get(f"{obj.url}/hpc/api/cluster/{name}/edit", cookies=obj.cookies, verify=False)
    if r.status_code != 200:
        return None, r.text
    return r.json(), None

@click.pass_obj
def pcl_status(obj, name):
    r = requests.get(f"{obj.url}/hpc/api/cluster/{name}",  cookies=obj.cookies, verify=False)
    if r.status_code != 200:
        return None, r.text
    if "clusterStatus" in r.json():
        return r.json()["clusterStatus"], None
    else:
        return r.json(), r.text

def pcl_status_wait(name, wait_status):
    status, err = pcl_status(name)
    while status == wait_status and err == None:
        time.sleep(10)
        status, err = pcl_status(name)
        print(".", end="", flush=True)
    if err != None:
        if wait_status == "DELETE_IN_PROGRESS" and "message" in err:
            return "DELETE_COMPLETE"
        else:
            print(err)
            raise click.Abort()
    return status

@click.pass_obj
def pcl_edit_cluster(obj, data):
    headers = {"Content-Type": "application/json"}
    print(f"Updating the cluster {obj.cluster}")
    r = requests.patch(f"{obj.url}/hpc/api/cluster/{obj.cluster}",  data=json.dumps(data), cookies=obj.cookies, verify=False, headers=headers)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()
    status, err = pcl_status(obj.cluster)
    print(status.lower().replace("_"," "))
    if status !=  "UPDATE_IN_PROGRESS":
        raise click.Abort()
    status = pcl_status_wait(obj.cluster, "UPDATE_IN_PROGRESS")
    print(status.lower().replace("_"," "))

def pcl_get_cluster_conf(cluster):
    cluster, err = pcl_get_cluster_edit(cluster)
    if err != None :
        click.echo("unable to get the cluster details")
        raise click.Abort()
    if "headInstanceType" not in cluster:
        click.echo("unable to get the cluster details")
        raise click.Abort()
    return cluster


@hpc.command()
@click.pass_obj
@click.option("-mi", "mi", default="t2.micro", help="master node instance type")
@click.option("-ci", "ci", default="t2.micro", help="compute instance type")
@click.option("-maxc", "maxc", default="4", help="max number of compute nodes")
@click.option("-minc", "minc", default="0", help="min number of compute nodes")
@click.option("-ami", "ami", required=False, help="custom ami image")
def create(obj, mi, ci, maxc, minc, ami):
    """create parallel cluster"""
    data = {'headInstanceType': mi , "slurmQueues": [ {"name": "default-queue", "instanceType":ci, "minCount": minc, "maxCount" : maxc}]}
 
    if ami != None:
        data["ami"] = ami
    
    headers = {"Content-Type": "application/json"}
    print(f"creating cluster {obj.cluster} ...")
    r = requests.post(f"{obj.url}/hpc/api/cluster",  data=json.dumps(data), cookies=obj.cookies, verify=False, headers=headers)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()
    resp = r.json()
    status = resp["cluster"]["clusterStatus"]
    print(status.lower().replace("_"," "))
    if status !=  "CREATE_IN_PROGRESS":
        raise click.Abort()
    name = resp["cluster"]["clusterName"]
    status = pcl_status_wait(name, "CREATE_IN_PROGRESS")
    print(status.lower().replace("_"," "))

@hpc.command()
@click.pass_obj
@click.option("-b", "backup", default="false", help="true/false creates backup ami image from head node")
@click.option("-f", "force", default="false", help="true/false deleting cluster by force")

def delete(obj, backup, force):
    """delete parallel cluster"""
    print(f"deleting cluster {obj.cluster}")
    r = requests.delete(f"{obj.url}/hpc/api/cluster/{obj.cluster}",  params={"backup":backup, "force": force}, cookies=obj.cookies, verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()
    status = r.json()["clusterStatus"]
    print(status.lower().replace("_"," "))
    if backup == "true":
        if status !=  "BACKUP_IN_PROGRESS":
            print(status.lower().replace("_"," "))
            raise click.Abort()
        status = pcl_status_wait(obj.cluster, "BACKUP_IN_PROGRESS")
        print(status.lower().replace("_"," "))
    if status !=  "DELETE_IN_PROGRESS":
        print(status.lower().replace("_"," "))
        raise click.Abort()
    status = pcl_status_wait(obj.cluster, "DELETE_IN_PROGRESS")
    print(status.lower().replace("_"," "))

@hpc.command()
@click.pass_obj
def list(obj):
    """list aws parallel clusters"""
    r = requests.get(f"{obj.url}/hpc/api/clusters", cookies=obj.cookies, verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()
    results = r.json()
    clusters = [["name", "status", "version", "region", "type"]]
    for c in  results:
        c = Struct(**c)
        clusters.append([c.clusterName, c.clusterStatus, c.version, c.region, c.scheduler["type"]])

    print(tabulate(clusters, headers="firstrow", tablefmt="presto"))

@hpc.command(context_settings=dict(ignore_unknown_options=True))
@click.pass_obj
@click.argument("name", required=False)
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
def ssh(obj, name,  command):
    """ssh/run a command inside parallel cluster head node"""
    cluster = obj.cluster
    if name != None:
        cluster = name
    r = requests.get(f"{obj.url}/hpc/api/cluster/{cluster}", cookies=obj.cookies, verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()
    resp = r.json()
    if "headNode" not in resp :
        print("Head node is not available")
        raise click.Abort()
    if  "publicIpAddress" in resp["headNode"]:
        ip = resp["headNode"]["publicIpAddress"]
    else :
        ip  = resp["headNode"]["privateIpAddress"]
    print(F"performing ssh into {ip}")
    args = ["ssh", "-o StrictHostKeyChecking=no",f"{obj.username}@{ip}"]
    args.extend(command)
    os.execvp("ssh", args)

@hpc.command()
@click.pass_obj
@click.option("-n", "name", required=True, help="slurm queue name")
@click.option("-ci", "ci", default="t2.micro", help="compute instance type")
@click.option("-maxc", "maxc", default="4", help="max number of compute nodes")
@click.option("-minc", "minc", default="0", help="min number of compute nodes")
def queue_add(obj, name, ci, maxc, minc):
    """add new slurm queue to the parallel cluster"""
    cluster = pcl_get_cluster_conf(obj.cluster)
    queues = cluster["slurmQueues"]
    queues.append({"name": name, "instanceType": ci, "minCount": minc, "maxCount": maxc})
    pcl_edit_cluster(data=cluster)

@hpc.command()
@click.pass_obj
@click.option("-n", "name", required=True, help="slurm queue name")
def queue_delete(obj, name):
    """deleting slurm queue to the parallel cluster"""
    print(f"deleting queue {name} from the cluster {obj.cluster}, all compute nodes will be stopped")
    cluster = pcl_get_cluster_conf(obj.cluster)
    slurmqueues = []
    slurmqueues.extend([{"name": q["name"], "instanceType": q["instanceType"], "minCount": q["minCount"], "maxCount": q["maxCount"]} for q in cluster["slurmQueues"] if q["name"] != name])
    cluster["slurmQueues"] = slurmqueues
    pcl_edit_cluster(data=cluster)

@hpc.command(context_settings=dict(ignore_unknown_options=True))
@click.pass_obj
@click.argument("buckets", nargs=-1, type=click.UNPROCESSED)
def s3_add(obj, buckets):
    """add s3 buckets to the parallel cluster"""
    cluster = pcl_get_cluster_conf(obj.cluster)
    print(f"adding {buckets} to the  cluster {obj.cluster}")
    s3_buckets = cluster["s3Buckets"]
    s3_buckets.extend([b for b in buckets])
    pcl_edit_cluster(data=cluster)

@hpc.command(context_settings=dict(ignore_unknown_options=True))
@click.pass_obj
@click.argument("buckets", nargs=-1, type=click.UNPROCESSED)
def s3_delete(obj, buckets):
    """removing s3 buckets from the parallel cluster"""
    print(f"deleting {buckets} from  the  cluster {obj.cluster}")
    cluster = pcl_get_cluster_conf(obj.cluster)
    s3_buckets = [] 
    s3_buckets.extend([b.replace("s3:", "") for b in cluster["s3Buckets"] if b.replace("s3:", "") not in buckets])
    cluster["s3Buckets"] = s3_buckets
    pcl_edit_cluster(data=cluster)

@hpc.command()
@click.pass_obj
@click.option("-n", "name", required=False , help="cluster name")
def get(obj, name):
    """getting details of the cluster"""
    cluster = obj.cluster
    if name != None:
        cluster = name
    print(f"getting details of the cluster {cluster}")
    cluster, err = pcl_get_cluster(cluster)
    if err != None :
        click.echo("unable to get the cluster details")
        raise click.Abort() 
    print(json.dumps(cluster, indent = 1))
