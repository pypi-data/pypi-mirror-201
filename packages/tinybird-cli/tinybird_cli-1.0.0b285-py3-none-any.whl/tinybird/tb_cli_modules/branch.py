
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Any, Dict, List, Tuple
import click
from click import Context
import yaml

from tinybird.client import TinyB
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import coro, get_config_and_hosts, \
    create_workspace_branch, switch_workspace, switch_to_workspace_by_user_workspace_data, \
    print_current_workspace, _get_config, print_data_branch_summary, echo_safe_humanfriendly_tables_format_smart_table, \
    get_current_main_workspace, get_current_workspace_branches, MAIN_BRANCH, print_current_branch, \
    merge_workspace_branch, print_branch_regression_tests_summary
from tinybird.feedback_manager import FeedbackManager
from tinybird.datafile import wait_job
from tinybird.config import VERSION


@cli.group(hidden=True)
@click.pass_context
def branch(ctx: Context) -> None:
    """Branch commands.
    """


@branch.command(name="ls", hidden=True)
@click.pass_context
@coro
async def branch_ls(ctx: Context) -> None:
    """List all the branches from the workspace token.
    """

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client = obj['client']
    config = obj['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    current_main_workspace = await get_current_main_workspace(client, config)

    if current_main_workspace['id'] != config['id']:
        client = TinyB(current_main_workspace['token'], config['host'], version=VERSION)

    response = await client.branches()

    columns = ['name', 'id', 'current']
    table: List[Tuple[str, str, bool]] = [(MAIN_BRANCH, current_main_workspace['id'], config['id'] == current_main_workspace['id'])]

    for branch in response['branches']:
        table.append((branch['name'], branch['id'], config['id'] == branch['id']))

    await print_current_workspace(ctx)

    click.echo(FeedbackManager.info_branches())
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@branch.command(name='use', hidden=True)
@click.argument('branch_name_or_id')
@click.pass_context
@coro
async def branch_use(
    ctx: Context,
    branch_name_or_id: str
) -> None:
    """Switch to another branch. Use 'tb branch ls' to list the branches you have access to.
    """

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    current_main_workspace = await get_current_main_workspace(client, config)
    if branch_name_or_id == MAIN_BRANCH:
        await switch_to_workspace_by_user_workspace_data(ctx, current_main_workspace)
    else:
        await switch_workspace(ctx, branch_name_or_id, only_branches=True)


@branch.command(name='current', hidden=True)
@click.pass_context
@coro
async def branch_current(ctx: Context) -> None:
    """Show the branch you're currently authenticated into.
    """

    await print_current_branch(ctx)


@branch.command(name='create', short_help="Create a new Branch from the Workspace you are authenticated", hidden=True)
@click.argument('branch_name', required=False)
@click.option('--last-partition', is_flag=True, default=False, help="When enabled, last modified partition is attached from the origin Workspace to the Branch")
@click.option('--all', is_flag=True, default=False, help="When enabled, all data from the origin Workspace is attached to the Branch. Use only if you actually need all the data in the branch.")
@click.option('--wait', is_flag=True, default=False, help="Waits for data branch jobs to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def create_branch(
    ctx: Context,
    branch_name: str,
    last_partition: bool,
    all: bool,
    wait: bool
) -> None:

    if last_partition and all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all but not both"))
        return

    await create_workspace_branch(ctx, branch_name, last_partition, all, wait)


@branch.command(name='rm', short_help="Removes a Branch for your Tinybird user and it can't be recovered.", hidden=True)
@click.argument('branch_name_or_id')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def delete_branch(
    ctx: Context,
    branch_name_or_id: str,
    yes: bool
) -> None:
    """Remove a branch where you are an admin.
    """

    client: TinyB = ctx.ensure_object(dict)['client']
    config, _, _ = await get_config_and_hosts(ctx)

    if branch_name_or_id == MAIN_BRANCH:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    try:
        workspace_branches = await get_current_workspace_branches(client, config)
        workspace_to_delete = next((workspace for workspace in workspace_branches
                                    if workspace['name'] == branch_name_or_id or workspace['id'] == branch_name_or_id),
                                   None)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return

    if not workspace_to_delete:
        raise click.ClickException(FeedbackManager.error_branch(branch=branch_name_or_id))

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_branch(branch=workspace_to_delete['name'])):
        need_to_switch_to_main = workspace_to_delete.get('main') and config['id'] == workspace_to_delete['id']
        # get origin workspace if deleting current branch
        if need_to_switch_to_main:
            try:
                workspaces = (await client.user_workspaces()).get('workspaces', [])
                workspace_main = next((workspace for workspace in workspaces if
                                       workspace['id'] == workspace_to_delete['main']), None)
            except Exception:
                workspace_main = None
        try:
            await client.delete_branch(workspace_to_delete['id'])
            click.echo(FeedbackManager.success_branch_deleted(branch_name=workspace_to_delete['name']))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return
        else:
            if need_to_switch_to_main:
                if workspace_main:
                    await switch_to_workspace_by_user_workspace_data(ctx, workspace_main)
                else:
                    click.echo(FeedbackManager.error_switching_to_main())


