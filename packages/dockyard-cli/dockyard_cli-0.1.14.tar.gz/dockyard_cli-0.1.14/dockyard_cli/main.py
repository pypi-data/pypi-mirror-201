import click
from configparser import ConfigParser
from pathlib import Path
import requests
import json
from urllib3 import Timeout, PoolManager
import os, sys
import subprocess
import re
import platform
from dockyard_cli.utils import catch_os_exec
from dockyard_cli.login import get_auth_cookie
from dockyard_cli.workspace import _get_workspaces, list_workspaces, start_stop_workspace
import dockyard_cli.pcluster as pcluster
from dockyard_cli.metrics import get_workspace_usage, get_nodes_usage
import pkg_resources
from rich.live import Live
from sseclient import SSEClient
from rich.layout import Layout

requests.packages.urllib3.disable_warnings()
timeout = Timeout(connect=1, read=2)
http = PoolManager(timeout=timeout, cert_reqs='CERT_NONE')

config = ConfigParser()
ini_file = str(Path.home() / ".dockyard.ini")
config.read(ini_file)
install_cmd = "pip3 install --upgrade dockyard-cli"
host_type = platform.system()

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return (getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix)


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix

def get_formatted_name(name) :
    name=re.sub('[^A-Za-z0-9-]+', '-', name).lower()
    return name.strip("-")

def _update():
    home = str(Path.home())
    if in_virtualenv():
        p = subprocess.run(install_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=home, shell=True)
    else:
        cmd = install_cmd + " --user"
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=home, shell=True)
    if p.returncode != 0 and p.stderr:
        print(p.stderr.decode("ascii"))


def dockyard_login(config):
    if config.get("default", "auto_update", fallback="true") == "true":
        _update()
    url = config.get("default","url")
    cookie = get_auth_cookie(url)
    config.set("default", "cookie", cookie)

    with open(ini_file, "w") as f:
        config.write(f)

def get_workspaces(ctx, args, incomplete):
    workspaces = _get_workspaces(config)
    return [ w["name"] for w in workspaces if incomplete in w["name"]]

cookie = config.get("default","cookie", fallback=None)

if len(sys.argv) > 1 and sys.argv[1] not in ["configure","login"] and cookie:
    url = config.get("default","url")
    cookies = {'Cookie':f'_oauth2_proxy={cookie}'}
    command = " ".join(sys.argv)
    version = pkg_resources.require("dockyard-cli")[0].version
    json_data = json.dumps({"command": command, "version": version})
    r = http.request('POST', url + "/api/ds/cli", body = json_data, headers=cookies, retries=False)
    if r.status == 302:
        dockyard_login(config)
    elif r.status != 200:
        print(r.data)
        raise click.Abort()
    try:
        me = json.loads(r.data)
    except Exception:
        dockyard_login(config)
    
@click.group()
@click.pass_context

def main(ctx):
    """Group for dockyard commands."""
    if ctx.invoked_subcommand != "configure":
        if "default" not in config.sections():
            click.echo("You need to run 'dcli configure' first.")
            raise click.Abort()
        if not config.get("default","cookie",fallback=None):
            dockyard_login(config)
        workspace = config.get("default","workspace",fallback=None)
        if workspace:
            os.environ["DOCKYARD_WORKSPACE"] = workspace
        ctx.obj = config

main.add_command(pcluster.hpc)

@main.command()
def configure():
    """Configure Dockyard CLI"""

    if "default" not in config.sections():
        config.add_section("default")
        
    url = config.get("default","url",fallback="https://dockyard.lab.altoslabs.com")
    url = click.prompt("Dockyard URL", default=url)
    username = config.get("default","username",fallback="default")
    username = click.prompt("Username", default=username)
    config.set("default", "url", url)
    config.set("default", "username", username)

    with open(ini_file, "w") as f:
        config.write(f)

    shell = os.environ["SHELL"].split("/")[-1]
    if shell in ["bash", "zsh"]:
        filename = os.environ["HOME"] + f"/.dcli-complete.{shell}rc"
        command = f'_DCLI_COMPLETE={shell}_source dcli'
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        open(filename,"wb").write(process.stdout)
        print(f"Append source {filename} in ~/.{shell}rc for command auto-completion")

@main.command()
@click.argument("workspace_name", shell_complete=get_workspaces)
def activate(workspace_name):
    """Set active workspace"""
    config.set("default", "workspace", workspace_name)

    with open(ini_file, "w") as f:
        config.write(f)

@main.command()
def login():
    """Login to Dockyard"""
    dockyard_login(config)
        
@main.command()
def update():
    """Update dockyard cli"""
    _update()


@main.command()
def list():
    """List dockyard workspaces"""
    list_workspaces(config)

@main.command()
@click.argument("workspace_name", envvar="DOCKYARD_WORKSPACE", shell_complete=get_workspaces)
def start(workspace_name):
    """Start given workspace"""
    start_stop_workspace(config, workspace_name, "start")

@main.command()
@click.argument("workspace_name", envvar="DOCKYARD_WORKSPACE", shell_complete=get_workspaces)
def stop(workspace_name):
    """Stop given workspace"""
    start_stop_workspace(config, workspace_name, "stop")

