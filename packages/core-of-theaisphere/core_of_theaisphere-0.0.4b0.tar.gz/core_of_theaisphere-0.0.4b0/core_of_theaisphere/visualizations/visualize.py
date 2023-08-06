"""
This script contains code for generating plots like roc-auc, precision, recall, confusion matrix, etc.
"""

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
from sklearn.metrics import roc_auc_score, roc_curve

"""
Author: vickyparmar
File: visualize.py
Created on: 07-10-2022, Fri, 1:51:58

Last modified by: vickyparmar
Last modified on: 10-3-2023, Fri, 14:50:41
"""


# Class ClassicMLPlots
class ClassicMLPlots:
    """
            A class for generating classic machine learning plots.

            Methods
            -------
            plot_confusion_matrix(y_true, y_pred, labels=None, title='Confusion matrix', cmap=None)
                Plot a confusion matrix for the given true and predicted labels.
            plot_roc_curve(y_true, y_score, title='ROC curve', **kwargs)
                Plot a ROC curve for the given true labels and predicted scores.
            plot_precision_recall_curve(y_true, y_score, title='Precision-Recall curve', **kwargs)
                Plot a precision-recall curve for the given true labels and predicted scores.

            """
    TAS_PALETTE = ['#04c99a', '#0fbaa6', '#17aab2', '#1d9bbe', '#4065e7', '#3c61ad',
                   '#280060']

    @staticmethod
    def plot_feature_importance(feature_df: pd.DataFrame, title: str, save_loc: str or Path,
                                top_n: int = None, important_only: bool = True, show: bool = False,
                                **kwargs: dict) -> None:
        """
            Plot feature importances from a pandas DataFrame.

            Parameters
            ----------
            feature_df : pandas.DataFrame
                The feature importances as a DataFrame. Must have columns named "feature" and "importance".
            title : str
                The title of the plot.
            save_loc : str or pathlib.Path
                The file path to save the plot.
            top_n : int, optional
                The number of top features to display. If None, display all features. Default is None.
            important_only : bool, optional
                Whether to exclude features with importance equal to zero. Default is True.
            show : bool, optional
                Whether to show the plot. Default is False.
            **kwargs : dict, optional
                Additional keyword arguments for customizing the plot, including:
                - fontdict : dict, optional
                    The font properties for the title, x-label, and y-label. Default is {'family': 'Trebuchet MS',
                    'color': '#280060', 'weight': 'normal', 'size': 16}.
                - font_scale : float, optional
                    The scaling factor for the font size. Default is 1.0.
                - figsize : tuple, optional
                    The size of the figure in inches. Default is (18, 9).
                - dpi : int, optional
                    The resolution of the figure in dots per inch. Default is 300.
                - orient : {'h', 'v'}, optional
                    The orientation of the plot. 'h' for horizontal bar chart and 'v' for vertical bar chart.
                    Default is 'h'.

            Returns
            -------
            None

            Raises
            ------
            ValueError
                If feature_df is not a pandas DataFrame or does not have columns named "feature" and "importance".

            Examples
            --------
            >>> df = pd.DataFrame({'feature': ['f1', 'f2', 'f3'], 'importance': [0.2, 0.3, 0.5]})
            >>> ClassicMLPlots.plot_feature_importance(df, 'Feature Importances', 'feature_importances.png')
            """
        if top_n is not None:
            feature_df = feature_df.nlargest(top_n, columns='importance')
        feature_df.sort_values(by='importance', inplace=True, ascending=False)
        if important_only:
            feature_df = feature_df[feature_df.importance != 0]

        # Figure parameters
        fontdict = kwargs['fontdict'] if 'fontdict' in kwargs else {'family': 'Trebuchet MS',
                                                                    'color': '#280060',
                                                                    'weight': 'normal',
                                                                    'size': 16,
                                                                    }
        font_scale = kwargs['font_scale'] if 'font_scale' in kwargs else 1.0
        figsize = kwargs['figsize'] if 'figsize' in kwargs else (18, 9)
        dpi = kwargs['dpi'] if 'dpi' in kwargs else 300
        orient = kwargs['orient'] if 'orient' in kwargs else 'h'

        # Plotting
        sns.set(font_scale=font_scale)
        fig = plt.figure(figsize=figsize, dpi=dpi)
        if orient == 'v':
            sns.barplot(data=feature_df, y='importance', x='feature', orient=orient,
                        palette=ClassicMLPlots.TAS_PALETTE)
            x_label = 'Feature'
            y_label = 'Importance'
        else:
            sns.barplot(data=feature_df, x='importance', y='feature', orient=orient,
                        palette=ClassicMLPlots.TAS_PALETTE)
            x_label = 'Importance'
            y_label = 'Feature'
        plt.grid(False)
        plt.xlabel(x_label, fontdict=fontdict)
        plt.ylabel(y_label, fontdict=fontdict)
        plt.title(title, pad=10, fontdict=fontdict)
        plt.tight_layout()
        sns.despine(right=True, top=True)

        # Saving the plot
        Path(save_loc).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(save_loc, dpi=dpi)
        if show:
            plt.show()
        plt.close(fig)

    @staticmethod
    def plot_confusion_matrix(confusion_matrix: np.ndarray, title: str, save_loc: str or Path,
                              show: bool = False, **kwargs: dict) -> None:
        """
            Plot a confusion matrix.

            Parameters
            ----------
            confusion_matrix : numpy.ndarray
                A confusion matrix in the form of a 2D numpy array.
            title : str
                The title of the plot.
            save_loc : str or pathlib.Path
                The path to save the plot.
            show : bool, optional
                Whether to display the plot, by default False.
            **kwargs : dict
                Additional keyword arguments to pass to the function.

            Keyword Args
            ------------
            fontdict : dict, optional
                Dictionary of font properties, by default {'family': 'Trebuchet MS', 'color': '#280060',
                'weight': 'normal', 'size': 12}.
            font_scale : float, optional
                Scaling factor for font size, by default 1.0.
            figsize : tuple, optional
                Figure size in inches, by default (8, 8).
            dpi : int, optional
                Dots per inch (resolution), by default 300.
            tick_labels : list, optional
                List of tick labels for x and y axes, by default None.

            Returns
            -------
            None
                The function saves the plot at the specified location.

            Raises
            ------
            ValueError
                If the length of confusion_matrix is less than 2.

            Examples
            --------
            >>> cm = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
            >>> ClassicMLPlots.plot_confusion_matrix(cm, "Confusion Matrix", "confusion_matrix.png", True)
            """
        # Figure parameters
        fontdict = kwargs['fontdict'] if 'fontdict' in kwargs else {'family': 'Trebuchet MS',
                                                                    'color': '#280060',
                                                                    'weight': 'normal',
                                                                    'size': 12,
                                                                    }
        font_scale = kwargs['font_scale'] if 'font_scale' in kwargs else 1.0
        figsize = kwargs['figsize'] if 'figsize' in kwargs else (8, 8)
        dpi = kwargs['dpi'] if 'dpi' in kwargs else 300

        # Plotting
        sns.set(font_scale=font_scale)
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = sns.heatmap(confusion_matrix, annot=True, cmap=ClassicMLPlots.TAS_PALETTE,
                         cbar=False)
        ax.set_title(title, pad=10, fontdict=fontdict)
        ax.set_xlabel('Predicted', fontdict=fontdict)
        ax.set_ylabel('Actual', fontdict=fontdict)
        if len(confusion_matrix) == 2:
            tick_labels = ['False', 'True']
        elif 'tick_labels' in kwargs:
            tick_labels = kwargs['tick_labels']
        else:
            tick_labels = [f"class_{i}" for i in range(len(confusion_matrix))]
        ax.xaxis.set_ticklabels(tick_labels)
        ax.yaxis.set_ticklabels(tick_labels)
        plt.grid(False)
        plt.tight_layout()

        # Saving the plot
        Path(save_loc).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(save_loc, dpi=dpi)
        if show:
            plt.show()
        plt.close(fig)

    @staticmethod
    def plot_roc_auc(ground_truth: np.ndarray or pd.Series or pd.DataFrame,
                     probabilities: np.ndarray or pd.Series or pd.DataFrame,
                     title: str, save_loc: str or Path,
                     show: bool = False, **kwargs: dict) -> None:
        """
            Plot the Receiver Operating Characteristic (ROC) curve and calculate the Area Under the Curve (AUC).

            Parameters
            ----------
            ground_truth : numpy.ndarray or pandas.Series or pandas.DataFrame
                Ground truth (correct) target values.
            probabilities : numpy.ndarray or pandas.Series or pandas.DataFrame
                Estimated probabilities of the positive class.
            title : str
                Title of the plot.
            save_loc : str or pathlib.Path
                Location to save the plot.
            show : bool, optional
                Whether to display the plot or not. Default is False.
            **kwargs : dict
                Additional keyword arguments to customize the plot. The following parameters are available:
                    - fontdict : dict, optional
                        Font properties for the title, xlabel and ylabel. Default is {'family': 'Trebuchet MS',
                        'color': '#280060', 'weight': 'normal', 'size': 12}.
                    - font_scale : float, optional
                        Scaling factor for the font size. Default is 1.0.
                    - figsize : tuple, optional
                        Figure size in inches. Default is (8, 8).
                    - dpi : int, optional
                        Dots per inch (resolution). Default is 300.
                    - label : str, optional
                        Label for the ROC curve. Default is 'AUC: {round(auc, 2)}'.

            Returns
            -------
            None

            Notes
            -----
            This function uses the `roc_curve` and `roc_auc_score` functions from the `sklearn.metrics` module,
            and the `seaborn` and `matplotlib.pyplot` plotting libraries.

            Examples
            --------
            >>> from sklearn.datasets import make_classification
            >>> X, y = make_classification(random_state=42)
            >>> ClassicMLPlots.plot_roc_auc(y, np.random.rand(len(y)), 'ROC Curve', Path('roc_curve.png'), True)
            """
        fpr, tpr, _ = roc_curve(ground_truth, probabilities)
        auc = roc_auc_score(ground_truth, probabilities)
        # Figure parameters
        fontdict = kwargs['fontdict'] if 'fontdict' in kwargs else {'family': 'Trebuchet MS',
                                                                    'color': '#280060',
                                                                    'weight': 'normal',
                                                                    'size': 12,
                                                                    }
        font_scale = kwargs['font_scale'] if 'font_scale' in kwargs else 1.0
        figsize = kwargs['figsize'] if 'figsize' in kwargs else (8, 8)
        dpi = kwargs['dpi'] if 'dpi' in kwargs else 300

        # Plotting
        sns.set(font_scale=font_scale)
        plt.rcParams['axes.facecolor'] = 'white'
        fig = plt.figure(figsize=figsize, dpi=dpi)
        label = kwargs['label'] if 'label' in kwargs else f"AUC: {round(auc, 2)}"
        plt.plot(fpr, tpr, color=ClassicMLPlots.TAS_PALETTE[-1], label=label)
        plt.plot([0, 1], [0, 1], color=ClassicMLPlots.TAS_PALETTE[0], lw=2,
                 linestyle='--', label='Chance-AUC: 0.5')
        plt.title(title, pad=10, fontdict=fontdict)
        plt.xlabel('False Positive Rate', fontdict=fontdict)
        plt.ylabel('True Positive Rate', fontdict=fontdict)
        plt.legend(labelcolor=ClassicMLPlots.TAS_PALETTE[-1])
        plt.grid(False)
        plt.tight_layout()

        # Saving the plot
        Path(save_loc).parent.mkdir(exist_ok=True, parents=True)
        fig.savefig(save_loc, dpi=dpi)
        if show:
            plt.show()
        plt.close(fig)
