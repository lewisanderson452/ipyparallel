import atexit
from subprocess import Popen
import sys


def start_cluster(depth, cluster_id, number_of_engines):
    ipcontroller_cmd = (
        f'ipcontroller --debug --profile=asv '
        f'{f"--cluster-id={cluster_id}" if cluster_id else ""} '
        f'--HubFactory.broadcast_scheduler_depth={depth}'
    )
    print(ipcontroller_cmd)
    ipengine_cmd = f'ipengine --debug --profile=asv ' \
                   f'{f"--cluster-id={cluster_id}" if cluster_id else ""}'
    ps = [
        Popen(
            ipcontroller_cmd.split(),
            stdout=sys.stdout,
            stderr=sys.stdout,
            stdin=sys.stdin,
        )
    ]
    print(ipengine_cmd)
    for i in range(number_of_engines):
        ps.append(
            Popen(
                ipengine_cmd.split(),
                stdout=sys.stdout,
                stderr=sys.stdout,
                stdin=sys.stdin,
            )
        )

    return ps

if __name__ == '__main__':
    if len(sys.argv) > 3:
        depth = sys.argv[1]
        cluster_id = sys.argv[2]
        number_of_engines = int(sys.argv[3])
    else:
        depth = 3
        cluster_id = ''
        number_of_engines = 30

    ps = start_cluster(depth, cluster_id, number_of_engines)

    for p in ps:
        p.wait()

    def clean_up():
        for p in ps:
            p.kill()

    atexit.register(clean_up)
