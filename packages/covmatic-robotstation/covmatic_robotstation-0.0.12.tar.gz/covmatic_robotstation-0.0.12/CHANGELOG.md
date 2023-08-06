# Covmatic RobotControl

## v0.0.12
- [RobotStation] Disabled watchdog timeout waiting for plate transfer.
- [RobotStation] Fixed broken trash behaviour since changes in *covmatic-robotmanager* v0.0.3;
- [Robot] Actions pick and drop added option to continue without waiting for action to complete;
- [Robot] Actions pick and drop now return retrieved action-id.

## v0.0.11
- [RobotStation] Added internal plate transfer function
- [Robot] Changed the wait logic to be able to launch pick and drop action for internal plate transfer.

## v0.0.10
- [RobotStation] Fixed typo in log messages.

## v0.0.9
- [RobotStation] Added trash function to pick the plate and drop in the TRASH location
- [RobotStation] Fixed bug in logs if run_stage was false

## v0.0.8
- [RobotStation] Added start_at logic to skip plate transfers if previous stages not run
- [RobotStation] Added user message for manual transfer if problem requesting robot transfer
- [API] Added timeout to HTTP requests

## v0.0.7

- [API] Fixed *POST* request for actions.
- Fixed bug in robot position build
- Fixed tests for Python 3.7

## v0.0.6

- [RobotStation] Added *RobotManager* server **port** parameter.

## v0.0.5

- Advanced *covmatic-stations* requirements to v2.19.7

## v0.0.4

- Added home command from *covmatic-stations* v2.19.6

## v0.0.3

- Renamed project to **covmatic-robotstation**
- [Robot API] Fixed action request

## v0.0.2

Initial release

