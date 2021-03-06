
ZIPDIR = input_zip/

#pulled from: http://www.elections.ca/scripts/resval/ovr_41ge_pollbypoll.asp?lang=e
# 48 - Alberta
# 59 - British Columbia
# 46 - Manitoba
# 13 - New Brunswick
# 10 - Newfoundland and Labrador
# 61 - Northwest Territories
# 12 - Nova Scotia
# 62 - Nunavut
# 35 - Ontario
# 11 - Prince Edward Island
# 24 - Quebec
# 47 - Saskatchewan
# 60 - Yukon

#PROVINCES = 48 59 46 13 10 61 12 62 35 11 24 47 60 

# The url was reversed by watching the network requests using the chrome debugger
# http://www.elections.ca/scripts/PollbyPoll2011/CSV/48_csv.zip

#URLPREFIX = http://www.elections.ca/scripts/PollbyPoll2011/CSV/
#FORMAT_SUFFIX = _csv
#ZIPDIR = input_zip/
#ZIPS = $(patsubst %, $(ZIPDIR)/%$(FORMAT_SUFFIX).zip, $(PROVINCES))

#Updated: better results and canada-wide results can be found via a single zip file:
# found via this page: http://www.elections.ca/scripts/resval/ovr_41ge.asp
URLPREFIX = http://www.elections.ca/scripts/OVR2011/34/data_donnees/
ZIPS = $(ZIPDIR)/pollbypoll_bureauparbureau_canada.zip
CSVPREFIX = pollbypoll_bureauparbureau

CSVDIR = input_csv/
OUTPUTDIR = output_csv/
CSVFILEs = $(wildcard $(CSVDIR)/$(CSVPREFIX)*.csv)
OUTCSVFILES := $(patsubst $(CSVDIR)/%.csv, $(OUTPUTDIR)/%.csv, $(CSVFILEs))

all: process_csvs

$(ZIPDIR)/%.zip:
	mkdir -p $(ZIPDIR)
	curl --progress-bar $(URLPREFIX)/$(notdir $@) -o $@

$(CSVDIR)/unzipped: $(ZIPS)
	mkdir -p $(CSVDIR)
	unzip -d $(CSVDIR) "$(ZIPDIR)/*.zip" #todo: make unzip overwrite
	touch $(CSVDIR)/unzipped

getzips: $(CSVDIR)/unzipped

$(OUTPUTDIR):
		mkdir -p $(OUTPUTDIR)

$(OUTPUTDIR)/%.csv: $(CSVDIR)/%.csv $(OUTPUTDIR) combine_polls.py
	./combine_polls.py $(CSVDIR)/$(notdir $@) > $@

process_csvs: $(CSVDIR)/unzipped $(OUTCSVFILES)

.PHONY: process_csvs