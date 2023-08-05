ac_table = {
    'commands': [
        '--help',
        '--version',
        '--version-full',
        'executor',
        'flow',
        'ping',
        'export',
        'new',
        'gateway',
        'auth',
        'hub',
        'cloud',
        'help',
        'pod',
        'deployment',
        'client',
    ],
    'completions': {
        'executor': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--workspace-id',
            '--extra-search-paths',
            '--timeout-ctrl',
            '--k8s-namespace',
            '--polling',
            '--shards',
            '--replicas',
            '--native',
            '--uses',
            '--uses-with',
            '--uses-metas',
            '--uses-requests',
            '--uses-dynamic-batching',
            '--py-modules',
            '--output-array-type',
            '--exit-on-exceptions',
            '--no-reduce',
            '--disable-reduce',
            '--grpc-server-options',
            '--raft-configuration',
            '--grpc-channel-options',
            '--entrypoint',
            '--docker-kwargs',
            '--volumes',
            '--gpus',
            '--disable-auto-volume',
            '--host',
            '--host-in',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--env-from-secret',
            '--shard-id',
            '--pod-role',
            '--noblock-on-start',
            '--floating',
            '--replica-id',
            '--reload',
            '--install-requirements',
            '--port',
            '--ports',
            '--monitoring',
            '--port-monitoring',
            '--retries',
            '--tracing',
            '--traces-exporter-host',
            '--traces-exporter-port',
            '--metrics',
            '--metrics-exporter-host',
            '--metrics-exporter-port',
            '--stateful',
            '--pod-ports',
            '--force-update',
            '--force',
            '--prefer-platform',
            '--compression',
            '--uses-before-address',
            '--uses-after-address',
            '--connection-list',
            '--timeout-send',
        ],
        'flow': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--workspace-id',
            '--suppress-root-logging',
            '--uses',
            '--reload',
            '--env',
            '--inspect',
        ],
        'ping': [
            '--help',
            'flow',
            'executor',
            'gateway',
            '--timeout',
            '--attempts',
            '--min-successful-attempts',
        ],
        'export flowchart': ['--help', '--vertical-layout'],
        'export kubernetes': ['--help', '--k8s-namespace'],
        'export docker-compose': ['--help', '--network_name'],
        'export schema': ['--help', '--yaml-path', '--json-path', '--schema-path'],
        'export': ['--help', 'flowchart', 'kubernetes', 'docker-compose', 'schema'],
        'new': ['--help', '--type'],
        'gateway': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--workspace-id',
            '--extra-search-paths',
            '--timeout-ctrl',
            '--k8s-namespace',
            '--entrypoint',
            '--docker-kwargs',
            '--prefetch',
            '--title',
            '--description',
            '--cors',
            '--no-debug-endpoints',
            '--no-crud-endpoints',
            '--expose-endpoints',
            '--uvicorn-kwargs',
            '--ssl-certfile',
            '--ssl-keyfile',
            '--expose-graphql-endpoint',
            '--protocol',
            '--protocols',
            '--host',
            '--host-in',
            '--proxy',
            '--uses',
            '--uses-with',
            '--py-modules',
            '--replicas',
            '--grpc-server-options',
            '--grpc-channel-options',
            '--graph-description',
            '--graph-conditions',
            '--deployments-addresses',
            '--deployments-metadata',
            '--deployments-no-reduce',
            '--deployments-disable-reduce',
            '--compression',
            '--timeout-send',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--env-from-secret',
            '--shard-id',
            '--pod-role',
            '--noblock-on-start',
            '--floating',
            '--replica-id',
            '--reload',
            '--port',
            '--ports',
            '--port-expose',
            '--port-in',
            '--monitoring',
            '--port-monitoring',
            '--retries',
            '--tracing',
            '--traces-exporter-host',
            '--traces-exporter-port',
            '--metrics',
            '--metrics-exporter-host',
            '--metrics-exporter-port',
            '--stateful',
            '--pod-ports',
        ],
        'auth login': ['--help', '--force'],
        'auth logout': ['--help'],
        'auth token create': ['--help', '--expire', '--format'],
        'auth token delete': ['--help'],
        'auth token list': ['--help'],
        'auth token': ['--help', 'create', 'delete', 'list'],
        'auth': ['--help', 'login', 'logout', 'token'],
        'hub new': [
            '--help',
            '--name',
            '--path',
            '--advance-configuration',
            '--description',
            '--keywords',
            '--url',
            '--dockerfile',
        ],
        'hub push': [
            '--help',
            '--no-usage',
            '--verbose',
            '--dockerfile',
            '--tag',
            '--protected-tag',
            '--force-update',
            '--force',
            '--build-env',
            '--platform',
            '--secret',
            '--no-cache',
            '--public',
            '--private',
        ],
        'hub pull': [
            '--help',
            '--no-usage',
            '--force-update',
            '--force',
            '--prefer-platform',
            '--install-requirements',
        ],
        'hub status': ['--help', '--id', '--verbose', '--replay'],
        'hub list': ['--help'],
        'hub': ['--help', 'new', 'push', 'pull', 'status', 'list'],
        'cloud login': ['--help'],
        'cloud logout': ['--help'],
        'cloud deploy': ['--help'],
        'cloud normalize': ['--help', '--output', '--verbose'],
        'cloud list': ['--help', '--phase', '--name', '--labels'],
        'cloud status': ['--help', '--verbose'],
        'cloud remove': ['--help', '--phase'],
        'cloud new': ['--help'],
        'cloud update': ['--help'],
        'cloud restart': ['--help', '--gateway', '--executor'],
        'cloud pause': ['--help'],
        'cloud resume': ['--help'],
        'cloud scale': ['--help', '--executor', '--replicas'],
        'cloud recreate': ['--help'],
        'cloud survey': ['--help'],
        'cloud': [
            '--help',
            '--version',
            '--loglevel',
            'login',
            'logout',
            'deploy',
            'normalize',
            'list',
            'status',
            'remove',
            'new',
            'update',
            'restart',
            'pause',
            'resume',
            'scale',
            'recreate',
            'survey',
        ],
        'help': ['--help'],
        'pod': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--workspace-id',
            '--extra-search-paths',
            '--timeout-ctrl',
            '--k8s-namespace',
            '--polling',
            '--shards',
            '--replicas',
            '--native',
            '--uses',
            '--uses-with',
            '--uses-metas',
            '--uses-requests',
            '--uses-dynamic-batching',
            '--py-modules',
            '--output-array-type',
            '--exit-on-exceptions',
            '--no-reduce',
            '--disable-reduce',
            '--grpc-server-options',
            '--raft-configuration',
            '--grpc-channel-options',
            '--entrypoint',
            '--docker-kwargs',
            '--volumes',
            '--gpus',
            '--disable-auto-volume',
            '--host',
            '--host-in',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--env-from-secret',
            '--shard-id',
            '--pod-role',
            '--noblock-on-start',
            '--floating',
            '--replica-id',
            '--reload',
            '--install-requirements',
            '--port',
            '--ports',
            '--monitoring',
            '--port-monitoring',
            '--retries',
            '--tracing',
            '--traces-exporter-host',
            '--traces-exporter-port',
            '--metrics',
            '--metrics-exporter-host',
            '--metrics-exporter-port',
            '--stateful',
            '--pod-ports',
            '--force-update',
            '--force',
            '--prefer-platform',
            '--compression',
            '--uses-before-address',
            '--uses-after-address',
            '--connection-list',
            '--timeout-send',
        ],
        'deployment': [
            '--help',
            '--name',
            '--workspace',
            '--log-config',
            '--quiet',
            '--quiet-error',
            '--workspace-id',
            '--extra-search-paths',
            '--timeout-ctrl',
            '--k8s-namespace',
            '--polling',
            '--shards',
            '--replicas',
            '--native',
            '--uses',
            '--uses-with',
            '--uses-metas',
            '--uses-requests',
            '--uses-dynamic-batching',
            '--py-modules',
            '--output-array-type',
            '--exit-on-exceptions',
            '--no-reduce',
            '--disable-reduce',
            '--grpc-server-options',
            '--raft-configuration',
            '--grpc-channel-options',
            '--entrypoint',
            '--docker-kwargs',
            '--volumes',
            '--gpus',
            '--disable-auto-volume',
            '--host',
            '--host-in',
            '--runtime-cls',
            '--timeout-ready',
            '--env',
            '--env-from-secret',
            '--shard-id',
            '--pod-role',
            '--noblock-on-start',
            '--floating',
            '--replica-id',
            '--reload',
            '--install-requirements',
            '--port',
            '--ports',
            '--monitoring',
            '--port-monitoring',
            '--retries',
            '--tracing',
            '--traces-exporter-host',
            '--traces-exporter-port',
            '--metrics',
            '--metrics-exporter-host',
            '--metrics-exporter-port',
            '--stateful',
            '--pod-ports',
            '--force-update',
            '--force',
            '--prefer-platform',
            '--compression',
            '--uses-before-address',
            '--uses-after-address',
            '--connection-list',
            '--timeout-send',
            '--uses-before',
            '--uses-after',
            '--when',
            '--external',
            '--grpc-metadata',
            '--deployment-role',
            '--tls',
        ],
        'client': [
            '--help',
            '--proxy',
            '--host',
            '--host-in',
            '--port',
            '--tls',
            '--asyncio',
            '--tracing',
            '--traces-exporter-host',
            '--traces-exporter-port',
            '--metrics',
            '--metrics-exporter-host',
            '--metrics-exporter-port',
            '--log-config',
            '--protocol',
            '--grpc-channel-options',
            '--prefetch',
            '--suppress-root-logging',
        ],
    },
}
