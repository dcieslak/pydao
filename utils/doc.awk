BEGIN {
	section = 0
	subsection = 0
	print "<html>"
	print "<body>"
	nListing = 1
	nImage = 1
	FS="|"
	DOC_MODE = ENVIRON["DOC_MODE"]
	AUTHOR = "<i>%s</i>"
	TITLE = "<h1>%s</h1>"
	IMAGE =\
		"<p align=center>"\
		"<img src={sFile} />"\
		"<br />Rysunek {nImage}. <b>{sOpis}</b>"\
		"</p>"
	LISTING = "<p style=\"margin-left: 5%\">"\
		"Listing {nListing}. <b>{sDescription}</b>"\
		"<br />"
	LISTING_LINE = "<tt>%s</tt><br />\n"
	LISTING_END = "</p>"
	KEYWORD_BEGIN = "<tt>"
	KEYWORD_END = "</tt>"
	RAMKA_BEGIN = "<table style=\"background: yellow\" align=right width=30%><tr><td>"
	RAMKA_END = "</td></tr></table>"
	NOP = " "
}

NR == 1 {
	TOC = FILENAME ".toc"
	while(1) {
		result = getline a < TOC
		if (result <= 0) {
			break
		}
		toc = toc a
	}
	print "" > TOC
}

function print_toc(number, prefix, s) {
	gsub(/<[^>]*>/, "", s)
	print prefix number ". <a href=\"#" number "\">" s "</a><br />" >> TOC
	print "<a name=\"" number "\"></a>"
}

/<toc>/ {
	print toc
}

/<h2>/ {
	section ++
	subsection = 0
	print_toc(section, "", $0)
	sub(/<h2>/, "<h2> " section ". ", $0)
}

/<h3>/ {
	subsection ++
	print_toc(section "." subsection, "&nbsp;&nbsp;&nbsp;", $0)
	sub(/<h3>/, "<h3> " section "." subsection ". ", $0)
}




$0 == "" {
	if(emptyLineAction)
	{
		print emptyLineAction
		emptyLineAction = ""
	}
}

/<author>/ {
	gsub(/<[^>]*>/, "")
	printf AUTHOR, $0
	next
}


/<title>/ {
	gsub(/<[^>]*>/, "")
	printf TITLE, $0
	next
}

$1 == "IMAGE" {
	sFile=$2
	sOpis=$3

	s = IMAGE
	gsub(/{sFile}/, sFile, s)
	gsub(/{sOpis}/, sOpis, s)
	gsub(/{nImage}/, nImage, s)
	print s

	if((getline b < sFile) < 0) {
		print FILENAME ":" FNR ": brak pliku" > "/dev/stderr"
		result = 1
	}
	close(sFile)

	nImage ++
	next
}

$1 == "INCLUDE" {
	sFile=$2
	sName=$3
	sDescription=$4

	sLang=""
	if(sFile ~ /\.py$/)
		sLang = "python"
	if(sFile ~ /\.txt$/)
		sLang = "txt"
	if(sFile ~ /\.php$/)
		sLang = "php"
	if(sFile ~ /\.xml$/)
		sLang = "xml"
	if(sFile ~ /\.awk$/)
		sLang = "awk"
	if(sFile ~ /\.sql$/)
		sLang = "sql"
	if(sFile ~ /\.java$/)
		sLang = "java"

	if(!sLang) {
		print FILENAME ":" FNR ": brak jêzyka" > "/dev/stderr"
		result = 1
	}

	s = LISTING
	gsub(/{nListing}/, nListing, s)
	gsub(/{sLang}/, sLang, s)
	gsub(/{sDescription}/, sDescription, s)
	print s
	
	skipTabs = ""
	bPrint = 0
	n = 0
	while((getline < sFile) > 0) {
		n ++
		if($0 ~ "BEGIN " sName) {
			if(match($0, /^[ \t][ \t]*/))
				skipTabs = substr($0, RSTART, RLENGTH)
			bPrint = 1
		}
		else if($0 ~ "END " sName) break
		else if(bPrint) {
			sub(skipTabs, "")
			if(length($0) > 60)
				print sFile ":" n ": >60"\
					> "/dev/stderr"
			gsub(/\t/, "   ")
			gsub(/\\&/, /\\&amp;/)
			gsub(/ /, "\\&nbsp;")
			gsub(/</, "\\&lt;")
			gsub(/>/, "\\&gt;")
			print sprintf(LISTING_LINE, $0)
		}
	}
	close(sFile)

	if(!bPrint) {
		print FILENAME ":" FNR ": brak tagu " sName > "/dev/stderr"
		result = 1
	}

	s = LISTING_END
	gsub(/{nListing}/, nListing, s)
	print s

	nListing ++
	next
}


/^   \$/ {
	$0 = substr($0, 4)
	printf LISTING_LINE, $0
	next
}

/^   / && !emptyLineAction {

	sDescription=substr($1, 4)
	sLang=$2

	if(sLang) {
		s = LISTING
		gsub(/{nListing}/, nListing, s)
		gsub(/{sLang}/, sLang, s)
		gsub(/{sDescription}/, sDescription, s)
		print s
		
		s = LISTING_END
		gsub(/{nListing}/, nListing, s)
		emptyLineAction = s

		nListing ++
		next
	} else {
		emptyLineAction = NOP
	}
}

/^   / {
	gsub(/&/, "\\&amp;");
	gsub(/</, "\\&lt;");
	gsub(/>/, "\\&gt;");
	gsub(/ /, "\\&nbsp;")
	printf LISTING_LINE, $0
	next
}

/<li>/ && !emptyLineAction {
	print "<ul>"
	emptyLineAction = "</ul>"
}

$0 != "" && !emptyLineAction && !/<h/ {
	print "<p>"
	emptyLineAction = "</p>"
}

{
	gsub("&listingbelow;", nListing)
	gsub("&listingbelow2;", nListing + 1)
	gsub("&listingabove;", nListing-1)
	gsub("&imagebelow;", nImage)
	gsub("&imageabove;", nImage-1)
	gsub("<k>", KEYWORD_BEGIN)
	gsub("<ramka>", RAMKA_BEGIN)
	gsub("</ramka>", RAMKA_END)
	gsub("</k>", KEYWORD_END)
	print
}


END {
	print "</body>"
	print "</html>"
	exit(result)
}









