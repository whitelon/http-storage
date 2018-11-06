from pathlib import Path

from daemon import DaemonContext

from server import run
from setproctitle import setproctitle

sout = open('.log.txt', 'w+')
serr = open('.err.txt', 'w+')

context = DaemonContext(
        working_directory=Path('.'),
        stdout=sout,
        stderr=serr,
        )

with context:
    setproctitle('httpstorage')
    run()
