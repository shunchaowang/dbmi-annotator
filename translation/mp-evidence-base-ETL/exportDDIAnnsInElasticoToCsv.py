 # Copyright 2016-2017 University of Pittsburgh

 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at

 #     http:www.apache.org/licenses/LICENSE-2.0

 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.

import csv
import uuid
import datetime
from sets import Set
import sys  
import validate as test
import codecs

from elastic import queryDDIDictAnnotation as es

reload(sys)  
sys.setdefaultencoding('utf8')


ES_HOST = "localhost"
ES_PORT = "9200"


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
        # csv.py doesn't do Unicode; encode temporarily as UTF-8:
        csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                                dialect=dialect, **kwargs)
        for row in csv_reader:
                # decode UTF-8 back to Unicode, cell by cell:
                yield [unicode(cell, 'utf-8') for cell in row]
                
def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
                yield line.encode('utf-8')



def run():

	#qryCondition = {'query': { 'term': {'annotationType': 'DDI'}}}

	#qryCondition = {'query': { 'term': {'rawurl': 'http://localhost/DDI-labels/829a4f51-c882-4b64-81f3-abfb03a52ebe.html'}}}

	qryCondition = {"query": {"bool": 
	 	{"must": [
	 		{"term": {"rawurl": "http://localhost/DDI-labels/75bf3473-2d70-4d41-93cd-afa1015e45bb.html"}},
	 		{"term": {"annotationType": "DDI"}}
	 	]
	  }}}

	results = es.queryDictAnnsByBody(ES_HOST, ES_PORT, qryCondition)
	print "[INFO] exported %s annotations from elasticsearch" % (len(results))	
		
	## write to csv
	#csv_columns = [unicode(x, 'utf-8') for x in ["document", "useremail", "claimlabel", "claimtext", "negation", "method", "relationship", "drug1", "drug2", "drug1PC", "drug2PC", "precipitant", "enzyme", "rejected", "evRelationship", "participants", "participantstext", "drug1dose", "drug1formulation", "drug1duration", "drug1regimens", "drug1dosetext", "drug2dose", "phenotypetype", "phenotypevalue", "phenotypemetabolizer", "phenotypepopulation", "drug2formulation", "drug2duration", "drug2regimens", "drug2dosetext", "aucvalue", "auctype", "aucdirection", "auctext", "cmaxvalue", "cmaxtype", "cmaxdirection", "cmaxtext", "clearancevalue", "clearancetype", "clearancedirection", "clearancetext", "halflifevalue", "halflifetype", "halflifedirection", "halflifetext", "dipsquestion", "reviewer", "reviewerdate", "reviewertotal", "reviewerlackinfo", "grouprandom", "parallelgroup", "id"]]
	csv_columns = [unicode(x, 'utf-8') for x in ["document", "useremail", "claimlabel", "claimtext", "method", "relationship", "drug1", "drug2", "evRelationship", "participants", "participantstotal", "participantsmale", "participantsfemale", "participantsmedianage", "participantsrace", "participantstumortype", "participantscancerstage", "participantstext", "drug1dose", "drug1formulation", "drug1duration", "drug1regimens", "drug1tolerateddose", "drug1dosetext", "drug2dose", "drug2formulation", "drug2duration", "drug2regimens", "drug2tolerateddose", "drug2dosetext", "radiotherapyYorN", "radiotherapytext", "deathfrequency", "withdrawalfrequency", "deathwithdrawaltext", "toxicitycriteria", "toxicityrow1", "toxicityrow2", "toxicityrow3", "toxicityrow4", "toxicityrow5", "toxicityrow6", "toxicityrow7", "toxicityrow8", "toxicityrow9", "toxicityrow10", "graderow1", "graderow2", "graderow3", "graderow4", "graderow5", "graderow6", "graderow7", "graderow8", "graderow9", "graderow10", "frequencyrow1", "frequencyrow2", "frequencyrow3", "frequencyrow4", "frequencyrow5", "frequencyrow6", "frequencyrow7", "frequencyrow8", "frequencyrow9", "frequencyrow10", "deathrow1", "deathrow2", "deathrow3", "deathrow4", "deathrow5", "deathrow6", "deathrow7", "deathrow8", "deathrow9", "deathrow10", "withdrawalrow1", "withdrawalrow2", "withdrawalrow3", "withdrawalrow4", "withdrawalrow5", "withdrawalrow6", "withdrawalrow7", "withdrawalrow8", "withdrawalrow9", "withdrawalrow10", "toxicitytext", "id"]]

	with codecs.open('data/exported-mp-annotations.csv', 'wb', 'utf8') as f: 
		w = csv.DictWriter(f, csv_columns)
		w.writeheader()
		w.writerows(results)


def main():
	run()

if __name__ == '__main__':
	main()