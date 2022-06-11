import pandas as pd
import config

def activities_with_notes(df):
    """ Extracts the activities after a certain date where soreness/injury
        notes were logged in Strava """
    if config.notes_start_date:
        df = df[pd.to_datetime(df["start_date"]) > config.notes_start_date]
    return df

def has_numbers(string_):
    return any(char.isdigit() for char in string_)

def first_number(string_):
    return int(list(filter(str.isdigit, string_))[0])

def two_first_words(string_):
    return ' '.join(string_.split()[:2])

def first_word(string_):
    return string_.split()[0]

def get_injury(note):
    """ Returns a dictionary with soreness/injury, on different body parts, rated from 0 to 3 """
    note_list = note.lower().split(',')
    injury = {'cheville gauche': 0, 'cheville droite': 0, 'genou gauche': 0, 'genou droite': 0, 
                'hanche gauche': 0, 'hanche droite': 0, 'cuisse gauche': 0, 'cuisse droite': 0, 
                'mollet gauche': 0, 'mollet droite': 0, 'fessier gauche': 0, 'fessier droite': 0}
    
    injury_plural = ['chevilles', 'genoux', 'hanches', 'cuisses', 'mollets', 'fessiers']
    
    for note_el in note_list:
        if has_numbers(note_el):
            rating = first_number(note_el)

            bodypart = two_first_words(note_el)
            if bodypart in injury:
                injury[bodypart] = rating

            bodypart_plural = first_word(note_el)
            if bodypart_plural in injury_plural:
                bodypart_singular = bodypart_plural[:-1]
                injury[bodypart_singular + ' gauche'] = rating
                injury[bodypart_singular + ' droite'] = rating
    
    return injury

def add_injuries(df):
    """ Returns the activity/load dataframe with information about
        soreness/injury in different body parts """
    injury_list = [get_injury(note) for note in df['note']]
    injury_df = pd.DataFrame(injury_list)

    df = pd.concat([df, injury_df], axis=1)
    return df

def add_injury_score(df, bodypart_number):
    """ Returns the last n columns (containing the injury ratings for each body part) """
    df['injury_score'] = df.iloc[:, -bodypart_number:].sum(axis=1)
    return df

def main():
    activities_df = pd.read_pickle('./db/load.pkl')
    activities_df = activities_with_notes(activities_df)
    activities_df = add_injuries(activities_df)
    activities_df = add_injury_score(activities_df, 12)

    activities_df.to_pickle('./db/injury.pkl')

    pd.set_option('display.max_columns', None)
    print(activities_df.shape)
    print(activities_df.head())

if __name__ == '__main__':
    main()