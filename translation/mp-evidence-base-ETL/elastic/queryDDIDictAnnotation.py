import sys, csv, json, re, os
import uuid
import datetime, copy
from elasticsearch import Elasticsearch
from elastic import operations as esop
from sets import Set


def queryDictAnnsById(host, port, annotationId):
	res = esop.queryById(host, port, annotationId)
	annsL = parseAnnotation(res)
	return annsL

def queryDictAnnsByBody(es_host, es_port, query_condit):
	## query condition (refers to elasticsearch REST API)
	doc = {'query': { 'term': {'annotationType': 'MP'}}}
	if query_condit:
		doc = query_condit

	res = esop.queryByBody(es_host, es_port, doc)	
	annsL = parseAnnotations(res['hits']['hits'])

	return annsL


def parseAnnotations(annotations):
	annsL = []
	for annotation in annotations:
		annsL.extend(parseAnnotation(annotation))
	return annsL


def parseAnnotation(annotation):
	annsL = []
	
	ann = annotation["_source"]
	initDict= getAnnDict()
	initDict["id"] = annotation["_id"]
	initDict["document"] = ann["rawurl"]
	initDict["useremail"] = ann["email"]
	
	claim = ann["argues"]
	initDict["claimlabel"] = claim["label"]
	initDict["claimtext"] = claim["hasTarget"]["hasSelector"]["exact"]
	initDict["method"] = claim["method"]	
	
	initDict["relationship"] = claim["qualifiedBy"]["relationship"]

	## drug 1 (required) and drug 2
	initDict["drug1"] = claim["qualifiedBy"]["drug1"]
	if "drug2" in claim["qualifiedBy"]:
		initDict["drug2"] = claim["qualifiedBy"]["drug2"]
	
	#if "enzyme" in claim["qualifiedBy"]:
		#initDict["enzyme"] = claim["qualifiedBy"]["enzyme"]

	#if "precipitant" in claim["qualifiedBy"]:
		#initDict["precipitant"] = claim["qualifiedBy"]["precipitant"]

	## parent coumpound
	#if "drug1PC" in claim["qualifiedBy"]:
		#initDict["drug1PC"] = claim["qualifiedBy"]["drug1PC"]

	#if "drug2PC" in claim["qualifiedBy"]:
		#initDict["drug2PC"] = claim["qualifiedBy"]["drug2PC"]

	#if "rejected" in claim and claim["rejected"]:			
		#initDict["rejected"] = claim["rejected"]["reason"] or ""

	dataL = claim["supportsBy"]

	## parse data & material
	if len(dataL) > 0:
		for data in dataL:

			annDict = copy.deepcopy(initDict)

			material = data["supportsBy"]["supportsBy"]
			annDict = addDataMaterialToAnnDict(data, material, annDict)
			annsL.append(annDict)
	else:
		annsL.append(initDict)

	return annsL

#global b
#b = ["Toxicity", "grade", "frequency", "death", "withdrawal"]


