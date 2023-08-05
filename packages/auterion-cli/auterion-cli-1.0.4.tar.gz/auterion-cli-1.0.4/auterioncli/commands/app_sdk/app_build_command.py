import os
import shutil
import pathlib
import yaml
import tempfile
from auterioncli.commands.command_base import CliCommand
from auterioncli.commands.app_sdk.environment import ensure_docker, ensure_mender_artifact, MENDER_CI_TOOLS_TAG
from auterioncli.commands.app_sdk.slimify import slimify
import subprocess
import collections.abc
import re
import copy
import sys

DEVICE_ALIAS = {
    'ainode': 'jetson'
}

PLATFORM_ALIAS = {
    'skynode': 'linux/arm64',
    'jetson': 'linux/arm64'
}


def deep_dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = deep_dict_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def run_command(commands, cwd='.'):
    print(f'> Executing \'{" ".join(commands)}\'')
    result = subprocess.run(commands, cwd=cwd)
    return result.returncode


def error(msg, code=1):
    print(msg, file=sys.stderr)
    exit(code)


class AppBuildCommand(CliCommand):

    @staticmethod
    def help():
        return 'Build Auterion OS app in current directory'

    def needs_device(self, args):
        return False

    def __init__(self, config):
        self._temp_dir = None
        self._config = config

    def setup_parser(self, parser):
        parser.add_argument('project_dir', help='Location of the project', nargs='?', default='.')
        parser.add_argument('--skip-docker-build', '-s', help='Do not execute docker build step. Just package.')

    def run(self, args):
        compose_cmd = ensure_docker()
        ensure_mender_artifact()

        self._temp_dir = tempfile.mkdtemp()
        meta = self._load_metadata(args)

        image_path = self._generate_image(compose_cmd, args, meta)

        if re.match('^v\d+$', meta['auterion-app-base']):
            v = meta['auterion-app-base']
            base_image_name = 'auterion/app-base:' + meta['auterion-app-base']
            slimify(image_path, base_image_name, self._config['persistent_dir'])
            print('┌──────────────────────────────────────────────────────────────────────────────────────┐')
            print('│                                                                                      │')
            print('│  Your app requires app auterion app-base-%s to be installed on your device.          │' % v)
            print('│                                                                                      │')
            print('│  Get app-base-%s.auterionos from Auterion suite.                                     │' % v)
            print('│                                                                                      │')
            print('│  NOTE: The app base has to be installed on the skynode before you install your app.  │')
            print('│        You can install the app-base like an app:                                     │')
            print('│        `auterion-cli app install <path to app-base-%s.auterionos>`                   │' % v)
            print('│                                                                                      │')
            print('└──────────────────────────────────────────────────────────────────────────────────────┘')

        else:
            print(f'.. {meta["auterion-app-base"]} does not match a valid app-base version. Skipping slimify step.')
        compressed_image = self._compress_image(image_path)

        self._mender_package_app(args, meta, compressed_image)
        shutil.rmtree(self._temp_dir)

    @staticmethod
    def _load_metadata(args):
        project_dir = args.project_dir
        meta_file = os.path.join(project_dir, 'auterion-app.yml')

        if not os.path.exists(meta_file):
            error(f'File \'{meta_file}\' does not exist. App structure invalid. Aborting...')

        with open(meta_file, 'r') as f:
            meta = yaml.safe_load(f)

        if 'app-name' not in meta or 'app-version' not in meta:
            error(f'{meta_file} does not contain app-name or app-version')

        if 'app-author' not in meta:
            error(f'{meta_file} does not contain `app-author` key. This field should contain a reverse-domain of the'
                  f'entity that authored the app, e.g. `com.auterion`')
        return meta

    def _extract_target_devices(self, meta):
        target_devices = [meta['target-platform']] \
            if isinstance(meta['target-platform'], str) else meta['target-platform']
        target_devices = [DEVICE_ALIAS.get(d, d) for d in target_devices]
        return target_devices

    def _extract_target_platform(self, meta):
        target_devices = self._extract_target_devices(meta)
        target_platforms = [PLATFORM_ALIAS.get(d, d) for d in target_devices]
        if len(set(target_platforms)) > 1:
            error('Targets have multiple architectures. Aborting.')
        return target_platforms[0]

    def _compose_for_building_from_meta(self, meta):
        api_version = meta['auterion-api-version']
        assert 0 <= api_version <= 2, f'Auterion API version {api_version} is not supported by this ' \
                                      f'version of auterion-cli. Supported API versions are 0 to 2.'

        compose = {}
        if api_version == 0:
            compose = {
                'version': '3.7',
                **meta['compose']
            }
        elif api_version >= 1:
            compose = {
                'version': '3.7',
                'services': {}
            }
            for name, service_config in meta['services'].items():
                compose['services'][name] = {}
                if 'build' in service_config:
                    compose['services'][name]['build'] = service_config['build']
                elif 'image' in service_config:
                    compose['services'][name]['image'] = service_config['image']

            # api version 1 still allows for dict update
            if 'compose-override' in meta:
                deep_dict_update(compose, meta['compose-override'])

        for name, service in compose['services'].items():
            if 'image' not in service:
                service['image'] = meta['app-author'] + '.' + name + ':' + meta['app-version']
            service['container_name'] = name
            service['platform'] = self._extract_target_platform(meta)
        return compose

    def _generate_image(self, compose_cmd, args, meta):
        # Generate build dir
        project_dir = args.project_dir
        build_dir = os.path.join(project_dir, 'build')
        if not os.path.exists(build_dir):
            os.mkdir(build_dir)

        target_file = os.path.join(build_dir, meta['app-author'] + '.' + meta['app-name'] + '.tar')

        # generate a minimal docker-compose file in temp dir for building using docker-compose
        # (don't use self._temp_dir, as podman-compose sets cwd to that directory)
        compose_file = os.path.join(args.project_dir, 'docker-compose-tmp.yml')
        compose = self._compose_for_building_from_meta(meta)
        with open(compose_file, 'w') as f:
            yaml.dump(compose, f)

        if not args.skip_docker_build:
            # Just export the required images from the local docker
            target_platform = self._extract_target_platform(meta)
            ret = run_command(compose_cmd + ['-f', compose_file, 'build'], cwd=args.project_dir)

            if ret != 0:
                error("Docker compose build failed.")
            os.remove(compose_file)

            non_built_images = [v['image'] for k, v in compose['services'].items() if 'build' not in v]
            if len(non_built_images) > 0:
                print(f'Need to pull {len(non_built_images)} images for this build..')
                for image in non_built_images:
                    run_command(['docker', 'pull', '--platform', target_platform, image])

        images = [v['image'] for k, v in compose['services'].items()]
        print('According to docker-compose, we have the following images:')
        for image in images:
            print(f'- {image}')

        for image in images:
            # Make sure that we correctly tag all images with the docker.io prefix. This is not
            # guaranteed on alternative runtimes such as podman
            run_command(['docker', 'tag', image, 'docker.io/' + image], cwd=project_dir)
            print('retagging...')
        images = ['docker.io/' + image for image in images]

        print('Packaging those images...')
        if os.path.isfile(target_file):
            os.remove(target_file)
        run_command(['docker', 'save'] + images + ['-o', target_file], cwd=project_dir)

        return target_file

    def _compress_image(self, image):
        run_command(['gzip', image])
        p = pathlib.Path(image + '.gz')
        target_name = p.with_suffix('').with_suffix('.image')
        p.rename(target_name)
        return str(target_name)

    def _generate_legacy_app_file(self, meta, app_file):
        # add default settings for compose
        compose = self._compose_for_building_from_meta(meta)
        app_dict = copy.deepcopy(compose)
        for name, service in app_dict['services'].items():
            if 'restart' not in service:
                service['restart'] = 'unless-stopped'
            if 'network_mode' not in service:
                service['network_mode'] = 'host'
            if 'volumes' not in service:
                service['volumes'] = [f'/data/app/{meta["app-name"]}/data:/data']
            if 'environment' not in service:
                service['environment'] = ['PYTHONUNBUFFERED=1']
            if 'env_file' not in service:
                service['env_file'] = ['settings.default.env', 'settings.user.env']

            # older docker-compose get confused about the platform and build tags
            if 'platform' in service:
                del service['platform']
            if 'build' in service:
                del service['build']

        with open(app_file, 'w') as fo:
            yaml.dump(app_dict, fo)

    def _mender_package_app(self, args, meta, image_file):
        if not os.path.exists(image_file):
            error(f'Image {image_file} does not exist. Nothing to package. Aborting..')

        version = meta['app-version']
        name = meta['app-name']

        slug = meta['app-author'] + '.' + meta['app-name']

        target_devices = self._extract_target_devices(meta)
        target_devices_args = []
        for d in target_devices:
            target_devices_args += ['-t', d]

        out_file = os.path.join(args.project_dir, 'build', slug + '.auterionos')

        meta_file = os.path.join(args.project_dir, 'auterion-app.yml')

        version_file = os.path.join(self._temp_dir, 'version')
        with open(version_file, 'w') as f:
            f.write(version)

        settings_file = os.path.join(args.project_dir, 'settings.default.env')

        if not os.path.exists(settings_file):
            settings_file = os.path.abspath(os.path.join(self._temp_dir, 'settings.default.env'))
            # create empty file
            pathlib.Path(settings_file).touch()

        # create empty user settings file for AuterionOS < 2.7
        user_settings_file = os.path.abspath(os.path.join(self._temp_dir, 'settings.user.env'))
        pathlib.Path(user_settings_file).touch()

        file_args = [
            '-f', os.path.abspath(meta_file),
            '-f', os.path.abspath(image_file),
            '-f', os.path.abspath(version_file),
            '-f', os.path.abspath(settings_file),
            '-f', os.path.abspath(user_settings_file)
        ]

        if meta['auterion-api-version'] < 2:
            app_file = os.path.join(self._temp_dir, 'app.yml')
            self._generate_legacy_app_file(meta, app_file)
            file_args += ['-f', app_file]

        pathlib.Path(settings_file).touch()

        ret = run_command([
            'docker',
            'run',
            '--rm',
            '--mount',
            f'type=bind,source={os.path.abspath(args.project_dir)},target={os.path.abspath(args.project_dir)}',
            '--mount',
            f'type=bind,source={os.path.abspath(self._temp_dir)},target={os.path.abspath(self._temp_dir)}',
            MENDER_CI_TOOLS_TAG,
            'mender-artifact', 'write', 'module-image',
            '-o', os.path.abspath(out_file),
            '-T', 'docker',
            '-n', slug + ':' + version,
            '--software-filesystem', 'docker-app',
            '--software-name', slug,
            '--software-version', version,
        ] + target_devices_args + file_args)

        if ret != 0:
            error('Packaging step failed. Aborting.')

        # get rid of image file
        os.unlink(image_file)