@branch.command(name='data', short_help="Perform a data branch operation, see flags for details", hidden=True)
@click.option('--last-partition', is_flag=True, default=False, help="When enabled, last modified partition is attached from the origin Workspace to the Branch")
@click.option('--all', is_flag=True, default=False, help="When enabled, all data from the origin Workspace is attached to the Branch. Use only if you actually need all the data in the branch.")
@click.option('--wait', is_flag=True, default=False, help="Waits for data branch jobs to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def data_branch(
    ctx: Context,
    last_partition: bool,
    all: bool,
    wait: bool
) -> None:

    if last_partition and all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all but not both"))
        return

    if not last_partition and not all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all"))
        return

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client = obj['client']
    config = obj['config']

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace['id'] == config['id']:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    try:
        response = await client.branch_workspace_data(config['id'], last_partition, all)
        if all:
            if 'job' not in response:
                raise click.ClickException(response)
            job_id = response['job']['job_id']
            job_url = response['job']['job_url']
            click.echo(FeedbackManager.info_data_branch_job_url(url=job_url))
            if wait:
                await wait_job(client, job_id, job_url, 'Data Branching')
                await print_data_branch_summary(client, job_id)
        else:
            await print_data_branch_summary(client, None, response)
            click.echo(FeedbackManager.success_workspace_data_branch())
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


