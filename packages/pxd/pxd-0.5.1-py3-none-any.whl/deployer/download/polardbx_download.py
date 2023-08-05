#   Copyright [2013-2021], Alibaba Group Holding Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import concurrent
import gzip
import logging
import os
import shutil
from concurrent.futures._base import as_completed
from pathlib import Path

import click
import requests
import yaml
from packaging import version

import deployer.download.constant as constant
import deployer.core.docker_manager as DockerManager
from deployer.decorator.decorators import download_task

logger = logging.getLogger(__name__)

polardbx_package = "polardbx-install"


@download_task(task_name="prepare install directory")
def prepare_dest_install_dir(env, arch, repo, image_list, dest):
    if not os.path.exists(dest) or not os.path.isdir(dest):
        click.echo("Dest directory %s does not exists or not a dir" % dest)

    install_package_dir = os.path.join(dest, polardbx_package)
    if os.path.exists(install_package_dir):
        click.confirm(click.style('Install package : %s already exists, override it?' % install_package_dir, fg='blue'),
                      abort=True)
        shutil.rmtree(install_package_dir)

    os.makedirs(install_package_dir, exist_ok=True)


def download_oss_file_to_local(file_list):
    for file_tuple in file_list:
        oss_url = file_tuple[0]
        local_file = file_tuple[1]
        local_dir = os.path.dirname(local_file)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        r = requests.get(oss_url)
        with open(local_file, "wb") as f:
            f.write(r.content)


@download_task(task_name="download pxd wheel package")
def download_pxd_related_package(env, arch, repo, image_list, dest):
    pxd_version_file = f"{constant.POLARDBX_OPENSOURCE_OSS}/{constant.PXD_WHL_MODULE}/{constant.PXD_VERSION_FILE}"
    r = requests.get(pxd_version_file)
    pxd_version = r.content.decode('utf-8').strip()

    install_package_dir = os.path.join(dest, polardbx_package)

    # pxd wheel file
    pxd_whl_oss_url = f"{constant.POLARDBX_OPENSOURCE_OSS}/{constant.PXD_WHL_MODULE}/{constant.PXD_WHL_FILE_FORMAT}" % pxd_version
    pxd_whl_local_file = os.path.join(dest, polardbx_package, constant.PXD_WHL_FILE_FORMAT) % pxd_version

    # pxd dependency
    pxd_dependency_file = constant.PXD_DEPENDENCY_FORMAT % arch
    pxd_dependency_oss_url = f"{constant.POLARDBX_OPENSOURCE_OSS}/{constant.PXD_DEPENDENCY_MODULE}/{pxd_dependency_file}"
    pxd_dependency_local_file = f"{install_package_dir}/{pxd_dependency_file}"
    file_list = [
        (pxd_whl_oss_url, pxd_whl_local_file),
        (pxd_dependency_oss_url, pxd_dependency_local_file)
    ]

    download_oss_file_to_local(file_list)


@download_task(task_name="download polardbx helm charts")
def download_helm_packages(env, arch, repo, image_list, dest):
    helm_index_url = f"{constant.POLARDBX_HELM_OSS}/index.yaml"
    r = requests.get(helm_index_url)
    data = yaml.load(r.content.decode("UTF-8").strip())
    helm_version = version.parse("0.0.0")
    for entry in data["entries"]["polardbx-operator"]:
        current_version = version.parse(entry['appVersion'])
        if current_version.is_prerelease or current_version.is_devrelease:
            continue
        if current_version > helm_version:
            helm_version = current_version
    logger.info("current helm chart version: %s" % helm_version.public)

    install_helm_dir = os.path.join(dest, polardbx_package, "helm")

    file_list = []
    helm_charts = [constant.OPERATOR_HELM_FORMAT, constant.MONITOR_HELM_FORMAT, constant.LOGGER_HELM_FORMAT]
    for helm in helm_charts:
        helm_chart_oss_url = f"{constant.POLARDBX_HELM_OSS}/{helm}" % helm_version
        helm_chart_local_file = f"{install_helm_dir}/{helm}" % helm_version
        file_list.append((helm_chart_oss_url, helm_chart_local_file))

    value_files = ['operator-values.yaml', 'monitor-values.yaml', 'logger-values.yaml']
    for value_file in value_files:
        values_oss_url = f"{constant.POLARDBX_OPENSOURCE_OSS}/{constant.K8S_VALUES_MODULE}/{value_file}"
        values_local_file = f"{install_helm_dir}/{value_file}"
        file_list.append((values_oss_url, values_local_file))

    # helm binary
    helm_bin_oss_url = f"{constant.POLARDBX_OPENSOURCE_OSS}/{constant.K8S_VALUES_MODULE}/linux-{arch}/helm"
    helm_bin_local_file = f"{install_helm_dir}/bin/helm"

    file_list.append((helm_bin_oss_url, helm_bin_local_file))

    download_oss_file_to_local(file_list)

