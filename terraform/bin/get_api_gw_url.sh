#!/bin/bash
API_GW_URL=`chalice --project-dir .. url`
jq -n --arg api_gw_url "$API_GW_URL" '{"api_gw_url":$api_gw_url}'
