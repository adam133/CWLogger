import boto3
import time

defaultLogGroup = 'MyCustomLogs/Logs'
defaultLogStream = 'LogStream'
region = 'us-east-1'


class CWLog:
    """Represents a logger object that keeps track of cloudwatch logging variables"""

    def __init__(self, logStreamName=None, logGroup=None):
        """Initializes the logger object

        The logStreamName is the name given to this instance of the logger
        A timestamp will be appended in the format "logStreamName_9999999999"
        The logGroup is the cloudwatch group of logs to put this instance in
        """

        self.cwl = boto3.client('logs', region_name=region)

        if logGroup is None:
            logGroup = defaultLogGroup

        # Check if the logGroup exists
        logGroups = self.cwl.describe_log_groups(logGroupNamePrefix=logGroup)

        if not logGroups['logGroups']:
            # No logGroups match, need to create it
            self.cwl.create_log_group(logGroupName=logGroup)

        # Set the logGroup
        self.logGroup = logGroup
        # Set a stream name if none given.
        if logStreamName is None:
            logStreamName = defaultLogStream

        # Set the logStreamName
        self.logStreamName = logStreamName + '_' + str(int(time.time() * 1000))

        # Create the log stream for all logs in this log instance
        self.cwl.create_log_stream(logGroupName=self.logGroup, logStreamName=self.logStreamName)

        # Start of log
        rsp = self.cwl.put_log_events(
            logGroupName=self.logGroup,
            logStreamName=self.logStreamName,
            logEvents=[{
                'timestamp': int(time.time() * 1000),
                'message': 'Log started for ' + logStreamName
            },
            ])

        # Track the next Log token
        self.nextSequenceToken = rsp['nextSequenceToken']

        # Record the response to the object if it's needed
        self.response = rsp

    def log(self, dataToLog):
        """Add something to the existing log"""

        rsp = self.cwl.put_log_events(
            logGroupName=self.logGroup,
            logStreamName=self.logStreamName,
            logEvents=[{
                'timestamp': int(time.time() * 1000),
                'message': dataToLog
            },
            ],
            sequenceToken=self.nextSequenceToken)

        # update the Sequence token
        self.nextSequenceToken = rsp['nextSequenceToken']

        rsp['logged-value'] = dataToLog

        print(dataToLog)

        # Record the response in case the caller needs it
        self.response = rsp
