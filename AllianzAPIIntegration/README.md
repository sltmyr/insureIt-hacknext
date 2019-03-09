# Hack to make Allianz API reachable from cloud
The Allianz API is only reachable from within local networks. We use one of our computers to run a small
flask server that tunnels requests from the could server to the Allianz API and returns the respose.
A static IP is generated using ngrok