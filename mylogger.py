import boto3
import time

defaultLogGroup = 'databricks-etl/notebooks/customlogs'
defaultLogStream = 'Notebook-logging-'

class cwlog:
    '''Represents a logger object that keeps track of cloudwatch logging variables'''
    
    def __init__(self, logStreamName=None, logGroup=None):
        '''Initializes the logger object
        
        The logStreamName is the name given to this instance of the logger
        The logGroup is the group of logs to put this instance in
        '''
        
        self.cwl =  boto3.client('logs',region_name='us-east-1')
        
        if logGroup is None:
            logGroup = defaultLogGroup
        
        #Check if the logGroup exists
        logGroups = self.cwl.describe_log_groups(logGroupNamePrefix=logGroup)
        
        if not logGroups['logGroups']:
            #No logGroups match, need to create it
            self.cwl.create_log_group(logGroupName=logGroup)
        
        self.logGroup = logGroup
        #Set a stream name if none given.
        if logStreamName is None:
            logStreamName = defaultLogStream + str(int(time.time()*1000))
        
        self.logStreamName = logStreamName
        #Create the log stream for all logs in this log instance
        self.cwl.create_log_stream(logGroupName=logGroup, logStreamName=logStreamName)
        
        #Start of log
        rsp = self.cwl.put_log_events(
               logGroupName=self.logGroup,
               logStreamName=self.logStreamName,
               logEvents=[{
                   'timestamp': int(time.time()*1000),
                   'message': 'Log started for ' + logStreamName
                    },
               ])
        
        #Track the next Log token
        self.nextSequenceToken = rsp['nextSequenceToken']
        
        #Record the response to the object if it's needed
        self.response = rsp

    def log(self, dataToLog):
        '''Add something to the existing log'''
        
        rsp = self.cwl.put_log_events(
               logGroupName=self.logGroup,
               logStreamName=self.logStreamName,
               logEvents=[{
                   'timestamp': int(time.time()*1000),
                   'message': dataToLog
                    },
               ],
               sequenceToken = self.nextSequenceToken)
        
        #update the Sequence token
        self.nextSequenceToken = rsp['nextSequenceToken']
        
        rsp['logged-value'] = dataToLog

        print(dataToLog)
        
        #Record the response in case the caller needs it
        self.response = rsp

