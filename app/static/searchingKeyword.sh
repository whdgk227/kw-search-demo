# Searching Keyword
# Example use : sh searchingKeyword.sh "TargetKeyword"


TARGET_KEYOWRD=$1 # keyword
OUT_LENGTH=$2 # keyword
# OUTPUT_PATH=$2

DIR="$( unset CDPATH && cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/searchingKeyword.py $TARGET_KEYOWRD $OUT_LENGTH