def addDataMaterialToAnnDict(data, material, annDict):
	## parse data
	if "evRelationship" in data:
		annDict["evRelationship"] = data["evRelationship"] or ""

	#for field in ["auc","cmax","clearance","halflife"]:
		#if data[field]:						
			#annDict[field+"value"] = data[field]["value"]
			#annDict[field+"type"] = data[field]["type"]
			#annDict[field+"direction"] = data[field]["direction"]
			#annDict[field+"text"] = getTextSpan(data[field])

	if data["radiotherapy"]:
		annDict["radiotherapyYorN"] = data["radiotherapy"]["r"]
		annDict["radiotherapytext"] = getTextSpan(data["radiotherapy"])

	if data["deathwithdrawal"]:
		annDict["deathfrequency"] = data["deathwithdrawal"]["deathFrequency"]
		annDict["withdrawalfrequency"] = data["deathwithdrawal"]["withdrawalFrequency"]
		annDict["deathwithdrawaltext"] = getTextSpan(data["deathwithdrawal"])

	if data["toxicity"]:
		annDict["toxicitycriteria"] = data["toxicity"]["toxicityCriteria"]

		#annDict["toxicityrow1"] = data["toxicity"]["Toxicity1"]
		'''for field in ["toxicityrow", "graderow", "frequencyrow", "deathrow", "withdrawalrow"]:
			if data[field]!= None:
				annDict[field +"1"] = data["toxicity"][b+"1"]
				annDict[field +"2"] = data["toxicity"][b+"2"]
				annDict[field +"3"] = data["toxicity"][b+"3"]
				annDict[field +"4"] = data["toxicity"][b+"4"]
				annDict[field +"5"] = data["toxicity"][b+"5"]
				annDict[field +"6"] = data["toxicity"][b+"6"]
				annDict[field +"7"] = data["toxicity"][b+"7"]
				annDict[field +"8"] = data["toxicity"][b+"8"]
				annDict[field +"9"] = data["toxicity"][b+"9"]
				annDict[field +"10"] = data["toxicity"][b+"10"]
			else:
				None
			if annDict[field+"1"] != None:
				annDict[field +"1"] = data["toxicity"][b+"1"]
			elif annDict[field+"2"] != None:
				annDict[field +"2"] = data["toxicity"][b+"2"]
			elif annDict[field+"3"] != None:
				annDict[field +"3"] = data["toxicity"][b+"3"]
			elif annDict[field+"4"] != None:
				annDict[field +"4"] = data["toxicity"][b+"4"]
			elif annDict[field+"5"] != None:
				annDict[field +"5"] = data["toxicity"][b+"5"]
			elif annDict[field+"6"] != None:
				annDict[field +"6"] = data["toxicity"][b+"6"]
			elif annDict[field+"7"] != None:
				annDict[field +"7"] = data["toxicity"][b+"7"]
			elif annDict[field+"8"] != None:
				annDict[field +"8"] = data["toxicity"][b+"8"]
			elif annDict[field+"9"] != None:
				annDict[field +"9"] = data["toxicity"][b+"9"]
			elif annDict[field+"10"] != None:
				annDict[field +"10"] = data["toxicity"][b+"10"]
			else:
				None'''
		'''if annDict["toxicityrow3"] != None:
			annDict["toxicityrow3"] = data["toxicity"]["Toxicity3"]
			print(annDict["toxicityrow3"])
		else:
			None
        
        
        annDict["toxicityrow1"] = data["toxicity"]["Toxicity1"] or ""
        if annDict["toxicityrow1"] != None:
        	return annDict["toxicityrow1"]
        else:
        	None

		if data["toxicity"]["Toxicity1"] != None:
			annDict["toxicityrow1"] = data["toxicity"]["Toxicity1"]
		else:
			None'''

		
		annDict["toxicityrow1"] = data["toxicity"]["Toxicity1"]
		annDict["toxicityrow2"] = data["toxicity"]["Toxicity2"] 
		annDict["toxicityrow3"] = data["toxicity"]["Toxicity3"]
		annDict["toxicityrow4"] = data["toxicity"]["Toxicity4"] 
		annDict["toxicityrow5"] = data["toxicity"]["Toxicity5"] 
		annDict["toxicityrow6"] = data["toxicity"]["Toxicity6"] 
		annDict["toxicityrow7"] = data["toxicity"]["Toxicity7"]
		annDict["toxicityrow8"] = data["toxicity"]["Toxicity8"]
		annDict["toxicityrow9"] = data["toxicity"]["Toxicity9"]
		annDict["toxicityrow10"] = data["toxicity"]["Toxicity10"]
		
		annDict["graderow1"] = data["toxicity"]["grade1"]
		annDict["graderow2"] = data["toxicity"]["grade2"]
		annDict["graderow3"] = data["toxicity"]["grade3"]
		annDict["graderow4"] = data["toxicity"]["grade4"]
		annDict["graderow5"] = data["toxicity"]["grade5"]
		annDict["graderow6"] = data["toxicity"]["grade6"]
		annDict["graderow7"] = data["toxicity"]["grade7"]
		annDict["graderow8"] = data["toxicity"]["grade8"]
		annDict["graderow9"] = data["toxicity"]["grade9"]
		annDict["graderow10"] = data["toxicity"]["grade10"]
		
		annDict["frequencyrow1"] = data["toxicity"]["frequency1"]
		annDict["frequencyrow2"] = data["toxicity"]["frequency2"]
		annDict["frequencyrow3"] = data["toxicity"]["frequency3"]
		annDict["frequencyrow4"] = data["toxicity"]["frequency4"]
		annDict["frequencyrow5"] = data["toxicity"]["frequency5"]
		annDict["frequencyrow6"] = data["toxicity"]["frequency6"]
		annDict["frequencyrow7"] = data["toxicity"]["frequency7"]
		annDict["frequencyrow8"] = data["toxicity"]["frequency8"]
		annDict["frequencyrow9"] = data["toxicity"]["frequency9"]
		annDict["frequencyrow10"] = data["toxicity"]["frequency10"]
		
		annDict["deathrow1"] = data["toxicity"]["death1"]
		annDict["deathrow2"] = data["toxicity"]["death2"]
		annDict["deathrow3"] = data["toxicity"]["death3"]
		annDict["deathrow4"] = data["toxicity"]["death4"]
		annDict["deathrow5"] = data["toxicity"]["death5"]
		annDict["deathrow6"] = data["toxicity"]["death6"]
		annDict["deathrow7"] = data["toxicity"]["death7"]
		annDict["deathrow8"] = data["toxicity"]["death8"]
		annDict["deathrow9"] = data["toxicity"]["death9"]
		annDict["deathrow10"] = data["toxicity"]["death10"]

		annDict["withdrawalrow1"] = data["toxicity"]["withdrawal1"]
		annDict["withdrawalrow2"] = data["toxicity"]["withdrawal2"]
		annDict["withdrawalrow3"] = data["toxicity"]["withdrawal3"]
		annDict["withdrawalrow4"] = data["toxicity"]["withdrawal4"]
		annDict["withdrawalrow5"] = data["toxicity"]["withdrawal5"]
		annDict["withdrawalrow6"] = data["toxicity"]["withdrawal6"]
		annDict["withdrawalrow7"] = data["toxicity"]["withdrawal7"]
		annDict["withdrawalrow8"] = data["toxicity"]["withdrawal8"]
		annDict["withdrawalrow9"] = data["toxicity"]["withdrawal9"]
		annDict["withdrawalrow10"] = data["toxicity"]["withdrawal10"]

		annDict["toxicitytext"] = getTextSpan(data["toxicity"])

	#if data["dips"]:
		#dipsQsStr = ""
		#qsL=["q1","q2","q3","q4","q5","q6","q7","q8","q9","q10"]
		#for q in qsL:
			#if q in data["dips"]:
				#if (q == len(qsL) - 1):
					#dipsQsStr += data["dips"][q]
				#else:
					#dipsQsStr += data["dips"][q] + "|"				
		#annDict["dipsquestion"] = dipsQsStr

	#if "reviewer" in data and data["reviewer"]:

		#annDict["reviewer"] = data["reviewer"]["reviewer"] or ""
		#annDict["reviewerdate"] = data["reviewer"]["date"] or ""
		#annDict["reviewertotal"] = data["reviewer"]["total"] or ""
		#annDict["reviewerlackinfo"] = data["reviewer"]["lackInfo"]

	#if "grouprandom" in data and data["grouprandom"]:
		#annDict["grouprandom"] = data["grouprandom"] or ""
						
	#if "parallelgroup" in data and data["parallelgroup"]:
		#annDict["parallelgroup"] = data["parallelgroup"] or ""
							
	## parse material
	if material["participants"]:
		annDict["participants"] = material["participants"]["value"] or ""
		annDict["participantstotal"] = material["participants"]["total"] or ""
		annDict["participantsmale"] = material["participants"]["male"] or ""
		annDict["participantsfemale"] = material["participants"]["female"] or ""
		annDict["participantsmedianage"] = material["participants"]["medianAge"] or ""
		annDict["participantsrace"] = material["participants"]["race"] or ""
		annDict["participantstumortype"] = material["participants"]["tumorType"] or ""
		annDict["participantscancerstage"] = material["participants"]["cancerStage"] or ""			
		annDict["participantstext"] = getTextSpan(material["participants"]) or ""
	
	if material["drug1Dose"]:
		annDict["drug1dose"] = material["drug1Dose"]["value"] or ""
		annDict["drug1formulation"] = material["drug1Dose"]["formulation"] or ""
		annDict["drug1duration"] = material["drug1Dose"]["duration"] or ""
		annDict["drug1regimens"] = material["drug1Dose"]["regimens"] or ""
		annDict["drug1tolerateddose"] = material["drug1Dose"]["toleratedDose"] or ""
		annDict["drug1dosetext"] = getTextSpan(material["drug1Dose"])

	if material["drug2Dose"]:
		annDict["drug2dose"] = material["drug2Dose"]["value"] or ""
		annDict["drug2formulation"] = material["drug2Dose"]["formulation"] or ""
		annDict["drug2duration"] = material["drug2Dose"]["duration"] or ""
		annDict["drug2regimens"] = material["drug2Dose"]["regimens"] or ""
		annDict["drug2tolerateddose"] = material["drug2Dose"]["toleratedDose"] or ""
		annDict["drug2dosetext"] = getTextSpan(material["drug2Dose"])

	#if material["phenotype"]:
		#annDict["phenotypetype"] = material["phenotype"]["type"] or ""
		#annDict["phenotypevalue"] = material["phenotype"]["typeVal"] or ""
		#if "metabolizer" in material["phenotype"] and "population" in material["phenotype"]:
			#annDict["phenotypemetabolizer"] = material["phenotype"]["metabolizer"] or ""
			#annDict["phenotypepopulation"] = material["phenotype"]["population"] or ""

	return annDict

