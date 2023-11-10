# Miriam and Sara Datalogger
this is a datalogger for Miriam (the live telemetry interface)

It can be run on any computer and saves the data published by Miriam on the different topics
related to the bike.

At the moment the server and the topics are temporarely set to "Taurus/bikedata/[topic name]", and it connects
to the open server broker.hivemq.com. During usage insert the password and username of our private server.

## How to run

When you are in the project root file, run the following command:

```Bash
python datalogger
```