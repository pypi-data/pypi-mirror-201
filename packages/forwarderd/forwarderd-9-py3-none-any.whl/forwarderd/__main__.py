import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--systemd-install',
    help='Install as systemd service',
    action='store_true',
    dest='systemd_install'
)

args = parser.parse_args()

if args.systemd_install:
    import os
    import sys

    if not os.path.exists('/run/systemd/system'):
        print('Systemd not found. '
              'This type of installation is not supported on your system.')
        sys.exit()

    template = '\n'.join([
        '[Unit]',
        'Description=SSH port forward daemon',
        'After=network.target',
        '',
        '[Service]',
        'Type=simple',
       f'WorkingDirectory={os.getcwd()}',
       f'ExecStart={sys.executable} -m forwarderd',
        'Restart=always',
    ])

    UNIT_PATH = '/etc/systemd/system/forwarderd.service'

    if os.path.exists(UNIT_PATH):
        print('Unit file already exists. '
              'Use \'systemctl status forwarderd\' to check service status')
        sys.exit()

    try:
        with open(UNIT_PATH, 'w') as file:
            file.write(template)
    except FileNotFoundError:
        print('Systemd service directory not found. '
              'Here is text of .service file, put it in systemd '
              'service directory, then start service with systemctl:')
        print()
        print(template)
    else:
        print(f'Service file created at {UNIT_PATH!r}')
        print('Use \'systemctl start forwarderd\' to start daemon')

else:
    import asyncio

    from . import _daemon

    asyncio.run(_daemon.main())
