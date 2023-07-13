def parse_string(df):
    df['time'] = df['time'].str.replace(r'W po.udnie', 'W południe', regex=True)
    df['time'] = df['time'].str.replace(r'Wiecz.r', 'Wieczór', regex=True)

    df['hobby'] = df['hobby'].str.replace(r'W.dkarstwo', 'Wędkarstwo', regex=True)

    df['knowledge'] = df['knowledge'].str.replace(r'Pocz.tkuj.cy', 'Początkujący', regex=True)
    df['knowledge'] = df['knowledge'].str.replace(r'.redniozaawansowany', 'Średniozaawansowany', regex=True)

    df['challenge_type'] = df['challenge_type'].str.replace(r'Lod.wka', 'Lodówka', regex=True)
