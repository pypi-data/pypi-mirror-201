#!/usr/bin/env bash
__version__ = '0.15.0'

from contextlib import AbstractContextManager, contextmanager
from enum import Enum
from logging import warning
from re import IGNORECASE, match, search
from subprocess import CalledProcessError, check_call, check_output

from parver import Version
from path import Path
from typer import run


class ReleaseType(Enum):
    DEV = 'dev'
    PATCH = 'patch'
    MINOR = 'minor'
    MAJOR = 'major'


DEV = ReleaseType.DEV
PATCH = ReleaseType.PATCH
MINOR = ReleaseType.MINOR
MAJOR = ReleaseType.MAJOR


SIMULATE = False


class VersionFile:
    """Wraps around a version variable in a file. Caches reads."""
    __slots__ = '_file', '_offset', '_version', '_trail'

    def __init__(self, path: Path):
        file = self._file = path.open('r+', newline='\n')
        text = file.read()
        if SIMULATE is True:
            print(f'* reading {path}')
            from io import StringIO
            self._file = StringIO(text)
        match = search(r'\b__version__\s*=\s*([\'"])(.*?)\1', text)
        self._offset, end = match.span(2)
        self._trail = text[end:]
        self._version = Version.parse(match[2])

    @property
    def version(self) -> Version:
        return self._version

    @version.setter
    def version(self, version: Version):
        (file := self._file).seek(self._offset)
        file.write(str(version) + self._trail)
        file.truncate()
        self._version = version

    def close(self):
        self._file.close()


def check_setup_cfg_and_get_version_path() -> Path:
    from configparser import ConfigParser
    setup_cfg = ConfigParser()
    successfully_parsed_files = setup_cfg.read('setup.cfg', encoding='utf8')
    if not successfully_parsed_files:
        msg = 'setup.cfg was not found'
        if Path('setup.py').exists():
            msg += '\ntry `setuptools-py2cfg` to convert setup.py to setup.cfg'
        raise FileNotFoundError(msg)

    try:
        options = setup_cfg['options']
    except KeyError:
        raise RuntimeError('[options] section was not found in setup.cfg')
    if 'tests_require' in options:
        raise RuntimeError(
            '`tests_require` in setup.cfg is deprecated; '
            'use the following sample instead:'
            '\n[options.extras_require]'
            '\ntests ='
            '\n    pytest'
            '\n    pytest-cov')
    if 'setup_requires' in options:
        raise RuntimeError('`setup_requires` is deprecated')

    # https://packaging.python.org/guides/single-sourcing-package-version/
    version = setup_cfg['metadata']['version']
    m = search(r'attr: (\w+)\.__version__', version)
    if not m:
        raise RuntimeError(
            'add `version = attr: package.__version__` to setup.cfg')
    return Path(m[1]) / '__init__.py'


@contextmanager
def read_version_file() -> AbstractContextManager[VersionFile]:
    version_path = check_setup_cfg_and_get_version_path()
    fv = VersionFile(version_path)
    try:
        yield fv
    finally:
        fv.close()


def get_release_type() -> ReleaseType:
    """Return 0 for major, 1 for minor and 2 for a patch release.

    According to https://www.conventionalcommits.org/en/v1.0.0/ .
    """
    try:
        last_version_tag: str = check_output(
            ('git', 'describe', '--match', 'v[0-9]*', '--abbrev=0')
        )[:-1].decode()
        if SIMULATE is True:
            print(f'* {last_version_tag=}')
        log = check_output(
            ('git', 'log', '--format=%B', '-z', f'{last_version_tag}..@'))
    except CalledProcessError:  # there are no version tags
        warning('No version tags found. Checking all commits...')
        log = check_output(('git', 'log', '--format=%B'))
    if search(
            rb'(?:\A|[\0\n])(?:BREAKING CHANGE[(:]|.*?!:)', log):
        return MAJOR
    if search(rb'(?:\A|\0)feat[(:]', log, IGNORECASE):
        return MINOR
    return PATCH


def get_release_version(
    current_version: Version, release_type: ReleaseType = None
) -> Version:
    """Return the next version according to git log."""
    if release_type is DEV:
        if current_version.is_devrelease:
            return current_version.bump_dev()
        return current_version.bump_release(index=2).bump_dev()
    if release_type is None:
        release_type = get_release_type()
        if SIMULATE is True:
            print(f'* {release_type}')
    base_version = current_version.base_version()  # removes devN
    if release_type is PATCH:
        return base_version
    if release_type is MINOR or current_version < Version(1):
        # do not change an early development version to a major release
        # that type of change should be more explicit (edit versions).
        return base_version.bump_release(index=1)
    return base_version.bump_release(index=0)


def update_version(
    version_file: VersionFile,
    release_type: ReleaseType = None,
) -> Version:
    """Update all versions specified in config + CHANGELOG.rst."""
    current_ver = version_file.version
    version_file.version = release_version = get_release_version(
        current_ver, release_type)
    if SIMULATE is True:  # noinspection PyUnboundLocalVariable
        print(f'* change file version from {current_ver} to {release_version}')
    version_file.version = release_version
    return release_version


def commit(version: Version):
    args = ('git', 'commit', '--all', f'--message=release: v{version}')
    if SIMULATE is True:
        print('* ' + ' '.join(args))
        return
    check_call(args)


def commit_and_tag(release_version: Version):
    commit(release_version)
    git_tag = ('git', 'tag', '-a', f'v{release_version}', '-m', '')
    if SIMULATE is True:
        print('* ' + ' '.join(git_tag))
        return
    check_call(git_tag)