@branch.group("regression-tests", invoke_without_command=True)
@click.option('-f', '--filename', type=click.Path(exists=True), required=False, help="yaml file with regression-tests definition")
@click.option('--wait', is_flag=True, default=False, help="Waits for regression job to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def regression_tests(ctx, filename: str, wait: bool):
    '''Branch regression-tests commands'''
    if filename:
        with open(filename, 'r') as file:
            regression_tests_commands = yaml.safe_load(file)
        client: TinyB = ctx.ensure_object(dict)['client']
        config = ctx.ensure_object(dict)['config']

        current_main_workspace = await get_current_main_workspace(client, config)
        if current_main_workspace['id'] == config['id']:
            click.echo(FeedbackManager.error_not_allowed_in_main_branch())
            return
        try:
            response = await client.branch_regression_tests_file(config['id'], regression_tests_commands)
            if 'job' not in response:
                raise click.ClickException(response)
            job_id = response['job']['job_id']
            job_url = response['job']['job_url']
            click.echo(FeedbackManager.info_regression_tests_branch_job_url(url=job_url))
            if wait:
                await wait_job(client, job_id, job_url, 'Regression tests')
                await print_branch_regression_tests_summary(client, job_id, config['host'])
        except click.ClickException as e:
            raise e
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return


@regression_tests.command(name='coverage', short_help="Run regression tests using coverage requests for branch vs main. It creates a regression-tests job", hidden=True)
@click.argument('pipe_name', required=False)
@click.option('--sample-by-params', type=click.IntRange(1, 100), default=1, required=False, help="When set, we will aggregate the pipe_stats_rt requests by extractURLParameterNames(assumeNotNull(url)) and for each combination we will take a sample of N requests")
@click.option('-m', '--match', multiple=True, required=False, help="Filter the checker requests by specific parameter. You can pass multiple parameters -m foo -m bar")
@click.option('--only-response-times', is_flag=True, default=False, help="Checks only response times")
@click.option('-ff', '--failfast', is_flag=True, default=False, help="When set, the checker will exit as soon one test fails")
@click.option('--ignore-order', is_flag=True, default=False, help="When set, the checker will ignore the order of list properties")
@click.option('--validate-processed-bytes', is_flag=True, default=False, help="When set, the checker will validate that the new version doesn't process more than 25% than the current version")
@click.option('--wait', is_flag=True, default=False, help="Waits for regression job to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def coverage(ctx: Context, pipe_name: str, sample_by_params: int, match: List[str],
                   only_response_times: bool, failfast: bool, ignore_order: bool, validate_processed_bytes: bool, wait: bool):
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace['id'] == config['id']:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return
    try:
        response = await client.branch_regression_tests(config['id'], [pipe_name],
                                                        'coverage',
                                                        samples_by_params=sample_by_params,
                                                        matches=match if match else [],
                                                        only_response_times=only_response_times,
                                                        failfast=failfast,
                                                        ignore_order=ignore_order, validate_processed_bytes=validate_processed_bytes)
        if 'job' not in response:
            raise click.ClickException(response)
        job_id = response['job']['job_id']
        job_url = response['job']['job_url']
        click.echo(FeedbackManager.info_regression_tests_branch_job_url(url=job_url))
        if wait:
            await wait_job(client, job_id, job_url, 'Regression tests')
            await print_branch_regression_tests_summary(client, job_id, config['host'])
    except click.ClickException as e:
        raise e
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


@regression_tests.command(name='last', short_help="Run regression tests using last requests for branch vs main. It creates a regression-tests job", hidden=True)
@click.argument('pipe_name', required=False)
@click.option('-l', '--limit', type=click.IntRange(0, 100), default=0, required=False, help="Number of requests to validate")
@click.option('-m', '--match', multiple=True, required=False, help="Filter the checker requests by specific parameter. You can pass multiple parameters -m foo -m bar")
@click.option('--only-response-times', is_flag=True, default=False, help="Checks only response times")
@click.option('-ff', '--failfast', is_flag=True, default=False, help="When set, the checker will exit as soon one test fails")
@click.option('--ignore-order', is_flag=True, default=False, help="When set, the checker will ignore the order of list properties")
@click.option('--validate-processed-bytes', is_flag=True, default=False, help="When set, the checker will validate that the new version doesn't process more than 25% than the current version")
@click.option('--wait', is_flag=True, default=False, help="Waits for regression job to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def last(ctx: Context, pipe_name: str, limit: int, match: List[str],
               only_response_times: bool, failfast: bool, ignore_order: bool, validate_processed_bytes: bool, wait: bool):
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace['id'] == config['id']:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return
    try:
        response = await client.branch_regression_tests(config['id'], [pipe_name],
                                                        'last',
                                                        limit=limit,
                                                        matches=match if match else [],
                                                        only_response_times=only_response_times,
                                                        failfast=failfast,
                                                        ignore_order=ignore_order, validate_processed_bytes=validate_processed_bytes)
        if 'job' not in response:
            raise click.ClickException(response)
        job_id = response['job']['job_id']
        job_url = response['job']['job_url']
        click.echo(FeedbackManager.info_regression_tests_branch_job_url(url=job_url))
        if wait:
            await wait_job(client, job_id, job_url, 'Regression tests')
            await print_branch_regression_tests_summary(client, job_id, config['host'])
    except click.ClickException as e:
        raise e
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


@regression_tests.command(name='manual', short_help="Run regression tests using manual requests for branch vs main. It creates a regression-tests job", hidden=True,
                          context_settings=dict(allow_extra_args=True, ignore_unknown_options=True))
@click.argument('pipe_name', required=False)
@click.option('--only-response-times', is_flag=True, default=False, help="Checks only response times")
@click.option('-ff', '--failfast', is_flag=True, default=False, help="When set, the checker will exit as soon one test fails")
@click.option('--ignore-order', is_flag=True, default=False, help="When set, the checker will ignore the order of list properties")
@click.option('--validate-processed-bytes', is_flag=True, default=False, help="When set, the checker will validate that the new version doesn't process more than 25% than the current version")
@click.option('--wait', is_flag=True, default=False, help="Waits for regression job to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def manual(ctx: Context, pipe_name: str, only_response_times: bool,
                 failfast: bool, ignore_order: bool, validate_processed_bytes: bool, wait: bool):
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    params = [{ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}]

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace['id'] == config['id']:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return
    try:
        response = await client.branch_regression_tests(config['id'], [pipe_name],
                                                        'manual',
                                                        params=params if params else [],
                                                        only_response_times=only_response_times,
                                                        failfast=failfast,
                                                        ignore_order=ignore_order, validate_processed_bytes=validate_processed_bytes)
        if 'job' not in response:
            raise click.ClickException(response)
        job_id = response['job']['job_id']
        job_url = response['job']['job_url']
        click.echo(FeedbackManager.info_regression_tests_branch_job_url(url=job_url))
        if wait:
            await wait_job(client, job_id, job_url, 'Regression tests')
            await print_branch_regression_tests_summary(client, job_id, config['host'])
    except click.ClickException as e:
        raise e
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


@branch.command(name='merge', short_help="Merge a Branch to main. It creates a deployment job", hidden=True)
@click.option('--wait', is_flag=True, default=False, help="Waits for data branch jobs to finish, showing a progress bar. Disabled by default.")
@click.option('--verbose', is_flag=True, default=False, help="Print DEBUG logs.")
@click.pass_context
@coro
async def merge_branch(
    ctx: Context,
    wait: bool,
    verbose: bool
) -> None:

    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace['id'] == config['id']:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    await merge_workspace_branch(ctx, config['id'], current_main_workspace, wait, verbose)


@branch.group()
@click.pass_context
def datasource(ctx: Context) -> None:
    """Branch data source commands.
    """


@datasource.command(name="copy")
@click.argument('datasource_name')
@click.option('--sql', default=None, help='SQL query to copy', hidden=True, required=False)
@click.option('--sql-from-main', is_flag=True, default=False, help='SQL query from main to copy', hidden=True, required=False)
@click.option('--wait', is_flag=True, default=False, help="Wait for copy job to finish, disabled by default")
@click.pass_context
@coro
async def datasource_copy_from_main(
    ctx: Context,
    datasource_name: str,
    sql: str,
    sql_from_main: bool,
    wait: bool
) -> None:
    """Copy data source from main.
    """

    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    if sql and sql_from_main:
        click.echo(FeedbackManager.error_exception(error="Use --sql or --sql-from-main but not both"))
        return

    if not sql and not sql_from_main:
        click.echo(FeedbackManager.error_exception(error="Use --sql or --sql-from-main"))
        return

    current_main_workspace = await get_current_main_workspace(client, config)
    if current_main_workspace['id'] == config['id']:
        click.echo(FeedbackManager.error_not_allowed_in_main_branch())
        return

    response = await client.datasource_query_copy(datasource_name, sql if sql else f"SELECT * FROM main.{datasource_name}")
    if 'job' not in response:
        raise click.ClickException(response)
    job_id = response['job']['job_id']
    job_url = response['job']['job_url']
    if sql:
        click.echo(FeedbackManager.info_copy_with_sql_job_url(sql=sql,
                                                              datasource_name=datasource_name,
                                                              url=job_url))
    else:
        click.echo(FeedbackManager.info_copy_from_main_job_url(datasource_name=datasource_name, url=job_url))
    if wait:
        base_msg = 'Copy from main' if sql_from_main else f'Copy from {sql}'
        await wait_job(client, job_id, job_url, f"{base_msg} to {datasource_name}")
