import numpy as np
import pandas as pd
#MODELS
#CLASSIFICATION
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
#REGRESSION
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor



#PREPROCESSING
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
#OPTIMIZERS
from sklearn.model_selection import GridSearchCV
from .bayes import ModelOptimizer
from sklearn.model_selection import RandomizedSearchCV
#INFO
from .models_info import *
#import compute_sample_weight
from sklearn.utils.class_weight import compute_sample_weight



#---------------------------------------------------------------------------

def automatic_preprocessor(X_train,ordinal_cat_cols):
    #Arguments assertion not needed because they are already checked in the model method of the classes that are the ones that call this function
    """
    This function performs a preprocessor for the data. It automatically detects the categorical and numeric variables and performs the following steps:
        - Numeric variables: imputation by scaling. STANDARD SCALER
        - Categorical variables: imputation by encoding. ONE HOT ENCODER
        - Ordinal categorical variables: imputation by encoding. ORDINAL ENCODER

    Parameters
    ----------
    X_train : pandas dataframe
        Training data.
    ordinal_cat_cols : list, optional
        List of categorical variables that are ordinal.

    Returns
    -------
    preprocessor : sklearn preprocessor
        Preprocessor for the data. Used fo the pipelines for every model.

    """
    num_cols = X_train.select_dtypes(include=np.number).columns.values.tolist() #Detects the numeric variables
    cat_cols = X_train.select_dtypes(include=['category']).columns.values.tolist() #detects the categorical variables

    if ordinal_cat_cols is None:
        cat_cols_onehot = cat_cols
        ordinal_cat_cols = []
    else:
        for col in ordinal_cat_cols:
            cat_cols.remove(col)
        cat_cols_onehot = cat_cols

    # Prepare the categorical variables by encoding the categories    
    categorical_transformer_onehot = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))])
    categorical_transformer_ordinal = Pipeline(steps=[('ordinal', OrdinalEncoder())])
    # Prepare the numeric variables by imputing by scaling
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, num_cols), #numeric variables
        ('cat_onehot', categorical_transformer_onehot, cat_cols_onehot), #categorical variables
        ('cat_ordinal', categorical_transformer_ordinal, ordinal_cat_cols)]) #ordinal categorical variables
    return preprocessor