def upload_to_pypi():
    build = ('python', '-m', 'build', '--no-isolation')
    twine = ('twine', 'upload', 'dist/*')
    if SIMULATE is True:
        print(f"* {' '.join(build)}\n* {' '.join(twine)}")
        return
    try:
        check_call(build)
        check_call(twine)
    finally:
        for d in ('dist', 'build'):
            Path(d).rmtree_p()


def check_update_changelog(
    changelog: bytes, release_version: Version,
    ignore_changelog_version: bool
) -> bytes | bool:
    unreleased = match(br'[Uu]nreleased\n-+\n', changelog)
    if unreleased is None:
        v_match = match(br'v([\d.]+\w+)\n', changelog)
        if v_match is None:
            raise RuntimeError(
                'CHANGELOG.rst does not start with a version or "Unreleased"')
        changelog_version = Version.parse(v_match[1].decode())
        if changelog_version == release_version:
            print("* CHANGELOG's version matches release_version")
            return True
        if ignore_changelog_version is not False:
            print('* ignoring non-matching CHANGELOG version')
            return True
        raise RuntimeError(
            f"CHANGELOG's version ({changelog_version}) does not "
            f"match release_version ({release_version}). "
            "Use --ignore-changelog-version ignore this error.")

    if SIMULATE is True:
        print(
            '* replace the "Unreleased" section of "CHANGELOG.rst" with '
            f'v{release_version}')
        return True

    ver_bytes = f'v{release_version}'.encode()
    return b'%b\n%b\n%b' % (
        ver_bytes, b'-' * len(ver_bytes), changelog[unreleased.end():])


def update_changelog(release_version: Version, ignore_changelog_version: bool):
    """Change the title of initial "Unreleased" section to the new version.

    Note: "Unreleased" and "CHANGELOG" are the recommendations of
        https://keepachangelog.com/ .
    """
    try:
        with open('CHANGELOG.rst', 'rb+') as f:
            changelog = f.read()
            new_changelog = check_update_changelog(
                changelog, release_version, ignore_changelog_version)
            if new_changelog is True:
                return
            f.seek(0)
            f.write(new_changelog)
            f.truncate()
    except FileNotFoundError:
        if SIMULATE is True:
            print('* CHANGELOG.rst not found')


ISORT = """
[tool.isort]
profile = "black"
line_length = 79
combine_as_imports = true
"""

PYPROJECT_TOML = f"""\
[build-system]
requires = [
    # 46.4.0 is required for handling attr version, see:
    # https://packaging.python.org/guides/single-sourcing-package-version/
    "setuptools>=46.4.0",
    "wheel"
]
build-backend = "setuptools.build_meta"
{ISORT}
"""


def check_pyproject_toml():
    # https://packaging.python.org/tutorials/packaging-projects/
    try:
        with open('pyproject.toml', encoding='utf8') as f:
            pyproject_toml = f.read()
    except FileNotFoundError:
        with open('pyproject.toml', 'w', encoding='utf8') as f:
            f.write(PYPROJECT_TOML)
        raise FileNotFoundError('pyproject.toml was not found; sample created')

    m = search(r'setuptools>=([\d.]+)', pyproject_toml)
    if not m or (Version.parse(m[1]) < Version((46, 4, 0))):
        raise RuntimeError(
            'Please require `setuptools>=46.4.0` in pyproject.toml\n'
            "That's the minimum version that supports `attr` in setup.cfg.\n"
        )

    if 'build-backend = "setuptools.build_meta"' not in pyproject_toml:
        raise RuntimeError(
            '`build-backend = "setuptools.build_meta"` not in pyproject.toml')

    if '[tool.isort]' not in pyproject_toml:
        with open('pyproject.toml', 'a', encoding='utf8') as f:
            f.write(ISORT)
        raise RuntimeError('[tool.isort] was added to pyproject.toml')


def check_r3l3453_json():
    if Path('r3l3453.json').exists():
        raise RuntimeError(
            'Remove r3l3453.json as it is not needed anymore.\n'
            'Version path should be specified in setup.cfg.\n'
            '[metadata]\n'
            'version = attr: package.__version__')


def check_git_status(ignore_git_status: bool):
    status = check_output(('git', 'status', '--porcelain'))
    if status:
        if ignore_git_status:
            print(f'* ignoring git {status=}')
        else:
            raise RuntimeError(
                'git status is not clean. '
                'Use --ignore-git-status to ignore this error.')
    branch = check_output(
        ('git', 'branch', '--show-current')).rstrip().decode()
    if branch != 'master':
        if ignore_git_status:
            print(f'* ignoring git branch ({branch} != master)')
        else:
            raise RuntimeError(
                f'git is on {branch} branch. '
                'Use --ignore-git-status to ignore this error.')


def main(
    rtype: ReleaseType = None, upload: bool = True, push: bool = True,
    simulate: bool = False, path: str = None,
    ignore_changelog_version: bool = False,
    ignore_git_status: bool = False,
):
    global SIMULATE
    SIMULATE = simulate

    if path is not None:
        Path(path).chdir()

    check_r3l3453_json()
    check_pyproject_toml()
    check_git_status(ignore_git_status)

    with read_version_file() as version_file:
        release_version = update_version(version_file, rtype)
        update_changelog(release_version, ignore_changelog_version)
        commit_and_tag(release_version)

        if upload is True:
            upload_to_pypi()

        # prepare next dev0
        new_dev_version = update_version(version_file, DEV)
        commit(new_dev_version)

    if push is True:
        if SIMULATE is True:
            print('* git push')
        else:
            check_call(('git', 'push', '--follow-tags'))


def console_scripts_entry_point():
    run(main)
