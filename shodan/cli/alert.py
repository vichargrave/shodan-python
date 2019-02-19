import click
import shodan

from shodan.cli.helpers import get_api_key


@click.group()
def alert():
    """Manage the network alerts for your account"""
    pass


@alert.command(name='clear')
def alert_clear():
    """Remove all alerts"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        alerts = api.alerts()
        for alert in alerts:
            click.echo(u'Removing {} ({})'.format(alert['name'], alert['id']))
            api.delete_alert(alert['id'])
    except shodan.APIError as e:
        raise click.ClickException(e.value)
    click.echo("Alerts deleted")


@alert.command(name='create')
@click.argument('name', metavar='<name>')
@click.argument('netblock', metavar='<netblock>')
def alert_create(name, netblock):
    """Create a network alert to monitor an external network"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        alert = api.create_alert(name, netblock)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    click.secho('Successfully created network alert!', fg='green')
    click.secho('Alert ID: {}'.format(alert['id']), fg='cyan')


@alert.command(name='list')
@click.option('--expired', help='Whether or not to show expired alerts.', default=True, type=bool)
def alert_list(expired):
    """List all the active alerts"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        results = api.alerts(include_expired=expired)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    if len(results) > 0:
        click.echo(u'# {:14} {:<21} {:<15s}'.format('Alert ID', 'Name', 'IP/ Network'))

        for alert in results:
            click.echo(
                u'{:16} {:<30} {:<35} '.format(
                    click.style(alert['id'], fg='yellow'),
                    click.style(alert['name'], fg='cyan'),
                    click.style(', '.join(alert['filters']['ip']), fg='white')
                ),
                nl=False
            )

            if 'triggers' in alert and alert['triggers']:
                click.secho('Triggers: ', fg='magenta', nl=False)
                click.echo(', '.join(alert['triggers'].keys()), nl=False)

            if 'expired' in alert and alert['expired']:
                click.secho('expired', fg='red')
            else:
                click.echo('')
    else:
        click.echo("You haven't created any alerts yet.")


@alert.command(name='remove')
@click.argument('alert_id', metavar='<alert ID>')
def alert_remove(alert_id):
    """Remove the specified alert"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        api.delete_alert(alert_id)
    except shodan.APIError as e:
        raise click.ClickException(e.value)
    click.echo("Alert deleted")


@alert.command(name='triggers')
def alert_list_triggers():
    """List all the available triggers"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        results = api.alert_triggers()
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    if len(results) > 0:
        click.echo(u'# {:14} {:<21} {:<15s}'.format('Name', 'Description', 'Rule'))

        for trigger in results:
            click.echo(
                u'{:16} {:<30} {:<35} '.format(
                    click.style(trigger['name'], fg='yellow'),
                    click.style(trigger['description'], fg='cyan'),
                    trigger['rule']
                )
            )
    else:
        click.echo("No triggers currently available.")


@alert.command(name='enable')
@click.argument('alert_id', metavar='<alert ID>')
@click.argument('trigger', metavar='<trigger name>')
def alert_enable_trigger(alert_id, trigger):
    """Enable a trigger for the alert"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        api.enable_alert_trigger(alert_id, trigger)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    click.secho('Successfully enabled the trigger {}'.format(trigger), color='green')


@alert.command(name='disable')
@click.argument('alert_id', metavar='<alert ID>')
@click.argument('trigger', metavar='<trigger name>')
def alert_disable_trigger(alert_id, trigger):
    """Disable a trigger for the alert"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        api.disable_alert_trigger(alert_id, trigger)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    click.secho('Successfully disabled the trigger {}'.format(trigger), color='green')
