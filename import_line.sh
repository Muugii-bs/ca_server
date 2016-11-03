mysql -u root -proot -e "LOAD DATA LOCAL INFILE '$1' INTO TABLE cnl1.vuln_line FIELDS TERMINATED BY '\t' (vuln_id, line)"