@download_task("download install scripts")
def download_install_script(env, arch, repo, image_list, dest):
    install_oss_url = f"{constant.POLARDBX_OPENSOURCE_OSS}/{constant.SCRIPTS_MODULE}/install-{env}.sh"
    install_local_file = os.path.join(dest, polardbx_package, 'install.sh')

    load_image_oss_url = f"{constant.POLARDBX_OPENSOURCE_OSS}/{constant.SCRIPTS_MODULE}/load_image.sh"
    load_image_local_file = os.path.join(dest, polardbx_package, 'images', 'load_image.sh')

    script_list = [(install_oss_url, install_local_file),
                   (load_image_oss_url, load_image_local_file)]
    download_oss_file_to_local(script_list)

"""
Download and save docker images to target repo
"""
@download_task(task_name="download image and save to file")
def download_and_save_images(env, arch, repo, image_list, dest):
    dest_image_dir = os.path.join(dest, polardbx_package, 'images')
    if not os.path.exists(dest_image_dir):
        os.makedirs(dest_image_dir)

    dest_image_list_file = f"{dest_image_dir}/image.list"
    if image_list == '':
        image_list_url = f"{constant.POLARDBX_OPENSOURCE_OSS}/{env}-images/images.list"
        download_oss_file_to_local([(image_list_url, dest_image_list_file)])
    else:
        shutil.copyfile(src=image_list, dst=dest_image_list_file)

    image_manifest_file = f"{dest_image_dir}/image.manifest"
    client = DockerManager.get_client(constant.LOCALHOST)
    with open(image_manifest_file, "wt") as manifest:
        with open(dest_image_list_file) as f:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                results = []
                for image in f:
                    result = executor.submit(_pull_and_save_image, arch, client, dest_image_dir, image, manifest, repo)
                    results.append(result)

                for res in as_completed(results):
                    logger.info(res.result())


def _pull_and_save_image(arch, client, dest_image_dir, image, manifest, repo):
    image = image.strip()
    image_name = image.split("/")[-1]
    image_file_name = image_name.replace(":", "-") + "-" + arch + ".tar.gz"
    image_file_name = f"{image_name.replace(':', '-')}-{arch}.tar.gz"
    new_image_name = image
    if repo != "":
        new_image_name = f"{repo}/{image_name}"
    # pull docker image first
    click.echo("Pulling image: %s" % image)
    client.images.pull(image, platform=arch)
    # Tag docker image to new tag
    click.echo("Tag %s to %s" % (image, new_image_name))
    client.images.get(image).tag(new_image_name)
    new_image = client.images.get(new_image_name)
    new_image_file = f"{dest_image_dir}/{image_file_name}"
    click.echo("Saving image: %s" % new_image_name)
    with gzip.open(new_image_file, "wb") as compress_file:
        for chunk in new_image.save(named=new_image_name):
            compress_file.write(chunk)
    manifest.write(f"{image_file_name} {new_image_name}\n")


"""
Render values.yaml for polardbx-operator, fill private repo
"""


@download_task(task_name="render helm chart values file")
def render_helm_values_file(env, arch, repo, image_list, dest):
    operator_values_file = os.path.join(dest, polardbx_package, "helm", "operator-values.yaml")
    operator_values = _read_yaml_file(operator_values_file)
    operator_values["imageRepo"] = repo
    operator_values["extension"]["config"]["images"]["store"]["galaxy"]["exporter"] = f"{repo}/mysqld-exporter:master"
    _write_yaml_file(operator_values_file, operator_values)

    monitor_values_file = os.path.join(dest, polardbx_package, "helm", "monitor-values.yaml")
    monitor_values = _read_yaml_file(monitor_values_file)
    _update_yaml_key_value(monitor_values, "repo", repo)
    _write_yaml_file(monitor_values_file, monitor_values)

    logger_values_file = os.path.join(dest, polardbx_package, "helm", "logger-values.yaml")
    logger_values = _read_yaml_file(logger_values_file)
    _update_yaml_key_value(logger_values, "repo", repo)
    _write_yaml_file(logger_values_file, logger_values)


def _read_yaml_file(yaml_file):
    with open(yaml_file) as f:
        return yaml.load(f)


def _write_yaml_file(yaml_file, data):
    with open(yaml_file, 'w') as f:
        yaml.dump(data, f)


def _update_yaml_key_value(yaml_data, key, new_value):
    if key in yaml_data.keys():
        yaml_data[key] = new_value
    for k, v in yaml_data.items():
        if isinstance(v, dict):
            _update_yaml_key_value(v, key, new_value)


download_pxd_package_tasks = [
    prepare_dest_install_dir,
    download_install_script,
    download_pxd_related_package,
    download_and_save_images,
]

download_k8s_package_tasks = [
    prepare_dest_install_dir,
    download_install_script,
    download_helm_packages,
    render_helm_values_file,
    download_and_save_images,
]


def download_polardbx_packages(env, arch, repo, image_list, dest):
    if env not in ("pxd", "k8s"):
        click.echo("input env does not support, only support pxd or k8s")
        return
    if repo != '' and repo[-1] == '/':
        repo = repo[:-1]

    tasks = download_k8s_package_tasks
    if env == "pxd":
        tasks = download_pxd_package_tasks

    with click.progressbar(tasks, label="Processing",
                           show_eta=False) as progress_bar:
        for task in progress_bar:
            task(env, arch, repo, image_list, dest)

    click.echo("polardbx install package download success, package: %s/%s" % (dest, polardbx_package))
