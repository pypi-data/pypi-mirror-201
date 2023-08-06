import yaml
from copy import deepcopy
import json
from sys import argv


def dump_topic_configs_to_fluvii_format(yaml_fp, as_terminal_input_str=True):
    """
    Dump a topic yaml filepath to a format consumable by fluvii. You can pipe this via:
    python {PATH_TO_THIS_PY_FILE} {PATH_TO_OUR_TOPIC_YAML} | fluvii topics sync
    Or, using dude:
    dude -e {MY_ENV_NAME} exec fluvii topics [create/sync] --topic-config-dict $(python {PATH_TO_THIS_PY_FILE} {PATH_TO_OUR_TOPIC_YAML})
    """
    d = []
    with open(yaml_fp, 'r') as f:
        for line in f.readlines():  # strip Openshift object stuff
            if line.startswith(('data', '  nubium-topics.yaml')):
                pass
            elif line.startswith('kind:'):
                break
            else:
                d.append(line)
    d = yaml.load(''.join(d), yaml.Loader)
    d.pop('.')
    d_out = {}
    for topic in list(d.keys()):
        val = deepcopy(d[topic])
        if 'cluster' in d[topic]:
            del val['cluster']
        val.update(val['configs'].pop('config'))
        val.update(val.pop('configs'))
        val['replication.factor'] = val.pop('replication_factor')
        d_out[topic] = val
    if as_terminal_input_str:
        return json.dumps(d_out, separators=(',', ':'))
    return d_out


if __name__ == '__main__':
    print(dump_topic_configs_to_fluvii_format(argv[1]), end='')
