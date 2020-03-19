cpu_min = 1
cpu_max = 40
mem_min = 0.1
mem_max = 376
gpu_max = 8
gpu_models = ['TITAN X (Pascal)', 'TAITAN Xp', '2080Ti']
gpu_node2gpu_max = {'julia': 2, 'james': 2, 'fred': 2, 'emeril': 8}
simple_gpu_model = {'TITAN X (Pascal)': 'TITANX', 
                    'TITAN Xp': 'TITANXp',
                    'GeForce RTX 2080 Ti': '2080Ti'}
gpu_info_dir = '/g/ssli/sw/roylu/roy_condor_wrapper/.gpu_info/'
gpu_hostnames = {
    'julia',
    'james',
    'fred',
    'emeril',
}
desktop_hostnames = {
    'tui',
    'sparrow',
    'robin',
    'owl',
    'magpie',
    'hummingbird',
    'heron',
    'flamingo',
    'falcon',
    'dove',
    'conure',
    'cardinal',
}
#offline_hostnames = {'emeril'}
offline_hostnames = {}
