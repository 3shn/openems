#!/bin/bash

# A script that creates the initial configuration files for Felix File Install
# to pick up, simulating the setup of the Simulator components and controllers.
# OpenEMS usually expects these in the felix-cache or config directory, but
# using the REST API is more robust.
# However, for an initial setup, dropping .config files might be easiest.
# Let's create a script that uses the OpenEMS REST API or drops .config files.
# It seems OpenEMS creates `io.openems.edge.application/generated/main/resources/config.d/`
# but since we are modifying the system, let's create a python script later
# to configure it via REST, or just write `.config` files to a standard location.

# Let's write OSGi config admin .config files.
mkdir -p felix-cache/config
mkdir -p load_data
cp load_profile.csv load_data/

# It might be easier to use a Python script with the REST API later, but the system
# needs to be running.
