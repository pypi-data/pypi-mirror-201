import numpy as np
import matplotlib.pyplot as plt

class BlockingTimeSeriesSplit():

    """
    BlockingTimeSeriesSplit is a variation of TimeSeriesSplit that splits the data into n_splits blocks of equal size.
    https://towardsdatascience.com/4-things-to-do-when-applying-cross-validation-with-time-series-c6a5674ebf3a
    https://neptune.ai/blog/cross-validation-mistakes
    """
    def __init__(self, n_splits:int):
        """
        Parameters
        ----------
        n_splits : int
            Number of splits.
        """
        self.n_splits = n_splits
    
    def get_n_splits(self, X, y, groups):
        """
        Returns the number of splitting iterations in the cross-validator.

        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """
        return self.n_splits
    
    def split(self, X, y=None, groups=None):
        """
        Generate indices to split data into training and test set.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        y : array-like, shape (n_samples,)
            The target variable for supervised learning problems.
        groups : array-like, with shape (n_samples,), optional
            Group labels for the samples used while splitting the dataset into
            train/test set.

        Returns
        -------
        yield indices[start: mid], indices[mid + margin: stop] : generator
        """
        n_samples = len(X)
        k_fold_size = n_samples // self.n_splits
        indices = np.arange(n_samples)

        margin = 0
        for i in range(self.n_splits):
            start = i * k_fold_size
            stop = start + k_fold_size
            mid = int(0.5 * (stop - start)) + start
            yield indices[start: mid], indices[mid + margin: stop]


def plot_timesplit(n_splits,n_samples,test_size=None ,text=False,figsize=(20,10)):

    """
    Plot the train and test size depending on the number of splits for TimeSeriesSplit

    Parameters
    ----------
    n_splits : int
        Number of splits.

    n_samples : int
        Number of samples.
    
    test_size : int, optional
        Size of the test set, by default None
    
    text : bool, optional
        Add the percentage of the train and test size to the side of the bar, by default False

    Returns
    -------
    None
        Plot the train and test size depending on the number of splits for TimeSeriesSplit
    """

    n_splits=n_splits
    n_samples=n_samples
    if test_size is None:
        test_size= n_samples // (n_splits+1)
    train_size=[]
    test_size_=[]
    plt.figure(figsize=figsize)
    for i in reversed(range(1,n_splits+1)):
        train_set=i * n_samples // (n_splits + 1) + n_samples % (n_splits + 1)
        train_size.append(train_set)
        test_size_.append(test_size)
    plt.barh(np.arange(1,n_splits+1),train_size)
    plt.barh(np.arange(1,n_splits+1),test_size_, left=train_size)
    plt.legend(["Train Size", "Test Size"])
    plt.xlabel("Number of Splits")
    plt.ylabel("Size")
    plt.title("Train and Test Size depending on the number of splits")
    #add the percentage of the train and test size to the side of the bar
    if text == True:
        for i in range(n_splits):
            plt.text(train_size[i]+test_size_[i]+1000, i+1, f"Train: {train_size[i]*100/n_samples:.2f}%  Test: {test_size_[i]*100/n_samples:.2f}%", fontsize=7)

        #extend the frame to the right to make room for the text
        plt.xlim(0, n_samples+n_samples*0.43)

    plt.show()
        