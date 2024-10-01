import numpy as np
from scipy.stats import entropy


def calculate_shannon_entropy(sequence):
    unique, counts = np.unique(sequence, axis=0, return_counts=True)
    probs = counts / len(sequence)
    shannon_entropy = entropy(probs)
    return shannon_entropy

def count_repeated_sequences(coordinates, min_sequence_length=5, min_repetitions=2):
    sequences = {}
    for i in range(len(coordinates) - min_sequence_length + 1):
        sequence = tuple(tuple(coord) for coord in coordinates[i:i + min_sequence_length])
        if sequence in sequences:
            sequences[sequence].append(i)
        else:
            sequences[sequence] = [i]

    repeated_sequence_count = sum(1 for indices in sequences.values() if len(indices) >= min_repetitions)
    return repeated_sequence_count

def detect_repeated_sequences(coordinates, min_sequence_length=5, min_repetitions=2):
    sequences = {}
    for i in range(len(coordinates) - min_sequence_length + 1):
        sequence = tuple(tuple(coord) for coord in coordinates[i:i + min_sequence_length])
        if sequence in sequences:
            sequences[sequence].append(i)
        else:
            sequences[sequence] = [i]

    repeated_sequences = {seq: indices for seq, indices in sequences.items() if len(indices) >= min_repetitions}
    return repeated_sequences

def plot_autocorrelation(sequence, repetitions, figsize=(12, 6), max_lag=50):
    """
    Plot the multidimensional autocorrelation of a sequence of coordinate pairs.
    
    Parameters:
    - sequence: numpy array of shape (n, 2) where n is the number of coordinate pairs.
    - repetitions: int, the number of times the sequence is repeated.
    - figsize: tuple, the size of the figure (width, height) in inches.
    - max_lag: int, maximum number of lags to display in the plot.
    
    """
    
    def multidimensional_autocorrelation(sequence):
        # Flatten the 2D sequence into a 1D array
        flat_sequence = sequence.flatten()
        
        n = len(flat_sequence)
        variance = np.var(flat_sequence)
        flat_sequence = flat_sequence - np.mean(flat_sequence)
        
        # Compute the autocorrelation
        r = np.correlate(flat_sequence, flat_sequence, mode='full')[-n:]
        result = r / (variance * (np.arange(n, 0, -1)))
        
        return result
    
    # Repeat the sequence to simulate multiple repetitions
    sequence_repeated = np.tile(sequence, (repetitions, 1))
    
    # Compute multidimensional autocorrelation
    acf = multidimensional_autocorrelation(sequence_repeated)
    
    # Calculate a simple metric, such as the mean of the first few lags
    autocorr_metric = np.mean(acf[:len(sequence)]) * 1000
    
    # Plot the autocorrelation with custom figure size
    # plt.figure(figsize=figsize)  # Create a new figure
    # lags = range(min(len(acf), max_lag))
    # plt.stem(lags, acf[:max_lag], linefmt='-', markerfmt='o', basefmt=' ')
    # plt.xlabel('Lag')
    # plt.ylabel('Autocorrelation')
    # plt.title(f'Multidimensional Autocorrelation of Coordinate Pairs (Repeated {repetitions} times)')
    # plt.show()  # Display the plot
    # plt.close()  # Close the figure to prevent empty windows
    
    # print(f"Autocorrelation metric for {repetitions} repetitions: {autocorr_metric}")

    return autocorr_metric