def getAnnDict():
	return {"document": None, "useremail": None, "claimlabel": None, "claimtext": None, "method": None, "relationship": None, "drug1": None, "drug2": None, "evRelationship":None, "participants":None, "participantstotal":None, "participantsmale":None, "participantsfemale":None, "participantsmedianage":None, "participantsrace":None, "participantstumortype":None, "participantscancerstage":None, "participantstext":None, "drug1dose":None, "drug1formulation":None, "drug1duration":None, "drug1regimens":None, "drug1tolerateddose":None, "drug1dosetext":None, "drug2dose":None, "drug2formulation":None, "drug2duration":None, "drug2regimens":None, "drug2tolerateddose":None, "drug2dosetext":None, "radiotherapyYorN":None, "radiotherapytext":None, "deathfrequency":None, "withdrawalfrequency":None, "deathwithdrawaltext":None, "toxicitycriteria":None, "toxicityrow1":None, "toxicityrow2":None, "toxicityrow3":None, "toxicityrow4":None, "toxicityrow5":None, "toxicityrow6":None, "toxicityrow7":None, "toxicityrow8":None, "toxicityrow9":None, "toxicityrow10":None, "graderow1":None, "graderow2":None, "graderow3":None, "graderow4":None, "graderow5":None, "graderow6":None, "graderow7":None, "graderow8":None, "graderow9":None, "graderow10":None, "frequencyrow1":None, "frequencyrow2":None, "frequencyrow3":None, "frequencyrow4":None, "frequencyrow5":None, "frequencyrow6":None, "frequencyrow7":None, "frequencyrow8":None, "frequencyrow9":None, "frequencyrow10":None, "deathrow1":None, "deathrow2":None, "deathrow3":None, "deathrow4":None, "deathrow5":None, "deathrow6":None, "deathrow7":None, "deathrow8":None, "deathrow9":None, "deathrow10":None, "withdrawalrow1":None, "withdrawalrow2":None, "withdrawalrow3":None, "withdrawalrow4":None, "withdrawalrow5":None, "withdrawalrow6":None, "withdrawalrow7":None, "withdrawalrow8":None, "withdrawalrow9":None, "withdrawalrow10":None, "id": None}


def getTextSpan(field):
	if field["hasTarget"]:
		if field["hasTarget"]["hasSelector"]:
			return field["hasTarget"]["hasSelector"]["exact"]
	return ""


######################### MAIN ##########################

def main():
	print query()
	


if __name__ == '__main__':
	main()

