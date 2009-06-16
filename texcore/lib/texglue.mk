# Makefile
#

BASEDIR:=/path/to/texplates
WORKDIR:=$(shell mktemp -dt lucy.XXXXXX)
EMBEDMAP:=kozuka

SRC=$(WORKDIR)/texput

SRCFILES=$(WORKDIR)/embed-kozuka.map $(WORKDIR)/apporeport.sty


silencer:=<>/dev/null >&0 2>&0
silencer_out:=>/dev/null 2>&1
silencer_err:=2>/dev/null

all:	pdf-stream

init:  

tidy: 
	rm -f *.{aux,log} *~

clean:	tidy
	rm -f $(SRC).{ps,dvi,pdf} 

nuke:
	rm -rf $(WORKDIR)

pull:	$(SRCFILES)

dvi:	$(SRC).dvi

ps:     $(SRC).ps

pdf:    $(SRC).pdf

pdf-scatter: $(SRC).pdf
	(cd $(WORKDIR) && cat $(notdir $<) $(silencer_err))

dvi-scatter: $(SRC).dvi
	(cd $(WORKDIR) && cat $(notdir $<) $(silencer_err))

pdf-stream: pdf-scatter nuke

dvi-stream: dvi-scatter nuke

.PNONY:	all clean dvi ps pdf pdf-scatter dvi-scatter pdf-stream dvi-stream pull dirprep dirnuke

$(SRC).dvi: $(SRCFILES)
	(cd $(WORKDIR) && cat - > texput.tex && while (true); do platex texput.tex $(silencer_out) || exit $$?; grep -E 'Re-?run.*LaTeX' texput.log $(silencer_out) || break; done)

$(SRC).ps: $(SRC).dvi

$(SRC).pdf: $(SRC).dvi
	(cd $(WORKDIR) && dvipdfmx -f embed-$(EMBEDMAP).map $(notdir $(SRC).dvi) $(silencer))

$(WORKDIR):
	mkdir -p $(WORKDIR)

$(SRCFILES): $(WORKDIR)
	(cd $(WORKDIR) && ln -sfn $(BASEDIR)/$(notdir $@) . $(silencer))

# XXX: Making style files for successful pull.  The downside is, now
# you will be required to make them prior to operate Lucy (httpd's
# typically cannot write to the texplate directory.)
$(BASEDIR)/apporeport.sty: $(BASEDIR)/apporeport.ins
	(cd $(BASEDIR) && platex $< $(silencer))

%.ps:	%.dvi
	(cd $(WORKDIR) && dvips $< $(silencer))

%.pdf:	%.dvi
	(cd $(WORKDIR) && dvipdfmx $< $(silencer))

%.sty:  %.ins
	(cd $(WORKDIR) && platex $< $(silencer))
