# CWLogger
Simple handler for cloudwatch logging. Just found it helpful rather than re-writing a handler each time I need to create a log, since the boto3 logs client isn't the easiest thing to work with.

# Usage
Requires boto3 to be installed and configured with read-write permissions to cloudwatch-logs.

If the log group is setup ahead of runtime, create-group permission is not needed.

```
import mylogger

log = mylogger.CWLog()
log.log("Text to log to cloudwatch-logs")
```

A specific log group can be specified:

```
log = mylogger.CWLog(logGroup='MyTestLogGroup/mylogs')
```

A specific log stream prefix can be specified:

```
log = mylogger.CWLog(logStreamName='MyStreamPrefix')
```

The default values:
```
defaultLogGroup = 'MyCustomLogs/Logs'
defaultLogStream = 'LogStream'
```
