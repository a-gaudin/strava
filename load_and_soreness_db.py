import pandas as pd
import config
import strava_api

def get_load(id):
    """ Returns a dictionary with rates of perceived exertion and notes
        (that may contain soreness/pain information) """
    activity_json = strava_api.get_activity(id) 
    print(f'Returned data for activity {id}')
    perceived_exertion = activity_json['perceived_exertion'] if 'perceived_exertion' in activity_json else float("NaN")
    note = activity_json['private_note'] if 'private_note' in activity_json else ''
    return {'perceived_exertion': perceived_exertion, 'note': note}

def add_load(df):
    """ Returns the activity dataframe with information about training load """
    load_list = [get_load(id) for id in df['id']]
    df['perceived_exertion'] = [x['perceived_exertion'] for x in load_list]
    df['note'] = [x['note'] for x in load_list]

    df['load'] = df['moving_time'] * df['perceived_exertion']
    return df

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

def get_soreness(note):
    """ Returns a dictionary with soreness/pain, on different body parts, rated from 0 to 3 """
    note_list = note.lower().split(',')
    soreness = {'cheville gauche': 0, 'cheville droite': 0, 'genou gauche': 0, 'genou droite': 0, 
                'hanche gauche': 0, 'hanche droite': 0, 'cuisse gauche': 0, 'cuisse droite': 0, 
                'mollet gauche': 0, 'mollet droite': 0, 'fessier gauche': 0, 'fessier droite': 0}
    
    soreness_plural = ['chevilles', 'genoux', 'hanches', 'cuisses', 'mollets', 'fessiers']
    
    for note_el in note_list:
        if has_numbers(note_el):
            rating = first_number(note_el)

            bodypart = two_first_words(note_el)
            if bodypart in soreness:
                soreness[bodypart] = rating

            bodypart_plural = first_word(note_el)
            if bodypart_plural in soreness_plural:
                bodypart_singular = bodypart_plural[:-1]
                soreness[bodypart_singular + ' gauche'] = rating
                soreness[bodypart_singular + ' droite'] = rating
    
    return soreness

def add_soreness(df):
    """ Returns the activity dataframe with information about soreness in different body parts """
    soreness_list = [get_soreness(note) for note in df['note']]
    soreness_df = pd.DataFrame(soreness_list)

    df = pd.concat([df, soreness_df], axis=1)
    return df

def main():
    activities_df = pd.read_pickle('./db/activities.pkl')
    activities_df = add_load(activities_df)

    activities_df.to_pickle('./db/activities_load.pkl')

    activities_df = activities_with_notes(activities_df)
    activities_df = add_soreness(activities_df)
    
    activities_df.to_pickle('./db/activities_load_soreness.pkl')

    pd.set_option('display.max_columns', None)
    print(activities_df.shape)
    print(activities_df.head())

if __name__ == '__main__':
    main()