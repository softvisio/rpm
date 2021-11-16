#!/bin/bash

set -e

# do not remove, need to install EV before coro, otherwise Coro::EV will not be available
cpanm EV Coro

cpanm Carton

cpanm HTTP::BrowserDetect
cpanm Imager
cpanm AnyEvent::Timer::Cron
cpanm Net::Subnet
