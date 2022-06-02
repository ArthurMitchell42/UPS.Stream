# UPS.tream
## A web interface to display the status of a UPS from a NUT server.
This project came from the need to have a **_simple to set up_** viewer that displays the status of a UPS on a web page.

The NUT project[^1] has drivers and tools to work with deveices from most common UPS manufacturers but thier CGI based web monitor is a bit dated and not very easy to set up.

## Usage
This has been developed on a Synology NAS system but should run equally well on any server with a little more effort. The system should have the NAS connected to a server that it protects. The server should them be set to share the UPS status using the NUT protocol and port.

With Synology DSM this is very easy to do through the sontrol panel. After setting up your UPS and server just check _Enable network UPS server_ and add the IP address that the server will see when UPS.tream polls it.

The IP will depend of where the container is hosted.

![DSM Settings](https://github.com/ArthurMitchell42/UPS.tream/blob/adead57860be825315b6e682755a2546a6b8f733/dsm_ups_settings.png)

![System diagram](https://github.com/ArthurMitchell42/UPS.tream/blob/4fef439787a2fcbd48db8735c0b3f5a87682b66a/diagram1.png)

## Status
 
You can get a container with it at [Docker Hub](https://hub.docker.com/repository/docker/kronos443/ups.tream)

This code is **very pre-alpha**. Please feedback all experiences to help develop this app.

## To do and ideas

- [ ] Wrap in a Flask app template

[^1]: The [NUT project](https://networkupstools.org/)
