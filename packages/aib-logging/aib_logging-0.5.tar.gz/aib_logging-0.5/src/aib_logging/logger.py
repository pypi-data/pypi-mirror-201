class aib_logger:
    from enum import Enum
    
    class Categories(Enum):
        MODEL="Model"
        DATA="Data"
        METRIC="Metric"
        OTHER="Other"

    class Actions(Enum):
        CREATE="Create"
        UPDATE="Update"
        DELETE="Delete"
        UPLOAD="Upload"
        MODEL_SCORE="Model_Score"
        DATA_STAT="Data_statistics"
        OTHER="Other"
    
    class Severities(Enum):
        INFO="INFO"
        WARNING="WARNING"
        ERROR="ERROR"

    def __init__(self, project:str, pipeline_name:str="", logger_name:str="aib_custom_logger"):
        import logging
        import google.cloud.logging
        self.project=project
        self.pipeline_name=pipeline_name
        client = google.cloud.logging.Client(project=project)
        self.logger = client.logger(name=logger_name)
    
    def score_log(
        self,
        msg:str,
        category:Categories=Categories.MODEL,
        action:Actions=Actions.MODEL_SCORE,
        severity:Severities=Severities.INFO,
        model_name:str="AIB_Test",
        data_subset:str='training',
        model_type:str='regression',
        accuracy_score:float=0.00,
        confusion_metric:list=[[0.0,0.0],[0.0,0.0]],
        precision:float=0.00,
        recall:float=0.00,
        f1_score:float=0.00,
        roc_auc_score:float=0.00,
        precision_recall_auc:float=0.00,
        log_loss:float=0.00,
        zero_one_loss_normal:float=0.00,
        zero_one_loss_fraction:float=0.00,
        balanced_accuracy_score_normal:float=0.00,
        balanced_accuracy_score_adjusted:float=0.00,
        brier_score_loss:float=0.00,
        brier_score_loss_0_positive:float=0.00,
        fbeta_precision:float=0.00,
        fbeta_score_recall:float=0.00,
        hamming_loss:float=0.00,
        r2_score:float=0.00,
        mean_absolute_error:float=0.00,
        mean_squared_error:float=0.00, 
        mean_squared_log_error:float=0.00,
        median_absolute_error:float=0.00,
        explained_variance_score:float=0.00,
        residual_error:float=0.00,
        adjusted_rand_score:float=0.00,
        extra_labels:list=[],
        object:dict={},
        **kwargs
    ):
        import inspect
        
        if model_type == 'classification':
            payload={
                "pipeline_run_name":self.pipeline_name,
                "component_name": inspect.stack()[1].function,
                "project":self.project,
                "category":category.value,
                "action":action.value,
                "model_name":model_name,
                "data_subset":data_subset,
                "model_type":model_type,
                "accuracy_score":accuracy_score,
                "confusion_metric":confusion_metric,
                "precision":precision,
                "recall":recall,
                "f1-score":f1_score,
                "roc_auc_score":roc_auc_score,
                "precision_recall_auc":precision_recall_auc,
                "log_loss":log_loss,
                "zero_one_loss_normal":zero_one_loss_normal,
                "zero_one_loss_fraction":zero_one_loss_fraction,
                "balanced_accuracy_score_normal":balanced_accuracy_score_normal,
                "balanced_accuracy_score_adjusted":balanced_accuracy_score_adjusted,
                "brier_score_loss":brier_score_loss,
                "brier_score_loss_0_positive":brier_score_loss_0_positive,
                "fbeta_precision":fbeta_precision,
                "fbeta_score_recall":fbeta_score_recall,
                "hamming_loss":hamming_loss,
                "extra_labels":extra_labels,
                "message":msg,
                "object":object
            }
            for key, value in kwargs.items():
                payload[key]=value
        
        if model_type == 'regression':
            payload={
                "pipeline_run_name":self.pipeline_name,
                "component_name": inspect.stack()[1].function,
                "project":self.project,
                "category":category.value,
                "action":action.value,
                "model_name":model_name,
                "data_subset":data_subset,
                "model_type":model_type,
                "r2_score":r2_score,
                "mean_absolute_error":mean_absolute_error,
                "mean_squared_error":mean_squared_error,
                "mean_squared_log_error":mean_squared_log_error,
                "median_absolute_error":median_absolute_error,
                "explained_variance_score":explained_variance_score,
                "residual_error":residual_error,                
                "extra_labels":extra_labels,
                "message":msg,
                "object":object
            }
            for key, value in kwargs.items():
                payload[key]=value
        
        if model_type == 'clustering':
            payload={
                "pipeline_run_name":self.pipeline_name,
                "component_name": inspect.stack()[1].function,
                "project":self.project,
                "category":category.value,
                "action":action.value,
                "model_name":model_name,
                "data_subset":data_subset,
                "model_type":model_type,
                "accuracy_score":accuracy_score,
                "confusion_metric":confusion_metric,
                "adjusted_rand_score":adjusted_rand_score,
                "extra_labels":extra_labels,
                "message":msg,
                "object":object
            }
            for key, value in kwargs.items():
                payload[key]=value
                
        self.logger.log_struct(payload, severity=severity.value)

    def data_stat_log(
        self,
        msg:str,
        category:Categories=Categories.DATA,
        action:Actions=Actions.DATA_STAT,
        severity:Severities=Severities.INFO,
        extra_labels:list=[],
        object:dict={},
        **kwargs
           ):
        import inspect
        payload={
            "pipeline_run_name":self.pipeline_name,
            "component_name": inspect.stack()[1].function,
            "project":self.project,
            "category":category.value,
            "action":action.value,
            "extra_labels":extra_labels,
            "message":msg,
            "object":object
        }
        for key, value in kwargs.items():
                payload[key]=value
        # Send the Log request
        self.logger.log_struct(payload, severity=severity.value)
