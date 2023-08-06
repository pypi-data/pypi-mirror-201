import click

from .di_manager import DIManager
from .version_getter import VersionGetter


context_settings = {'help_option_names': ['-h', '--help']}
target_dirs_help = "Target directories to copy (e.g., .husky, \
.github/ISSUE_TEMPLATE). If you don't specify this option, this command \
copies all files of Base Template to the destination repo. If you want to \
copy only root files, use --only-root option."


def validate_lang(ctx, param, value):
    if value not in ('en', 'ja'):
        raise click.BadParameter('Only `en` or `ja` can be used.')

    return value


def validate_options(target_dirs, only_root):
    if len(target_dirs) > 0 and only_root:
        raise click.BadParameter(
            '--target-dirs and --only-root options cannot be used together.')


@click.group(context_settings=context_settings)
@click.version_option(version=VersionGetter.run(),
                      prog_name='Base Template CLI')
def cli():
    """Base Template CLI."""
    pass


@cli.command()
@click.option('-d', '--dst', default='.', help='Destination repo root path.')
@click.option('-t', '--target-dirs', multiple=True, help=target_dirs_help)
@click.option('-r', '--only-root', is_flag=True,
              help='Copy only root directory files of Base Template repo.')
@click.option('-l',
              '--lang',
              default='en',
              help='Language of Base Template. `en` or `ja`.',
              callback=validate_lang)
@click.argument('base_template_root_path')
def apply(dst, target_dirs, only_root, lang, base_template_root_path):
    """Apply (Copy) Base Template boilerplates to the destination repo."""
    validate_options(target_dirs, only_root)

    di_manager = DIManager(
        dst,
        base_template_root_path,
        target_dirs,
        only_root,
        lang)
    applyer = di_manager.getInstance('Applyer')
    applyer.apply()


if __name__ == '__main__':
    cli()
