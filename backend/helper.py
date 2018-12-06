from utils.file import File
from episode import Episode

files = []
for t1 in ['Brian', '']:
    for t2 in ['Roger', '', 'Brian']:
        for t3 in ['John', '', 'Brian', 'Roger']:
            for eo in ['Single', 'Double', 'Triple']:
                for a in [True, False]:
                    for se in [[2, 1], [20, 10], [2, 100]]:
                        if se[1] == 100 and not a:
                            continue
                        f = File(
                            s_nr=se[0],
                            e_nr=se[1],
                            series_name='Freddie',
                            title=t1,
                            title2=t2,
                            title3=t3,
                            episode_option=eo,
                            anime=a)
                        f.extension = 'mkv'
                        comp = Episode.compile_file_name(None, f)
                        if comp in files:
                            pass
                        s = ''.join([t1[0] if t1 else '_', t2[0] if t2 else '_',
                                     t3[0] if t3 else '_', 'A' if a else '_', eo[0],
                                    str(len(str(se[0])) + 3), str(len(str(se[1])))])
                        print(s)
                        files.append(comp)

