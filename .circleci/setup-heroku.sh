#!/bin/bash
mkdir ~/.ssh/
ssh-keyscan -H heroku.com >> ~/.ssh/known_hosts

cat > ~/.netrc << EOF
machine api.heroku.com
  login $HEROKU_EMAIL
  password $HEROKU_TOKEN
machine git.heroku.com
  login $HEROKU_EMAIL
  password $HEROKU_TOKEN
EOF
