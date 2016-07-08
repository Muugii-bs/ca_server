import mysql.connector as db
import sys
import json
import operator
from itertools import izip
import xml.etree.ElementTree as ET

db_config = {
		'host':			'127.0.0.1',
		'port':			3306,
		'user':			'root',
		'password':	'root',
		'database':	'cnl',
		'autocommit': True,
}
conn = db.connect(**db_config)
cursor = conn.cursor()
prefix = "{http://scap.nist.gov/schema/vulnerability/0.4}"
prefix1 = "{http://scap.nist.gov/schema/cvss-v2/0.2}"

def xml_parse(_file):
    tree = ET.parse(_file)
    root = tree.getroot()
    for child in root:
        software_list = []
        entry_id = child.attrib['id']
        for softs in child.iter(prefix + 'vulnerable-software-list'):
            for soft in softs:
                software_list.append(soft.text)
        for date1 in child.iter(prefix + 'published-datetime'):
            published_datetime = date1.text
        for date2 in child.iter(prefix + 'last-modified-datetime'):
            updated_datetime = date2.text
        for cvss in child.iter(prefix1 + 'score'):
            score = cvss.text
        for cvss in child.iter(prefix1 + 'access-vector'):
            access_vector = cvss.text
        for cvss in child.iter(prefix1 + 'access-complexity'):
            access_complexity = cvss.text
        for cvss in child.iter(prefix1 + 'authentication'):
            authentication = cvss.text
        for cvss in child.iter(prefix1 + 'confidentiality-impact'):
            confidentiality_impact = cvss.text
        for cvss in child.iter(prefix1 + 'integrity-impact'):
            integrity_impact = cvss.text
        for cvss in child.iter(prefix1 + 'availability-impact'):
            availability_impact = cvss.text
        for cvss in child.iter(prefix + 'source'):    
            source = cvss.text
        for cvss in child.iter(prefix + 'reference'):
            reference = cvss.attrib['href']
        for cvss in child.iter(prefix + 'summary'):
            summary = cvss.text
        
        sql = "INSERT IGNORE INTO vuln_analyze (entry_id, software_list, published_datetime, updated_datetime, score, access_vector, access_complexity, authentication, confidentiality_impact, integrity_impact, availability_impact, source, reference, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
        cursor.execute(sql, (entry_id, json.dumps(software_list), published_datetime, updated_datetime, score, access_vector, access_complexity, authentication, confidentiality_impact, integrity_impact, availability_impact, source, reference, summary))
    
def main():
	xml_parse(sys.argv[1])
        cursor.close()
	conn.close()

if __name__ == '__main__':
	main()