def train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,random_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=None,cv=10,random_n_iter=10, X_prev=None, columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):

    #Arguments assertion not needed because they are already checked in the model method of the classes that are the ones that call this function
    """
    This function performs a grid search or a bayesian search for the hyperparameters of the model. It is used in the for the deployment 
    of the model in ecah model method of the model classes.

    Parameters
    ----------
    X_train : pandas
        Training data.
    y_train : pandas
        Training labels.
    bayes_pbounds : dict, optional
        Dictionary with the bounds for the bayesian search. The default is None.
    grid_params : dict, optional
        Dictionary with the grid search parameters. The default is None.
    random_params : dict, optional
        Dictionary with the random search parameters. The default is None.
    n_jobs : int, optional
        Number of jobs for the grid search. The default is -1.
    pipe : sklearn pipeline
        Pipeline for the model.
    scoring : str
        Scoring metric for the grid search.
    bayes_int_params : list, optional
        List of parameters that are integers. The default is None.
    bayes_n_iter : int, optional
        Number of iterations for the bayesian search. The default is 10.
    sample_weight : pandas, optional
        Sample weights for the grid search. The default is None.
    cv : int, optional
        Number of folds for the grid search. The default is 10.
        For time series use TimeSeriesSplit or BlockTimeSeriesSplit
    random_n_iter : int, optional
        Number of iterations for the random search. The default is 10.
    """
    #For Grid Search optimizartion,its done when the bayes_pbounds and random_params are None
    if bayes_pbounds is None and random_params is None : 
        print("Grid search is running")
    #apply the grid search
        model_ = GridSearchCV(
            estimator = pipe, 
            param_grid = grid_params, 
            cv = cv, 
            n_jobs = n_jobs, 
            scoring = scoring,
            verbose=2
        )
    #For Bayesian Search optimization, its done when the bayes_pbounds is not None and random_params is None
    elif bayes_pbounds is not None and random_params is None: 
        print("Bayesian search is running")
        optimizer = ModelOptimizer(scoring=scoring,cv=cv)
        params_bayes = optimizer.optimize_model(pbounds=bayes_pbounds, X_train_scale=X_train, 
                                    y_train=y_train, model=pipe, 
                                    int_params=bayes_int_params,n_iter=bayes_n_iter)
        hyper_params = { (k):(int(np.round(v, 0)) if k in bayes_int_params else round(v, 2)) for k, v in params_bayes.items()}
        model_ = pipe.set_params(**hyper_params)
    #For Random Search optimization, its done when the bayes_pbounds is None and random_params is not None
    else: 
        print("Random search is running")
        model_ = RandomizedSearchCV(
            estimator = pipe, 
            param_distributions = random_params, 
            cv = cv, 
            n_jobs = n_jobs, 
            scoring = scoring,
            verbose=2,
            return_train_score=True,
            n_iter=random_n_iter
        )

    if sample_weight is not None : #Sample weight are for XGBoost ando some other models but not fo all
        if sample_weight=='balanced' : #If the sample weight is balanced
            sample_weights = compute_sample_weight(
            class_weight='balanced',
            y=y_train)
        else:
            sample_weights=sample_weight
        if pipe.steps[-1][0]=='XGB':
            model_.fit(X_train, y_train, XGB__sample_weight=sample_weights, X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
        elif pipe.steps[-1][0]=='LGBM':
            model_.fit(X_train, y_train, LGBM__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
        elif pipe.steps[-1][0]=='RF':
            model_.fit(X_train, y_train, RF__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
        elif pipe.steps[-1][0] == 'KNN':
            model_.fit(X_train, y_train, KNN__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
        elif pipe.steps[-1][0] == 'LR':
            model_.fit(X_train, y_train, LR__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
        elif pipe.steps[-1][0] == 'MLP':
            model_.fit(X_train, y_train, MLP__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
        elif pipe.steps[-1][0] == 'DT':
            model_.fit(X_train, y_train, DT__sample_weight=sample_weights, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
    else :
        model_.fit(X_train, y_train, X_prev = X_prev, columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)
    return model_


class Classification:
    """
    This class contains all the classification models. Consideres relevant.
    Its up to suggestions for other models to be added.
    """
    #Global Attributes
    RandomForest_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    XGBoost_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    LogisticRegression_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    DecisionTree_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    KNN_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    MLP_Classifier_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"

    def __init__(self):
        pass

    def RandomForest_Classifier(self, X_train, y_train, ordinal_cat_cols=None,
                                scoring='accuracy', class_weight=None,
                                grid_params={'RFC__n_estimators': [100, 200],
                                            'RFC__max_depth': [None, 10, 20],
                                            'RFC__min_samples_split': [2, 5],
                                            'RFC__max_features': ['sqrt', None]},
                                cv=10,
                                random_params=None,
                                random_n_iter=10,
                                bayes_pbounds=None,
                                bayes_int_params=None, 
                                bayes_n_iter=30,
                                criterion='gini',
                                sample_weight=None,
                                random_state=None,
                                n_jobs=-1):
        """
        This function performs a Random Forest classification model with grid search or bayesian optimization.


        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        
        y_train : pandas dataframe
            Training labels.
        
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal. The default is None.
        
        scoring : str, optional
            Scoring function for model evaluation. The default is 'accuracy'.
        
        balanced : str, optional
            If 'balanced', class weights are balanced. The default is None.

        grid_param_grid : dict, optional
            Dictionary of parameters for grid search. The default is {'RFC__n_estimators': [100, 200], 'RFC__max_depth': [None, 10, 20],
                                                    'RFC__min_samples_split': [2, 5], 'RFC__max_features': ['sqrt', None]}.             
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        criterion : str, optional
            Criterion for splitting. The default is 'gini'.
        
        random_state : int, optional
            Random state. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        Returns
        -------
        model : sklearn model
            Trained model with grid seach
        """
        print(" INFO: Agurments params must start as 'RF__param'" + '\n' "INFO: Default params in Documentation for Random Forest are: ", rf_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'criterion = {criterion}',
            f'bayes_n_iter = {bayes_n_iter}', f'class_weigth = {class_weight}', f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}',
            f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert class_weight is None or class_weight is 'balanced' , "In case of balanced class weights, balanced must be 'balanced'"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameters"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #RFC should be in every key of grid_param_grid
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert all('RF__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'RF__'"
        elif random_params is not None:
            assert all('RF__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'RF__'"
        elif bayes_pbounds is not None:
            assert all('RF__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'RF__'"
            assert all('RF__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'RF__'"
        # Inputs of the model. Change accordingly to perform variable selection
    
        preprocessor = automatic_preprocessor(X_train, ordinal_cat_cols)
        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('RF', RandomForestClassifier(
                criterion = criterion,
                bootstrap = True,
                n_jobs = n_jobs,
                random_state = random_state,
                class_weight = class_weight))])

        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,random_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=sample_weight,cv=cv,random_n_iter=random_n_iter)

        return model_
    
    def XGBoost_Classifier( self, X_train, y_train, ordinal_cat_cols=None,
                            scoring='accuracy', eval_metric='merror',
                            objective='multi:softmax', grid_params={},
                            cv=10, random_params=None, random_n_iter=10,
                            bayes_pbounds=None,bayes_int_params=None, 
                            bayes_n_iter=30, random_state=None,
                            sample_weight=None, n_jobs=-1):  
        """
        This method performs a XGBoost classification model with grid search or bayesian optimization.


        Parameters
        ----------
        X_train : pandas dataframe
            Training data.
        
        y_train : pandas dataframe
            Training labels.
        
        ordinal_cat_cols : list, optional
            List of categorical variables that are ordinal. The default is None.
        
        scoring : str, optional
            Scoring function for model evaluation. The default is 'accuracy'.
        
        eval_metric : str, optional
            Evaluation metric. The default is 'merror'.
        
        objective : str, optional
            Objective function. The default is 'multi:softmax'.

        grid_param_grid : dict, optional
            Dictionary of parameters for grid search. 
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.

        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.

        sample_weight : str, optional
            If 'balanced', class weights are balanced. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        Returns
        -------
        model : sklearn model
            Trained model with grid seach or bayesian optimization

        """
        print(" INFO: Agurments params must start as 'XGB__param'" + '\n' "INFO: Default params for XGBoost in Documentation are: ", xgb_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'eval_metric = {eval_metric}',f'objective = {objective}',
            f'bayes_n_iter = {bayes_n_iter}', f'sample_weigth = {sample_weight}', f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}',
            f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert sample_weight is None or sample_weight is 'balanced' or isinstance(sample_weight, compute_sample_weight) , "In case of balanced class weights, balanced must be 'balanced'"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameters"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #XGB__ is the prefix for every hyperparameter of this model
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert all('XGB__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'XGB__'"
        elif random_params is not None:
            assert all('XGB__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'XGB__'"
        elif bayes_pbounds is not None:
            assert all('XGB__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'XGB__'"
            assert all('XGB__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'XGB__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)

        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('XGB', XGBClassifier(
                                random_state=random_state,
                                n_jobs=n_jobs, 
                                verbosity=0,
                                eval_metric=eval_metric,
                                objective=objective))])
                                
        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,random_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=sample_weight,cv=cv,random_n_iter=random_n_iter)
        return model_
    
    def LogisticRegression_Classifier(self, X_train, y_train,  
                                      ordinal_cat_cols=None, scoring='accuracy',
                                    grid_params = {'LR__C': [0.1, 1, 10],
                                    'LR__penalty': ['l1', 'l2', 'elasticnet'],
                                    'LR__multi_class': ['ovr', 'multinomial'],   
                                    'LR__solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']},
                                    cv=10, random_params=None, random_n_iter=10,
                                    bayes_pbounds=None, bayes_int_params=None, 
                                    bayes_n_iter=30, random_state=None, class_weight=None, sample_weight=None,
                                    n_jobs=-1 , tol=0.0001, max_iter=1000):
        """
        This method performs a Logistic Regression classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.
        
        y_train : pandas dataframe
            Training set labels.
        
        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.
        
        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.
        
        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is 
            {'LR__C': [0.1, 1, 10], 'LR__penalty': ['l1', 'l2', 'elasticnet'],
            'LR__multi_class': ['ovr', 'multinomial'], 'LR__solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}.

        cv : int, optional
            Number of folds for cross validation. The default is 10.

        random_params : dict, optional
            Dictionary of parameters for random search. The default is None.

        random_n_iter : int, optional   
            Number of iterations for random search. The default is 10.
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.
        
        class_weight : str, optional
            If 'balanced', class weights will balanced. The default is None.

        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        tol : float, optional
            Tolerance for stopping criteria. The default is 0.0001.
        
        max_iter : int, optional
            Maximum number of iterations. The default is 1000.
        
        Returns
        -------
        model_ : trained model
            Trained model with grid seach or bayesian optimization

        """

        print(" INFO: Agurments params must start as 'LR__param'" + '\n' "INFO: Default params in Documentaction for Logistic Regression are: ", lr_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'bayes_n_iter = {bayes_n_iter}',
            f'class_weigth = {class_weight}', f'max_iter = {max_iter}' f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}',
            f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert class_weight is None or class_weight is 'balanced' , "In case of balanced class weights, balanced must be 'balanced'"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        #LR__ is the prefix for every hyperparameter in this model
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert all('LR__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'LR__'"
        elif random_params is not None:
            assert all('LR__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'LR__'"
        elif bayes_pbounds is not None:
            assert all('LR__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'LR__'"
            assert all('LR__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LR__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)

        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('LR', LogisticRegression(
                                    max_iter=max_iter,
                                    tol=tol, #default 1e-4
                                    class_weight=class_weight, #is used to handle the imbalance dataset
                                    random_state=random_state,
                                    n_jobs=n_jobs, 
                                    verbose=0,
                                    warm_start=False,
                                    fit_intercept=True,
                                    intercept_scaling=1,
                                    dual=False))])

        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,random_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,cv=cv,random_n_iter=random_n_iter,sample_weight=sample_weight)
        
        return model_
    
    def MLP_Classifier(self,X_train,y_train,ordinal_cat_cols=None, scoring='accuracy',
                       grid_params={'MLP__alpha': [1e-9,1e-7,1e-5,0.001,0.01],
                        'MLP__hidden_layer_sizes':[(5,),(10,),(15,),(20,),(25,)]},
                        cv=10, random_params=None, random_n_iter=10,
                        bayes_pbounds=None, bayes_int_params=None, bayes_n_iter=30, 
                        random_state=None, n_jobs=-1, solver='lbfgs',
                        activation='logistic', tol=1e-4, max_iter=450, early_stopping=False,
                       learning_rate='constant',learning_rate_init=0.001,verbose=True, sample_weight=None):
        
        """
        This method performs a Multi Layer Perceptron classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.
        
        y_train : pandas dataframe
            Training set labels.
        
        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.
        
        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.
        
        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is
            {'MLP__alpha': [1e-9,1e-7,1e-5,0.001,0.01],
            'MLP__hidden_layer_sizes':[(5,),(10,),(15,),(20,),(25,)]}.

        cv : int, optional
            Number of folds for cross validation. The default is 10.
        
        random_params : dict, optional
            Dictionary of parameters for random search. The default is None.
        
        random_n_iter : int, optional
            Number of iterations for random search. The default is 10.
        
        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.
        
        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.
        
        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        solver : str, optional
            The solver for weight optimization. The default is 'lbfgs'.
        
        activation : str, optional
            Activation function for the hidden layer. The default is 'logistic'.
        
        tol : float, optional
            Tolerance for stopping criteria. The default is 1e-4.
        
        max_iter : int, optional
            Maximum number of iterations. The default is 450.

        early_stopping : bool, optional
            Whether to use early stopping to terminate training when validation score is not improving. The default is False.

        learning_rate : str, optional
            Learning rate schedule for weight updates. The default is 'constant'.
        
        learning_rate_init : float, optional
            The initial learning rate used. The default is 0.001.
        
        verbose : bool, optional
            Whether to print progress messages to stdout. The default is True.
        
        Returns
        -------
        model_ : sklearn model
            Trained model.

        """

        print(" INFO: Agurments params must start as 'MLP__param'" + '\n' "INFO: Default params in Documentation for MultiLayer Perceptron are: ", mlp_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'solver = {solver}',f'activation = {activation}',
        f'bayes_n_iter = {bayes_n_iter}', f'tol = {tol}', f'max_iter = {max_iter}' , f'learning_rate = {learning_rate}', f'learning_rate_init = {learning_rate_init}',
        f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}',
        f'random_state = {random_state}', f'n_jobs = {n_jobs}', f'early_stopping = {early_stopping}', f'verbose = {verbose}')
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_params must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #MLP__ is the prefix for every hyperparameter in MLPClassifier
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert all('MLP__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'MLP__'"
        elif random_params is not None:
            assert all('MLP__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'MLP__'"
        elif bayes_pbounds is not None:
            assert all('MLP__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'MLP__'"
            assert all('MLP__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'MLP__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor), 
                            ('MLP', MLPClassifier(solver=solver, # Update function
                                                    activation=activation, # Logistic sigmoid activation function
                                                    max_iter=max_iter, # Maximum number of iterations
                                                    tol=tol, # Tolerance for the optimization
                                                    random_state=random_state,
                                                    verbose = verbose,
                                                    early_stopping=early_stopping,
                                                    learning_rate=learning_rate,
                                                    learning_rate_init=learning_rate_init
                                                    ))]) # For replication


        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,random_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=sample_weight,cv=cv,random_n_iter=random_n_iter)
        return model_
        


    #do the same for knn_classifier
    def KNN_Classifier(self,X_train,y_train,ordinal_cat_cols=None, scoring='accuracy',
                        grid_params={'KNN__n_neighbors': [3,10,25,60]},
                        cv=10, random_params=None, random_n_iter=10,  bayes_pbounds=None,
                        bayes_int_params=None, bayes_n_iter=30, sample_weight=None,
                        random_state=None, n_jobs=-1):
          
        """
        This method performs a K-Nearest Neighbors classification model with grid search or bayesian optimization.

        Parameters
        ----------
        X_train : pandas dataframe
            Training set.

        y_train : pandas dataframe
            Training set labels.

        ordinal_cat_cols : list, optional
            List of ordinal categorical variables. The default is None.

        scoring : str, optional
            Evaluation metric. The default is 'accuracy'.

        grid_params : dict, optional
            Dictionary of parameters for grid search. The default is
            {'KNN__n_neighbors': [3,10,25,60]}.
        
        cv : int, optional
            Number of folds for cross validation. The default is 10.
        
        random_params : dict, optional
            Dictionary of parameters for random search. The default is None.

        random_n_iter : int, optional
            Number of iterations for random search. The default is 10.

        bayes_pbounds : dict, optional
            Dictionary of parameters for bayesian optimization. The default is None.
        
        bayes_int_params : list, optional
            List of parameters for bayesian optimization that are integers. The default is None.

        bayes_n_iter : int, optional
            Number of iterations for bayesian optimization. The default is 30.
        
        random_state : int, optional
            Random state. The default is None.

        n_jobs : int, optional
            Number of jobs. The default is -1.
        
        p : int, optional
            Power parameter for the Minkowski metric. The default is 2.
        
        metric : str, optional
            The distance metric to use for the tree. The default is 'minkowski'.
        
        Returns
        -------
        model_ : sklearn model
            Trained model.

        """

        print(" INFO: Agurments params must start as 'KNN__param'" + '\n' "INFO: Default params in Documentation for Random Forest are: ", knn_default_params_clf)
        print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'bayes_n_iter = {bayes_n_iter}',
               f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
        assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
        assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter values"
        assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter values"
        assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
        assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
        assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
        #KNN_ is the prefix for every hyperparameter in the KNN model
        if grid_params is not None and random_params is None and bayes_pbounds is None:
            assert all('KNN__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'KNN__'"
        elif random_params is not None:
            assert all('KNN__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'KNN__'"
        elif bayes_pbounds is not None:
            assert all('KNN__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'KNN__'"
            assert all('KNN__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'KNN__'"

        preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
        pipe = Pipeline(steps=[('Prep', preprocessor),
                            ('KNN', KNeighborsClassifier(n_jobs=n_jobs, random_state=random_state))])
        
        model_=train_bayes_or_grid_search(X_train,y_train,bayes_pbounds,grid_params,random_params,n_jobs,pipe,scoring,bayes_int_params,bayes_n_iter,sample_weight=sample_weight,cv=cv,random_n_iter=random_n_iter)

        return model_


    

    #do the same for a decision tree
    def DecisionTree_Classifier(self,X_train,y_train, ordinal_cat_cols=None, scoring='accuracy',
                            grid_params={'DT__max_depth': [3,5,7,10],
                                'DT__min_samples_split': [2,3,4],
                                'DT__min_samples_leaf': [4,5,6],
                                'DT__max_features': ['auto','sqrt','log2',None]},
                            cv=10, random_params=None, random_n_iter=10, bayes_pbounds=None, 
                            bayes_int_params=None, bayes_n_iter=30, class_weight=None, sample_weight=None, random_state=None, n_jobs=-1):
            
            """
            This method performs a Decision Tree classification model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'accuracy'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.

            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'DT__param'" + '\n' "INFO: Default params in Documentation for Decision Tree are: ", dt_default_params_clf)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'class_weigth = {class_weight}', f'bayes_pbounds = {bayes_pbounds}', 
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter values"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_param_grid must be a dictionary of parameter values"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #DT__ is the prefix for every hyperparameter in the Decision Tree model
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert all('DT__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'DT__'"
            elif random_params is not None:
                assert all('DT__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'DT__'"
            elif bayes_pbounds is not None:
                assert all('DT__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'DT__'"
                assert all('DT__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'DT__'"

            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('DT', DecisionTreeClassifier(random_state=random_state,class_weight=class_weight))])
            
            model_=train_bayes_or_grid_search(X_train, y_train, bayes_pbounds, grid_params, random_params,n_jobs, pipe, scoring, bayes_int_params, bayes_n_iter, sample_weight=sample_weight,cv=cv,random_n_iter=random_n_iter)

            return model_
    
#-------------------------------------------------------------------------------------------------------------------REGRESSION-------------------------------------------------------------------------------------------------------------#
class Regression:
    """
    This class contains all regression models that are considered relevant.
    Its up to add more models in the future thta could be suggested by the user.
    """

    RandomForest_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    XGBoost_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    LogisticRegression_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    DecisionTree_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    KNN_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"
    MLP_Regressor_Description = "Sustituir por desciprion que inlcuya los pros y contras del modelo guardado en models_info.py"

    def __init__(self):
        pass

    def RandomForest_Regressor(self, X_train, y_train, ordinal_cat_cols=None, scoring='neg_mean_squared_error', criterion="friedman_mse",
                            grid_params={'RF__n_estimators': [100, 200, 300, 400, 500],
                                'RF__max_depth': [3,5,7,10],
                                'RF__min_samples_split': [2,3,4],
                                'RF__min_samples_leaf': [4,5,6],
                                'RF__max_features': ['auto','sqrt','log2',None]}, 
                            cv=10, random_params=None, random_n_iter = 10, bayes_pbounds=None, 
                            bayes_int_params=None, bayes_n_iter = 30, sample_weight=None, random_state=None, n_jobs=-1,X_prev=None,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a Random Forest regression model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is

            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For Time Series, cv must be a TimeSeriesSplit object or BlockTimeSeriesSplit object.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """
            

            print(" INFO: Agurments params must start as 'RF__param'" + '\n' "INFO: Default params in Documentation for Random Forest are: ", rf_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}', 
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameters"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #RF__ is the prefix for every hyperparameter in the model
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert all('RF__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'RF__'"
            elif random_params is not None:
                assert all('RF__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'RF__'"
            elif bayes_pbounds is not None:
                assert all('RF__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'RF__'"
                assert all('RF__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'RF__'"

            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('RF', RandomForestRegressor(criterion=criterion,random_state=random_state,n_jobs=n_jobs))])
            
            model_=train_bayes_or_grid_search(X_train, y_train, bayes_pbounds, grid_params, random_params, n_jobs, pipe, scoring, bayes_int_params, bayes_n_iter, sample_weight=sample_weight,cv=cv,random_n_iter=random_n_iter, X_prev=X_prev
                                              ,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            return model_
    
    def XGB_Regressor(self, X_train, y_train, ordinal_cat_cols=None, scoring='neg_mean_squared_error',
                            grid_params={'XGB__n_estimators': [100, 200, 300, 400, 500],
                                'XGB__max_depth': [3,5,7,10],
                                'XGB__learning_rate': [0.01,0.05,0.1,0.15,0.2],
                                'XGB__min_child_weight': [1,3,5,7],
                                'XGB__gamma': [0.0,0.1,0.2,0.3,0.4],
                                'XGB__colsample_bytree': [0.3,0.4,0.5,0.7]}, 
                            cv=10, random_params=None, random_n_iter=10, bayes_pbounds=None, bayes_int_params=None,
                            bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1, X_prev=None,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a XGBoost regression model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For Time Series, cv must be a TimeSeriesSplit object or BlockTimeSeriesSplit object.
            
            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.

            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'XGB__param'" + '\n' "INFO: Default params in Documentation for XGBoost are: ", xgb_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # XGB__ is the prefix for every hyperparameters
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert all('XGB__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'XGB__'"
            elif random_params is not None:
                assert all('XGB__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'XGB__'"
            elif bayes_pbounds is not None:
                assert all('XGB__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'XGB__'"
                assert all('XGB__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'XGB__'"
            
            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('XGB', XGBRegressor(random_state=random_state,n_jobs=n_jobs))])
            
            model_=train_bayes_or_grid_search(X_train, y_train, bayes_pbounds, grid_params, random_params, n_jobs, pipe, scoring, bayes_int_params, bayes_n_iter, sample_weight=sample_weight,cv=cv,random_n_iter=random_n_iter, X_prev=X_prev,
                                              columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            return model_
    
    def Linear_Regression(self, X_train, y_train, ordinal_cat_cols=None, scoring='neg_mean_squared_error',
                            grid_params={'LR__fit_intercept': [True, False],
                                'LR__normalize': [True, False],
                                'LR__copy_X': [True, False]}, 
                            cv=10, random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1, X_prev=None,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a Linear Regression model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, use TimeSeriesSplit.

            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'LR__param'" + '\n' "INFO: Default params in Documentation for Linear Regression are: ", lr_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameters"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_param_grid must be a dictionary of parameters"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #LR is the prefix for every hyperparameter of the Linear Regression
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert all('LR__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'LR__'"
            elif random_params is not None:
                assert all('LR__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'LR__'"
            elif bayes_pbounds is not None:
                assert all('LR__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'LR__'"
                assert all('LR__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'LR__'"
            
            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('LR', LinearRegression())])
            
            model_=train_bayes_or_grid_search(X_train, y_train, bayes_pbounds, grid_params, random_params, n_jobs, pipe, scoring, bayes_int_params, bayes_n_iter, sample_weight=sample_weight, cv=cv, random_n_iter=random_n_iter,
                                              X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            return model_
    
    def KNN_Regressor(self, X_train, y_train, ordinal_cat_cols=None, scoring='neg_mean_squared_error',
                            grid_params={'KNN__n_neighbors': [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95,97,99],
                                'KNN__weights': ['uniform', 'distance'],
                                'KNN__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                                'KNN__leaf_size': [10,20,30,40,50,60,70,80,90,100],
                                'KNN__p': [1,2]}, 
                            cv=10, random_params=None, random_n_iter=10, bayes_pbounds=None, bayes_int_params=None,
                            bayes_n_iter=30, sample_weight=None ,random_state=None, n_jobs=-1, X_prev=None,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a KNN Regressor model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is
            
            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, use TimeSeriesSplit or BlockTimeSeriesSplit.
            
            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.
            
            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.

            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'KNN__param'" + '\n' "INFO: Default params in Documentation for KNN Regressor are: ", knn_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #KNN_ is the prefix for every hyperparameter in KNN
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert all('KNN__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'KNN__'"
            elif random_params is not None:
                assert all('KNN__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'KNN__'"
            elif bayes_pbounds is not None:
                assert all('KNN__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'KNN__'"
                assert all('KNN__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'KNN__'"

            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('KNN', KNeighborsRegressor())])
            
            model_=train_bayes_or_grid_search(X_train, y_train, bayes_pbounds, grid_params, random_params, n_jobs, pipe, scoring, bayes_int_params, bayes_n_iter, sample_weight=sample_weight, cv=cv, random_n_iter=random_n_iter,
                                              X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            return model_
    
    def DecisionTree_Regressor(self, X_train, y_train, ordinal_cat_cols=None, scoring='neg_mean_squared_error',
                            grid_params={'DT__criterion': ["squared_error", "friedman_mse", "absolute_error", "poisson"],
                                'DT__max_depth': [None,2,3,4,5],
                                'DT__min_samples_split': [2,3,4,],
                                'DT__max_features': ['auto', 'sqrt', 'log2'],
                                'DT__min_impurity_decrease': [0.0,0.1,0.2]}, 
                            cv=10, random_params=None, random_n_iter=10, bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None, random_state=None, n_jobs=-1, X_prev=None,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            
            """
            This method performs a Decision Tree Regressor model with grid search or bayesian optimization.
    
            Parameters
            ----------
            X_train : pandas dataframe
                Training set.
    
            y_train : pandas dataframe
                Training set labels.
    
            ordinal_cat_cols : list, optional
                List of ordinal categorical variables. The default is None.
    
            scoring : str, optional
                Evaluation metric. The default is 'neg_mean_squared_error'.
    
            grid_params : dict, optional
                Dictionary of parameters for grid search. The default is

            cv : int, optional
                Number of folds for cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object.
            
            random_params : dict, optional
                Dictionary of parameters for random search. The default is None.
            
            random_n_iter : int, optional
                Number of iterations for random search. The default is 10.
            
            bayes_pbounds : dict, optional
                Dictionary of parameters for bayesian optimization. The default is None.

            bayes_int_params : list, optional
                List of parameters for bayesian optimization that are integers. The default is None.
            
            bayes_n_iter : int, optional
                Number of iterations for bayesian optimization. The default is 30.
            
            random_state : int, optional
                Random state. The default is None.
            
            n_jobs : int, optional
                Number of jobs. The default is -1.
            
            Returns
            -------
            model_ : sklearn model
                Trained model.
            
            """

            print(" INFO: Agurments params must start as 'DT__param'" + '\n' "INFO: Default params in Documentation for Decision Tree Regressor are: ", dt_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}',
            f'bayes_n_iter = {bayes_n_iter}', f'bayes_pbounds = {bayes_pbounds}',
            f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}', f'n_jobs = {n_jobs}')
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            # DT__ is the prefix for every hyperparameter in the Decision Tree Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert all('DT__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'DT__'"
            elif random_params is not None:
                assert all('DT__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'DT__'"
            elif bayes_pbounds is not None:
                assert all('DT__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'DT__'"
                assert all('DT__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'DT__'"
            
            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor),
                                ('DT', DecisionTreeRegressor(random_state=random_state))])
            
            model_=train_bayes_or_grid_search(X_train, y_train, bayes_pbounds, grid_params, random_params, n_jobs, pipe, scoring, bayes_int_params, bayes_n_iter, sample_weight=sample_weight,cv=cv, random_n_iter=random_n_iter,
                                              X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            return model_
    
    def MLP_Regressor(self, X_train, y_train, ordinal_cat_cols=None, scoring='neg_mean_squared_error',
                            grid_params={'MLP__hidden_layer_sizes': [(3,),(5,)],
                                'MLP__activation': ['identity', 'logistic', 'tanh', 'relu'],
                                'MLP__solver': ['lbfgs', 'sgd', 'adam'],
                                'MLP__alpha': [0.0001,0.001,0.01,0.1,1,10,100],
                                'MLP__max_iter': [200]},
                            cv=10, random_params=None, random_n_iter=10,bayes_pbounds=None,
                            bayes_int_params=None, bayes_n_iter=30, sample_weight=None,random_state=None, n_jobs=-1, X_prev=None,
                            columns_lags=None, column_rolled_lags=None,lags=None,rolled_lags=None, rolled_metrics=None, column_rolled_lags_initial=None):
            """
            Trains a MLP Regressor model.

            Parameters
            ----------
            X_train : pandas dataframe
                Training data.
            
            y_train : pandas dataframe
                Training target.
            
            ordinal_cat_cols : list, optional
                List of ordinal categorical columns. The default is None.
            
            scoring : str, optional
                Scoring metric. The default is 'neg_mean_squared_error'.

            grid_params : dict, optional
                Grid search parameters. The default is {'MLP__hidden_layer_sizes': [(100,),(200,),(300,),(400,),(500,),(600,),(700,),(800,),(900,),(1000,)],
                'MLP__activation': ['identity', 'logistic', 'tanh', 'relu'],
                'MLP__solver': ['lbfgs', 'sgd', 'adam'],
                'MLP__alpha': [0.0001,0.001,0.01,0.1,1,10,100],
                'MLP__max_iter': [200,400,600,800,1000,1200,1400,1600,1800,2000],
            
            cv : int, optional
                Cross validation. The default is 10.
                For time series data, cv must be a TimeSeriesSplit object or 
                a BlockTimeSeriesSplit object.
            
            random_params : dict, optional
                Random search parameters. The default is None.
            
            random_n_iter : int, optional
                Random search number of iterations. The default is 10.

            bayes_pbounds : dict, optional
                Bayesian optimization parameters. The default is None.
            
            bayes_int_params : list, optional
                Bayesian optimization integer parameters. The default is None.

            bayes_n_iter : int, optional
                Bayesian optimization number of iterations. The default is 30.

            random_state : int, optional
                Random state. The default is None.

            n_jobs : int, optional
                Number of jobs. The default is -1.

            Returns
            -------
            None.

            """
            

            print(" INFO: Agurments params must start as 'MLP__param'" + '\n' "INFO: Default params in Documentation for MultiLayer Perceptron are: ", mlp_default_params_reg)
            print("\n"+ "INFO: Default params RUN for this model are: ", f'grid_params = {grid_params}',f'scoring = {scoring}', f'bayes_n_iter = {bayes_n_iter}' ,
            f'bayes_pbounds = {bayes_pbounds}', f'bayes_int_params = {bayes_int_params}', f'ordinal_cat_cols = {ordinal_cat_cols}', f'random_state = {random_state}',
            f'n_jobs = {n_jobs}')
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert ordinal_cat_cols is None or isinstance(ordinal_cat_cols, list), "In case of ordinal categorical variables, ordinal_cat_cols must be a list of column names"
            assert grid_params is None or isinstance(grid_params, dict), "In case of grid search, grid_param_grid must be a dictionary of parameter bounds"
            assert bayes_pbounds is None or isinstance(bayes_pbounds, dict), "In case of bayesian optimization, bayes_pbounds must be a dictionary of parameter bounds"
            assert random_params is None or isinstance(random_params, dict), "In case of random search, random_params must be a dictionary of parameter bounds"
            assert bayes_int_params is None or isinstance(bayes_int_params, list), "In case of bayesian optimization, bayes_int_params must be a list of parameter names"
            assert isinstance(bayes_n_iter,int), "In case of bayesian optimization, bayes_n_iter must be an integer"
            #MLP__ is the prefix for every hyperparameter in the MLP Regressor
            if grid_params is not None and random_params is None and bayes_pbounds is None:
                assert all('MLP__' in s for s in grid_params.keys()), "In case of grid search, grid_param_grid must start with 'MLP__'"
            elif random_params is not None:
                assert all('MLP__' in s for s in random_params.keys()), "In case of random search, random_params must start with 'MLP__'"
            elif bayes_pbounds is not None:
                assert all('MLP__' in s for s in bayes_pbounds.keys()), "In case of bayesian optimization, bayes_pbounds must start with 'MLP__'"
                assert all('MLP__' in s for s in bayes_int_params), "In case of bayesian optimization, bayes_int_params must start with 'MLP__'"

            
            preprocessor=automatic_preprocessor(X_train,ordinal_cat_cols)
            pipe = Pipeline(steps=[('Prep', preprocessor), 
                                      ('MLP', MLPRegressor(random_state=random_state))])
            

            model_=train_bayes_or_grid_search(X_train, y_train, bayes_pbounds, grid_params, random_params, n_jobs, pipe, scoring, bayes_int_params, bayes_n_iter, sample_weight=sample_weight,cv=cv, random_n_iter=random_n_iter,
                                              X_prev = X_prev,columns_lags=columns_lags, column_rolled_lags=column_rolled_lags,lags=lags,rolled_lags=rolled_lags, rolled_metrics=rolled_metrics, column_rolled_lags_initial=column_rolled_lags_initial)

            return model_
    
            

            

            
            
                                
    


        


    

    
