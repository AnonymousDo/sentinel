#!/bin/bash
set -evx

mkdir ~/.helpicocore

# safety check
if [ ! -f ~/.helpicocore/.helpico.conf ]; then
  cp share/helpico.conf.example ~/.helpicocore/helpico.conf
fi
