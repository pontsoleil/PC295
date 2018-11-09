#! /bin/sh

Tmp=/tmp/${0##*/}.$$

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

dd bs=${CONTENT_LENGTH:-0} count=1 > $Tmp-cgivars
mime-read photo $Tmp-cgivars > $Tmp-photofile
filename=$(mime-read -v $Tmp-cgivars                                       | # tee log/${0##*/}.$$.step1.log |
  grep -Ei '^[0-9]+[[:blank:]]*Content-Disposition:[[:blank:]]*form-data;' | # tee log/${0##*/}.$$.step2.log |
  grep '[[:blank:]]name="photo"'                                           | # tee log/${0##*/}.$$.step3.log |
  head -n 1                                                                | # tee log/${0##*/}.$$.step4.log |
  sed 's/.*[[:blank:]]filename="\([^"]*\)".*/\1/'                          | # tee log/${0##*/}.$$.step5.log |
  tr '/"' '--'                                                             )
fullname=$(mime-read fullname $Tmp-cgivars)

cp $Tmp-photofile $filename

cat <<HTML_CONTENT
Content-Type: text/html

<html>
<head><title>Test</title></head>
<body>
<h1>Hello $fullname!</h1>
<img src="$filename" alt="$filename">
</body>
</html>
HTML_CONTENT

rm -f $Tmp-*
exit 0