@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("workspace_name", envvar="DOCKYARD_WORKSPACE", shell_complete=get_workspaces)
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
def ssh(workspace_name, command):
    """SSH to dockyard workspace"""

    url = config.get("default","url")
    user = config.get("default","username")
    cookie = config.get("default","cookie")
    cookies = {"_oauth2_proxy": cookie}
    r = requests.get(f"{url}/api/ds/workspaces/{workspace_name}/services", cookies=cookies, verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()

    resp = r.json()
    host = resp["ip"]
    port = resp["ports"]["ssh"]
    print(f"running ssh {user}@{host} -p {port} {' '.join(command)}")
    a = ["ssh", "-o StrictHostKeyChecking=no", f"{user}@{host}", "-p", str(port)]
    a.extend(command)
    os.execvp("ssh", a)


@main.command()
@click.argument("workspace_name", envvar="DOCKYARD_WORKSPACE", shell_complete=get_workspaces)
@catch_os_exec
def code(workspace_name):
    """Start local VSCode and connect to dockyard workspace"""

    url = config.get("default","url")
    user = config.get("default","username")
    cookie = config.get("default","cookie")
    cookies = {"_oauth2_proxy": cookie}
    r = requests.get(f"{url}/api/ds/workspaces/{workspace_name}/services", cookies=cookies, verify=False, allow_redirects=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()

    resp = r.json()
    host = resp["ip"]
    port = resp["ports"]["ssh"]
    print(f"running code {user}@{host} -p {port}")
    if host_type == "Darwin":
        code = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
    else:
        code = subprocess.run("which code", stdout=subprocess.PIPE, shell=True).stdout.decode().strip()
    folder =  f"vscode-remote://ssh-remote+{user}@{host}:{port}/home/{user}"
    os.execlp(code,"code", "--folder-uri", folder)

@main.command()
@click.argument("workspace_name", envvar="DOCKYARD_WORKSPACE", shell_complete=get_workspaces)
@catch_os_exec
def vnc(workspace_name):
    """VNC connection to  dockyard workspace"""

    url = config.get("default","url")
    user = config.get("default","username")
    cookie = config.get("default","cookie")
    cookies = {"_oauth2_proxy": cookie}
    r = requests.get(f"{url}/api/ds/workspaces/{workspace_name}/services", cookies=cookies, verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()

    resp = r.json()
    host = resp["ip"]
    port = resp["ports"]["vnc"]
    uuid = resp["uuid"]
    print(f"connecting to VNC server at {host}:{port}. password: {uuid}")
    
    if host_type == "Linux": 
        os.execlp("vncviewer","vncviewer", f"{host}:{port}")
    elif host_type == "Darwin":
        os.execlp("open", "open", f"vnc://{user}@{host}:{port}")

@main.command()
@click.argument("source")
@click.argument("target")
def scp(source, target):
    """COPY files(s)/directory from/to dockyard workspace"""

    if ":" not in source and ":" not in target:
        raise click.UsageError("source or target needs to be of the format <worksapce_name>:/path")

    url = config.get("default","url")
    user = config.get("default","username")

    local_source = False

    if ":" in source:
        workspace_name = source.split(":")[0]
        source = source.split(":")[1]
    else:
        workspace_name = target.split(":")[0]
        local_source = True
        target = target.split(":")[1]

    workspace_dir = get_formatted_name(workspace_name.lower())

    cookie = config.get("default","cookie")
    cookies = {"_oauth2_proxy": cookie}
    r = requests.get(f"{url}/api/ds/workspaces/{workspace_name}/services", cookies=cookies, verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()

    resp = r.json()
    host = resp["ip"]
    port = resp["ports"]["ssh"]

    
    if local_source:
        if target == "" or target[0] not in ["~","/"]:
            target = f"workspaces/{workspace_dir}/{target}"
        print("scp", "-r", "-P", str(port), source, f"{user}@{host}:{target}")
        os.execlp("scp","scp", "-r", "-P", str(port), source, f"{user}@{host}:{target}")
    else:
        if source == "" or source[0] not in ["~","/"]:
            source = f"workspaces/{workspace_dir}/{source}"
        print("scp", "-r", "-P", str(port), f"{user}@{host}:{source}", target)
        os.execlp("scp","scp", "-r", "-P", str(port), f"{user}@{host}:{source}", target)        

@main.command()
@click.argument("workspace", required=False)
def top(workspace):
    """Show workspace resource usage"""
    user = config.get("default","username")
    url = config.get("default", "url")
    layout = Layout()
    layout.split_column(Layout(name="Workspaces", ratio=3), Layout(name="Nodes", ratio=1))
    layout["Workspaces"].update(get_workspace_usage({}))
    layout["Nodes"].update(get_nodes_usage({}))
    cookie = config.get("default","cookie")
    headers = {"Accept-Encoding": "gzip"}
    response = requests.get(f'{url}/api/ds/metrics', stream=True, cookies={"_oauth2_proxy": cookie}, headers=headers)
    client = SSEClient(response)
    with Live(layout, refresh_per_second=1) as live:
        for event in client.events():
            if event.data.startswith("{"):
                metrics = json.loads(event.data)
                node_filter = None
                if workspace:
                    for k, m in metrics["workspaces"].items():
                        if workspace in k and user == m["user"]:
                            node_filter = m["node"]
                            break
                layout["Workspaces"].update(get_workspace_usage(metrics["workspaces"], node_filter))
                layout["Nodes"].update(get_nodes_usage(metrics["nodes"], node_filter))
                live.update(layout)