# Searching Keyword
# Example use : sh searchingKeyword.sh out_length "TargetKeyword"


OUT_LENGTH=5 # keyword
TARGET_KEYOWRD=$1 # keyword
# OUTPUT_PATH=$2

DIR="$( unset CDPATH && cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/searchingKeyword.py $TARGET_KEYOWRD $OUT_LENGTH
