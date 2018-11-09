#!/bin/sh

# === Initialize shell environment ===================================
set -eux
# -e  Exit immediately if a command exits with a non-zero status.
# -u  Treat unset variables as an error when substituting.
# -v  Print shell input lines as they are read.
# -x  Print commands and their arguments as they are executed.
export LC_ALL=C
type command >/dev/null 2>&1 && type getconf >/dev/null 2>&1 &&
export PATH=".:$(command -p getconf PATH)${PATH+:}${PATH-}"
export UNIX_STD=2003  # to make HP-UX conform to POSIX
# === Log ============================================================
exec 2>log/${0##*/}.$$.log

Tmp=/tmp/${0##*/}.$$
printf '%s' "${QUERY_STRING:-}" | cgi-name > $Tmp-cgivars
fullname=$(nameread fullname $Tmp-cgivars)

cat <<HTML_CONTENT
Content-Type: text/html

<html>
<head><title>Test</title></head>
<body>
<h1>Hello $fullname!</h1>
</body>
</html>
HTML_CONTENT

rm -f $Tmp-*
exit 0
