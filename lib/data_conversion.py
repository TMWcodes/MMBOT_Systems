import pandas as pd
from data_loader import load_json


def json_to_dataframe(json_file):
    data = load_json(json_file)
    df = pd.DataFrame(data)

    # Convert 'pos' and 'color' lists to strings for display
    df['pos'] = df['pos'].apply(lambda x: ', '.join(map(str, x)) if x else 'None')
    df['color'] = df['color'].apply(lambda x: ', '.join(map(str, x)) if x else 'None')

    # Round the 'time' column to 4 decimal places
    df['time'] = df['time'].round(4)

    # Initialize a list to hold the filtered rows
    filtered_data = []
    held_keys = {}  # Track keys that are held down

    i = 0
    while i < len(df):
        current_row = df.iloc[i].copy()  # Make a copy to avoid SettingWithCopyWarning

        if current_row['type'] == 'keyDown':
            key = current_row['button']

            # Check if the key is held down and suppress duplicate keyDown events
            if key not in held_keys:
                held_keys[key] = True  # Mark the key as held down
                
                # Check if the next event is a 'keyUp' for the same key within 0.2 seconds
                if i + 1 < len(df):
                    next_row = df.iloc[i + 1]
                    if (
                        next_row['type'] == 'keyUp' 
                        and next_row['button'] == key 
                        and next_row['time'] - current_row['time'] <= 0.4
                    ):
                        # Combine 'keyDown' and 'keyUp' into a single 'keyPress' event
                        current_row['type'] = 'keyPress'
                        filtered_data.append(current_row)
                        i += 1  # Skip the next row (keyUp) since it's combined
                    else:
                        # No immediate keyUp, so just add the keyDown event
                        filtered_data.append(current_row)
                else:
                    filtered_data.append(current_row)

        elif current_row['type'] == 'keyUp':
            key = current_row['button']

            # Remove the key from held keys and add keyUp event to the display
            held_keys.pop(key, None)
            filtered_data.append(current_row)

        else:
            # For non-key events, just add them
            filtered_data.append(current_row)

        i += 1

    # Convert the filtered data back to a DataFrame
    df_filtered = pd.DataFrame(filtered_data)
    return df_filtered


