import importlib
import importlib.util
import os
import sys
import traceback
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Union

from chalk.features.resolver import Resolver, StreamResolver
from chalk.gitignore.gitignore_parser import parse_gitignore
from chalk.gitignore.helper import IgnoreConfig, _get_default_combined_ignore_config, _is_ignored
from chalk.parsed.duplicate_input_gql import FailedImport
from chalk.sql._internal.sql_file_resolver import ResolverResult, get_sql_file_resolvers
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.paths import _search_recursively_for_file, get_directory_root

_logger = get_logger(__name__)


def _py_path_to_module(path: Path, repo_root: Path) -> str:
    try:
        p = path.relative_to(repo_root)
    except ValueError:
        p = path
    return str(p)[: -len(".py")].replace("./", "").replace("/", ".")


def import_all_files() -> List[FailedImport]:
    project_root: Optional[Path] = get_directory_root()
    if project_root is None:
        return [
            FailedImport(
                filename="",
                module="",
                traceback="Could not find chalk.yaml in this directory or any parent directory",
            )
        ]
    failed_imports: List[FailedImport] = import_all_python_files_from_dir(project_root=project_root)
    failed_imports.extend(import_sql_file_resolvers(project_root))
    return failed_imports


def import_sql_file_resolvers(path: Path):
    sql_resolver_results: List[ResolverResult] = list(get_sql_file_resolvers(path, BaseSQLSource.registry))
    failed_imports: List[FailedImport] = []
    for result in sql_resolver_results:
        if result.resolver:
            if isinstance(result.resolver, StreamResolver):
                StreamResolver.registry.append(result.resolver)
                if StreamResolver.hook:
                    StreamResolver.hook(result.resolver)
            else:
                Resolver.registry.append(result.resolver)
                if Resolver.hook:
                    Resolver.hook(result.resolver)
        if result.errors:
            for error in result.errors:
                failed_imports.append(
                    FailedImport(
                        traceback=error.display,
                        filename=error.path,
                        module=error.path,
                    )
                )
    return failed_imports


def _get_py_files_fast(
    resolved_root: Path, venv_path: Optional[Path], ignore_config: Optional[IgnoreConfig]
) -> Iterable[Path]:
    """
    Gets all the .py files in the resolved_root directory and its subdirectories.
    Faster than the old method we were using because we are skipping the entire
    directory if the directory is determined to be ignored. But if any .gitignore
    or any .chalkignore file has negation, we revert to checking every filepath
    against each .*ignore file.

    :param resolved_root: Project root absolute path
    :param venv_path: Path of the venv folder to skip importing from.
    :param ignore_config: An optional CombinedIgnoreConfig object. If None, we simply don't check for ignores.
    :return: An iterable of Path each representing a .py file
    """

    for dirpath_str, dirnames, filenames in os.walk(resolved_root):
        dirpath = Path(dirpath_str).resolve()

        if (venv_path is not None and venv_path.samefile(dirpath)) or (
            ignore_config
            and not ignore_config.has_negation
            and ignore_config.ignored(str(dirpath) + "/#")  # Hack to make "dir/**" match "/Users/home/dir"
        ):
            dirnames.clear()  # Skip subdirectories
            continue  # Skip files

        for filename in filenames:
            if filename.endswith(".py"):
                filepath = dirpath / filename
                if not ignore_config or not ignore_config.ignored(filepath):
                    yield filepath


def import_all_python_files_from_dir(project_root: Path, check_ignores: bool = True) -> List[FailedImport]:
    use_old_ignores_check = env_var_bool("USE_OLD_IGNORES_CHECK")
    project_root = project_root.absolute()

    cwd = os.getcwd()
    os.chdir(project_root)
    repo_root = Path(project_root)

    resolved_root = repo_root.resolve()
    _logger.debug(f"REPO_ROOT: {resolved_root}")

    # If we don't import both of these, we get in trouble.
    sys.path.append(str(resolved_root))
    sys.path.append(str(repo_root.parent.resolve()))

    venv = os.environ.get("VIRTUAL_ENV")
    if use_old_ignores_check:
        ignore_functions: List[Callable[[Union[Path, str]], bool]] = []
        ignore_functions.extend(
            parse_gitignore(str(x))[0] for x in _search_recursively_for_file(project_root, ".gitignore")
        )
        ignore_functions.extend(
            parse_gitignore(str(x))[0] for x in _search_recursively_for_file(project_root, ".chalkignore")
        )

        repo_files = {p.resolve() for p in repo_root.glob("**/*.py") if p.is_file()}
        repo_files = sorted(repo_files)
        repo_files = (repo_file for repo_file in repo_files if venv is None or Path(venv) not in repo_file.parents)
        if check_ignores:
            repo_files = (p for p in repo_files if not _is_ignored(p, ignore_functions))
    else:
        venv_path = None if venv is None else Path(venv)
        ignore_config = _get_default_combined_ignore_config(resolved_root) if check_ignores else None
        repo_files = _get_py_files_fast(resolved_root=resolved_root, venv_path=venv_path, ignore_config=ignore_config)

    errors: List[FailedImport] = []
    for filename in repo_files:
        module_path = _py_path_to_module(filename, repo_root)
        if module_path.startswith(".eggs") or module_path.startswith("venv") or filename.name == "setup.py":
            continue

        try:
            importlib.import_module(module_path)
        except Exception:
            filename = filename.resolve()
            # relevant_file = any("from chalk." or "import chalk." in c for c in f)
            # if relevant_file:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            tb = traceback.extract_tb(ex_traceback)
            line = 0
            for i, l in enumerate(tb):
                if filename == Path(l.filename).resolve():
                    line = i
                    break

            relevant_traceback = f"""Exception in module {module_path}:
{os.linesep.join(traceback.format_tb(ex_traceback)[line:])}
\n{ex_type and ex_type.__name__}: {str(ex_value)}
"""
            errors.append(
                FailedImport(
                    traceback=relevant_traceback,
                    filename=str(filename),
                    module=module_path,
                )
            )

            _logger.debug(f"Failed while importing {module_path}", exc_info=True)
            continue

    os.chdir(cwd)
    return errors
