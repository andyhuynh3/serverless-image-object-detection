#!/bin/bash
eval "$(jq -r '@sh "ENV=\(.env)"')"
API_GW_URL=`chalice --project-dir .. url --stage $ENV`
jq -n --arg api_gw_url "$API_GW_URL" '{"api_gw_url":$api_gw_url}'
