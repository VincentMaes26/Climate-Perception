#!/bin/bash
set -e
sudo -u ec2-user -i <<'EOF'
ENVIRONMENT=python3
source /home/ec2-user/anaconda3/bin/activate "$ENVIRONMENT"
pip install --upgrade cufflinks yellowbrick wordcloud joblib
source /home/ec2-user/anaconda3/bin/deactivate
EOF
